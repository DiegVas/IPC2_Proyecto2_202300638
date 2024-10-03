from graphviz import Digraph


def generate_tda_graph(machine, product, time):
    dot = Digraph(comment="TDA Report")
    dot.attr(rankdir="LR")

    # Create a subgraph for the machine
    with dot.subgraph(name="cluster_machine") as c:
        c.attr(label=f"Machine: {machine.nombre}")
        c.node(
            "machine",
            f"Name: {machine.nombre}\\nLines: {machine.num_lineas_produccion}\\nComponents: {machine.num_componentes}",
        )

    # Create a subgraph for the product
    with dot.subgraph(name="cluster_product") as c:
        c.attr(label=f"Product: {product.nombre}")
        c.node(
            "product",
            f"Name: {product.nombre}\\nSequence: {product.secuencia_ensamblaje}",
        )

    # Simulate assembly up to the specified time
    assembly_data = simulate_assembly(machine, product, time)

    # Create nodes for each assembly line
    for i in range(machine.num_lineas_produccion):
        dot.node(f"line_{i}", f"Line {i+1}")

    # Create nodes for each second and its actions
    for second_node in assembly_data.secondsActions:
        if second_node.second > time:
            break

        second_id = f"second_{second_node.second}"
        dot.node(second_id, f"Second {second_node.second}")

        if second_node.second > 1:
            dot.edge(f"second_{second_node.second-1}", second_id)

        for i, action in enumerate(second_node.actions):
            action_id = f"action_{second_node.second}_{i}"
            dot.node(action_id, action)
            dot.edge(second_id, action_id)
            dot.edge(action_id, f"line_{i}")

    # Render the graph
    dot.render(
        f"tda_report_{machine.nombre}_{product.nombre}_time_{time}",
        format="png",
        cleanup=True,
    )
    print(
        f"TDA report graph generated: tda_report_{machine.nombre}_{product.nombre}_time_{time}.png"
    )


# Usage example:
# machine = ... # Your machine object
# product = ... # Your product object
# time = 10  # The time up to which you want to visualize the assembly process
# generate_tda_graph(machine, product, time)
