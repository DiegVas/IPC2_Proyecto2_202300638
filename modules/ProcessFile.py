import xml.etree.ElementTree as ET
from classes.Machine import Machine

# Función para leer el archivo XML
def ProcessFile(ruta_xml, CiruclarList):
    # Cargar y parsear el archivo XML
    arbol = ET.parse(ruta_xml)
    raiz = arbol.getroot()
    
    # ? Recorrer cada máquina
    for maquina in raiz.findall('Maquina'):
        name_Machine = maquina.find('NombreMaquina').text
        lineas_Production = maquina.find('CantidadLineasProduccion').text
        components = maquina.find('CantidadComponentes').text
        time_Assembly = maquina.find('TiempoEnsamblaje').text
        
        machine = Machine(name_Machine, lineas_Production, components)
        
        
        
        # ? Recorrer los productos de cada máquina
        productos = maquina.find('ListadoProductos')
        for producto in productos.findall('Producto'):
            
            name_Product = producto.find('nombre').text
            assembly_Sequence = producto.find('elaboracion').text
            
            machine.agregar_producto(name_Product, assembly_Sequence)
            
        # ! Agregar la máquina a la lista circular
        machine.obtener_info()
        machine.mostrar_productos()
        
        CiruclarList.append(machine)
        
        print()  # Espacio entre máquinas

