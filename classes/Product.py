class Producto:
    def __init__(self, nombre, secuencia_ensamblaje):
        self.nombre = nombre
        self.secuencia_ensamblaje = secuencia_ensamblaje


class NodoProducto:
    def __init__(self, producto):
        self.producto = producto
        self.siguiente = None


class ListaCircularProductos:
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def agregar_producto(self, producto):
        nuevo_nodo = NodoProducto(producto)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def eliminar_producto(self, nombre_producto):
        if self.esta_vacia():
            return

        if self.cabeza.producto.nombre == nombre_producto:
            if self.cabeza.siguiente == self.cabeza:
                self.cabeza = None
            else:
                actual = self.cabeza
                while actual.siguiente != self.cabeza:
                    actual = actual.siguiente
                actual.siguiente = self.cabeza.siguiente
                self.cabeza = self.cabeza.siguiente
        else:
            actual = self.cabeza
            anterior = None
            while actual.siguiente != self.cabeza:
                anterior = actual
                actual = actual.siguiente
                if actual.producto.nombre == nombre_producto:
                    anterior.siguiente = actual.siguiente
                    break

    def mostrar_productos(self):
        if self.esta_vacia():
            print("No hay productos en la máquina.")
            return
        actual = self.cabeza
        while True:
            print(f"Producto: {actual.producto.nombre}")
            print(f"Secuencia de ensamblaje: {actual.producto.secuencia_ensamblaje}")
            print("---------")
            actual = actual.siguiente
            if actual == self.cabeza:
                break

    def __iter__(self):
        if self.esta_vacia():
            return
        actual = self.cabeza
        while True:
            yield actual.producto
            actual = actual.siguiente
            if actual == self.cabeza:
                break
