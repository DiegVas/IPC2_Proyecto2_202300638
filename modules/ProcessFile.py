import xml.etree.ElementTree as ET
from classes.Machine import Machine
from classes.LinkedLists import (
    StepLinkedList,
    LinkedList,
    ActionLinkedList,
    TimeLinkedList,
    ProductLinkedList,
)


# Función para leer el archivo XML
def ProcessFile(ruta_xml, CiruclarList):

    # Cargar y parsear el archivo XML
    arbol = ET.parse(ruta_xml)
    raiz = arbol.getroot()

    # ? Recorrer cada máquina
    for maquina in raiz.findall("Maquina"):
        name_Machine = maquina.find("NombreMaquina").text
        lineas_Production = int(maquina.find("CantidadLineasProduccion").text)
        components = int(maquina.find("CantidadComponentes").text)
        time_Assembly = int(maquina.find("TiempoEnsamblaje").text)

        machine = Machine(name_Machine, lineas_Production, components)
        machine.tiempo_ensamblaje = time_Assembly

        # ? Recorrer los productos de cada máquina
        productos = maquina.find("ListadoProductos")
        for producto in productos.findall("Producto"):

            name_Product = producto.find("nombre").text
            assembly_Sequence = producto.find("elaboracion").text

            machine.agregar_producto(name_Product, assembly_Sequence)

        # ! Agregar la máquina a la lista circular
        CiruclarList.append(machine)


def simulate_assembly(machine, product):

    # ? Extraer los pasos de ensamblaje
    assembly_steps = extract_assembly_steps(product.secuencia_ensamblaje)

    # * LinkedLists
    # ? Inicializar las posiciones actuales de los brazos
    current_positions = LinkedList()
    timeLinked = TimeLinkedList()

    # * Variable de ensamblaje
    total_time = 0
    next_assembly_index = 0

    # ! Cambio de estrucutras de datos
    assembly_in_progress = LinkedList()
    assembly_time_left = LinkedList()

    # * Todas las lineas empiezan en el componente -1
    for _ in range(machine.num_lineas_produccion):
        current_positions.append(-1)
        assembly_in_progress.append(False)
        assembly_time_left.append(machine.tiempo_ensamblaje)

    def RecopileAction(time, actions):
        actionLinked = ActionLinkedList()

        for action in actions:
            actionLinked.append(action)

        timeLinked.append(time, actionLinked)

    while next_assembly_index < assembly_steps.length():

        actions = LinkedList()
        total_time += 1

        for _ in range(machine.num_lineas_produccion):
            actions.append("No hacer nada")

        next_step = assembly_steps.get(next_assembly_index)  # ? Obtener el nodo
        next_line = next_step.line - 1  # ? Acceder al atributo 'line'
        next_component = next_step.component - 1  # ? Acceder al atributo 'component'

        for line in range(machine.num_lineas_produccion):

            # ? Obtener la posición actual del brazo
            current_position = current_positions.get(line)

            if line == next_line:

                # * Si la posición actual no es la misma que la del siguiente componente
                if current_position != next_component:

                    # ? Mover brazo a la derecha o izquierda
                    direction = "→" if next_component > current_position else "←"

                    current_positions.set(
                        line,
                        (
                            current_position + 1
                            if direction == "→"
                            else current_position - 1
                        ),
                    )

                    # ? Agregar la acción a la lista
                    actions.set(
                        line,
                        f"Mover brazo {direction} C{current_positions.get(line) + 1}",
                    )

                # * Si la posición actual es la misma que la del siguiente componente
                elif current_position == next_component:

                    # ? Si no hay ensamblaje en progreso
                    if not assembly_in_progress.get(line):
                        assembly_in_progress.set(line, True)
                        assembly_time_left.set(line, machine.tiempo_ensamblaje)
                        actions.set(line, f"Ensamblar C{next_component + 1}")
                        assembly_time_left.set(line, assembly_time_left.get(line) - 1)

                    # ? Si hay ensamblaje en progreso
                    else:
                        actions.set(line, f"Ensamblando C{next_component + 1}")
                        assembly_time_left.set(line, assembly_time_left.get(line) - 1)

                    # ? Si el ensamblaje ha terminado
                    if assembly_time_left.get(line) == 0:
                        assembly_in_progress.set(line, False)
                        next_assembly_index += 1

            else:

                # ? Buscar el próximo paso para esta línea
                next_step_for_line = next(
                    (
                        s
                        # ? Obtener el siguiente paso para la línea actual
                        for s in (
                            assembly_steps.get(i)
                            for i in range(next_assembly_index, assembly_steps.length())
                        )
                        if s.line - 1 == line
                    ),
                    None,
                )

                # ? Si hay un próximo paso para esta línea
                if next_step_for_line:
                    target_component = next_step_for_line.component - 1
                    if current_position != target_component:
                        direction = "→" if target_component > current_position else "←"
                        current_positions.set(
                            line,
                            (
                                current_position + 1
                                if direction == "→"
                                else current_position - 1
                            ),
                        )
                        actions.set(
                            line,
                            f"Mover brazo {direction} C{current_positions.get(line) + 1}",
                        )

        # * Agregar la acción a la lista
        RecopileAction(total_time, actions)

    ProductLinked = ProductLinkedList()
    ProductLinked.append(
        product.nombre, total_time, timeLinked, machine.num_lineas_produccion
    )

    return ProductLinked


def extract_assembly_steps(secuenciaEnsam):

    # * Lista enlzada para los pasos
    steps = StepLinkedList()

    i = 0

    while i < len(secuenciaEnsam):

        if secuenciaEnsam[i] == "L" and (i + 1) < len(secuenciaEnsam):

            j = i + 1

            while j < len(secuenciaEnsam) and secuenciaEnsam[j].isdigit():
                j += 1

            linea = int(secuenciaEnsam[i + 1 : j])  # Extraer el número de línea

            if j < len(secuenciaEnsam) and secuenciaEnsam[j] == "C":

                k = j + 1

                while k < len(secuenciaEnsam) and secuenciaEnsam[k].isdigit():
                    k += 1
                componente = int(
                    secuenciaEnsam[j + 1 : k]
                )  # ? Extraer el número de componente

                steps.append(linea, componente)  # ? Agregar el paso como un nodo

                i = k  # ? Avanzar al siguiente paso
            else:
                i += 1
        else:
            i += 1
    return steps
