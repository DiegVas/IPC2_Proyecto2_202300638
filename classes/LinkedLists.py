from classes.Nodes import Node, StepNode, ActionNode, TimeNode, ProductNode


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

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next


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


class ActionLinkedList:
    def __init__(self):
        self.head = None

    def append(self, action):
        new_node = ActionNode(action)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def set(self, index, data):
        current = self.head
        count = 0
        while current:
            if count == index:
                current.data = data
                return
            count += 1
            current = current.next

    def __iter__(self):
        current = self.head
        while current:
            yield current.action
            current = current.next


class TimeLinkedList:
    def __init__(self):
        self.head = None

    def append(self, second, actionLinked):
        new_node = TimeNode(second, actionLinked)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        return new_node  # Retornar el nodo recién creado

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next


class ProductLinkedList:
    def __init__(self):
        self.head = None

    def append(self, name, total_time, secondsActions):
        new_node = ProductNode(name, total_time, secondsActions)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next
