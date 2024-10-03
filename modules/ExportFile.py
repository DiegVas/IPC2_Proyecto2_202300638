import xml.etree.ElementTree as ET
from xml.dom import minidom
from modules.ProcessFile import simulate_assembly


def generate_output_xml(machines):
    root = ET.Element("SalidaSimulacion")

    for machine in machines:
        machine_elem = ET.SubElement(root, "Maquina")
        ET.SubElement(machine_elem, "Nombre").text = machine.nombre

        products_elem = ET.SubElement(machine_elem, "ListadoProductos")

        for product in machine.productos:
            product_elem = ET.SubElement(products_elem, "Producto")
            ET.SubElement(product_elem, "Nombre").text = product.nombre

            # Simulate assembly and get ProductLinkedList
            product_linked = simulate_assembly(machine, product)

            for product_node in product_linked:
                ET.SubElement(product_elem, "TiempoTotal").text = str(
                    product_node.total_time
                )

                elaboration_elem = ET.SubElement(product_elem, "ElaboracionOptima")

                for time_node in product_node.secondsActions:
                    time_elem = ET.SubElement(elaboration_elem, "Tiempo")
                    time_elem.set("NoSegundo", str(time_node.second))

                    for i, action in enumerate(time_node.actions):
                        line_elem = ET.SubElement(time_elem, "LineaEnsamblaje")
                        line_elem.set("NoLinea", str(i + 1))
                        line_elem.text = action

    # Convert to string and pretty print
    rough_string = ET.tostring(root, "utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Write to file
    with open("salida.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)


# Usage
# circular_list = CircularList()  # Assuming you have this from your input processing
# ProcessFile("input.xml", circular_list)
# generate_output_xml(circular_list)
