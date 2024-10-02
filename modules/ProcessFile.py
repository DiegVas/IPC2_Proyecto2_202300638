import xml.etree.ElementTree as ET
from classes.Machine import Machine
import re


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
        # machine.obtener_info()
        # machine.mostrar_productos()

        CiruclarList.append(machine)

        print()  # Espacio entre máquinas

        for producto in machine.productos:
            print(f"\nSimulación para el producto: {producto.nombre}")
            simulate_assembly(machine, producto)


def simulate_assembly(machine, product):
    assembly_steps = extract_assembly_steps(product.secuencia_ensamblaje)
    total_time = 0
    current_positions = LinkedList()
    for _ in range(machine.num_lineas_produccion):
        current_positions.append(-1)
    next_assembly_index = 0

    def print_table_row(time, actions):
        if time == "":
            print("Tiempo".ljust(10), end="|")
            for i in range(machine.num_lineas_produccion):
                print(f"Línea {i+1}".ljust(30), end="|")
            print()
            print("-" * (11 + 31 * machine.num_lineas_produccion))
            return
        print(f"{time:<10}|", end="")
        for action in actions:
            print(f"{action:<30}|", end="")
        print()

    print_table_row(
        "", ["Tiempo"] + [f"Línea {i+1}" for i in range(machine.num_lineas_produccion)]
    )

    while next_assembly_index < assembly_steps.length():
        total_time += 1
        actions = LinkedList()
        for _ in range(machine.num_lineas_produccion):
            actions.append("No hacer nada")

        next_step = assembly_steps.get(next_assembly_index)  # Obtener el nodo
        next_line = next_step.line - 1  # Acceder al atributo 'line'
        next_component = next_step.component - 1  # Acceder al atributo 'component'

        for line in range(machine.num_lineas_produccion):
            current_position = current_positions.get(line)

            if line == next_line:
                if current_position != next_component:
                    direction = "→" if next_component > current_position else "←"
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
                elif current_position == next_component:
                    actions.set(line, f"Ensamblar C{next_component + 1}")
                    total_time += (
                        machine.tiempo_ensamblaje - 1
                    )  # -1 porque ya contamos 1 segundo en este ciclo
                    next_assembly_index += 1
            else:
                # Buscar el próximo paso para esta línea
                next_step_for_line = next(
                    (
                        s
                        for s in (
                            assembly_steps.get(i)
                            for i in range(next_assembly_index, assembly_steps.length())
                        )
                        if s.line - 1 == line
                    ),
                    None,
                )
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

        # Convierte la lista enlazada actions a una lista regular para imprimir
        action_list = []
        current_node = actions.head
        while current_node:
            action_list.append(current_node.data)
            current_node = current_node.next

        print_table_row(total_time, action_list)

    print(
        f"\nEl producto {product.nombre} se puede elaborar óptimamente en {total_time} segundos."
    )


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class StepNode:
    def __init__(self, line, component):
        self.line = line  # Línea del paso
        self.component = component  # Componente del paso
        self.next = None  # Apuntador al siguiente nodo


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current.data
            count += 1
            current = current.next
        return None

    def set(self, index, data):
        current = self.head
        count = 0
        while current:
            if count == index:
                current.data = data
                return
            count += 1
            current = current.next

    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count


class StepLinkedList:
    def __init__(self):
        self.head = None

    def append(self, line, component):
        new_node = StepNode(line, component)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current  # Devuelve el nodo completo, no solo los datos
            count += 1
            current = current.next
        return None

    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count


def extract_assembly_steps(secuencia_ensamblaje):
    steps = StepLinkedList()
    i = 0
    while i < len(secuencia_ensamblaje):
        if secuencia_ensamblaje[i] == "L" and (i + 1) < len(secuencia_ensamblaje):
            j = i + 1
            while j < len(secuencia_ensamblaje) and secuencia_ensamblaje[j].isdigit():
                j += 1
            linea = int(secuencia_ensamblaje[i + 1 : j])  # Extraer el número de línea
            if j < len(secuencia_ensamblaje) and secuencia_ensamblaje[j] == "C":
                k = j + 1
                while (
                    k < len(secuencia_ensamblaje) and secuencia_ensamblaje[k].isdigit()
                ):
                    k += 1
                componente = int(
                    secuencia_ensamblaje[j + 1 : k]
                )  # Extraer el número de componente
                steps.append(linea, componente)  # Agregar el paso como un nodo
                i = k  # Avanzar al siguiente paso
            else:
                i += 1
        else:
            i += 1
    return steps
