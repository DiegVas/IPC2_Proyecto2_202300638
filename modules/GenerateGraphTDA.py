import graphviz


def generate_tda_report(machine, product_name, specific_time):
    dot = graphviz.Digraph(comment="Estado de la Cola de Ensamblaje")
    dot.attr(rankdir="LR")  # Establecer dirección de izquierda a derecha

    # Encontrar el producto en la máquina
    product = next((p for p in machine.productos if p.nombre == product_name), None)
    if not product:
        print(f"Producto {product_name} no encontrado en la máquina {machine.nombre}")
        return

    # Obtener los pasos de ensamblaje
    assembly_steps = extract_assembly_steps(product.secuencia_ensamblaje)

    # Calcular qué pasos ya se han completado en el tiempo específico
    completed_steps = 0
    current_time = 0
    for step in assembly_steps:
        if current_time + 1 > specific_time:  # +1 por el movimiento del brazo
            break
        current_time += 1  # Tiempo para mover el brazo
        completed_steps += 1
        if current_time + machine.tiempo_ensamblaje > specific_time:
            break
        current_time += machine.tiempo_ensamblaje  # Tiempo para ensamblar

    # Crear nodos para los pasos restantes
    previous_node = None
    for i in range(completed_steps, len(assembly_steps)):
        step = assembly_steps[i]
        node_name = f"L{step['line']}C{step['component']}"
        dot.node(node_name, node_name)
        if previous_node:
            dot.edge(previous_node, node_name)
        previous_node = node_name

    # Generar el gráfico
    dot.render(
        f"tda_report_{machine.nombre}_{product_name}_time_{specific_time}",
        view=True,
        format="png",
    )


# ! USO DE LISRASSS
def extract_assembly_steps(secuencia_ensamblaje):
    steps = []
    i = 0
    while i < len(secuencia_ensamblaje):
        if secuencia_ensamblaje[i] == "L" and (i + 1) < len(secuencia_ensamblaje):
            j = i + 1
            while j < len(secuencia_ensamblaje) and secuencia_ensamblaje[j].isdigit():
                j += 1
            linea = int(secuencia_ensamblaje[i + 1 : j])
            if j < len(secuencia_ensamblaje) and secuencia_ensamblaje[j] == "C":
                k = j + 1
                while (
                    k < len(secuencia_ensamblaje) and secuencia_ensamblaje[k].isdigit()
                ):
                    k += 1
                componente = int(secuencia_ensamblaje[j + 1 : k])
                steps.append({"line": linea, "component": componente})
                i = k
            else:
                i += 1
        else:
            i += 1
    return steps


# Ejemplo de uso:
# machine = Machine("MaquinaA", 2, 5)
# machine.agregar_producto("ProductoX", "L1C2 L2C3 L1C4 L2C1")
# generate_tda_report(machine, "ProductoX", 3)  # Genera el reporte para el segundo 3
