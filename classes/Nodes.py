class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class StepNode:
    def __init__(self, line, component):
        self.line = line  # Línea del paso
        self.component = component  # Componente del paso
        self.next = None  # Apuntador al siguiente nodo


class ActionNode:
    def __init__(self, action):
        self.action = action  # Acción a realizar
        self.next = None  # Apuntador al siguiente nodo


class TimeNode:
    def __init__(self, second, actionLinked):
        self.second = second  # Segundo actual
        self.actions = actionLinked  # Lista enlazada de acciones
        self.next = None  # Apuntador al siguiente nodo


class ProductNode:
    def __init__(self, name, total_time, secondsActions):
        self.name = name  # Nombre del producto
        self.total_time = total_time  # Tiempo total para ensamblar
        self.next = None  # Apuntador al siguiente nodo
        self.secondsActions = secondsActions  # Lista enlazada de segundos y acciones
