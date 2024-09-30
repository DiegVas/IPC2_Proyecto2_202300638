from classes.Product import Producto, ListaCircularProductos

class Machine:
    def __init__(self, nombre, num_lineas_produccion, num_componentes):
        self.nombre = nombre
        self.num_lineas_produccion = num_lineas_produccion
        self.num_componentes = num_componentes
        self.productos = ListaCircularProductos()

    def agregar_producto(self, nombre_producto, secuencia_ensamblaje):
        nuevo_producto = Producto(nombre_producto, secuencia_ensamblaje)
        self.productos.agregar_producto(nuevo_producto)

    def eliminar_producto(self, nombre_producto):
        self.productos.eliminar_producto(nombre_producto)

    def mostrar_productos(self):
        print(f"Productos en la máquina {self.nombre}:")
        self.productos.mostrar_productos()

    def obtener_info(self):
        return f"Máquina: {self.nombre}\n" \
               f"Líneas de producción: {self.num_lineas_produccion}\n" \
               f"Componentes por línea: {self.num_componentes}"