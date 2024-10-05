import graphviz
from classes.LinkedLists import (
    LinkedList,
    ActionLinkedList,
    TimeLinkedList,
    ProductLinkedList,
    StepLinkedList,
)
from modules.ProcessFile import extract_assembly_steps
import os


def generate_tda_report(machine, product, timeSpecific, LinkedLists):

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

    while next_assembly_index < assembly_steps.length() and total_time < timeSpecific:

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
                        if total_time < timeSpecific:
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

    next_steps = get_next_steps(assembly_steps, next_assembly_index)

    generate_tda_graph(machine, product, timeSpecific, next_steps, link=LinkedLists)

    return next_steps


def get_next_steps(stepsLink, next_assembly_index):
    next_steps = StepLinkedList()
    for i in range(next_assembly_index, stepsLink.length()):
        next_steps.append(i, stepsLink.get(i))
    return next_steps


def generate_tda_graph(machine, product, specific_time, next_steps, link):

    dot = graphviz.Digraph(
        comment=f"Estado de la Cola de Ensamblaje en tiempo {specific_time}"
    )

    dot.attr(rankdir="LR")

    current = next_steps.head
    current_previeus = None

    while current:

        dot.node(
            str(current.line),
            f"L{current.component.line}C{current.component.component}",
        )
        if current_previeus:
            dot.edge(str(current_previeus.line), str(current.line))
        current_previeus = current
        current = current.next

    outputPath = f"static/{machine.nombre}_{product.nombre}_{specific_time}"
    link.append(outputPath)
    # Generate the graph
    dot.render(
        outputPath,
        format="png",
    )
    dot.render("static/tda_graph", format="png")
