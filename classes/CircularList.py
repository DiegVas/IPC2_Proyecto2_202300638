class Node:
    def __init__(self, Machine):
        self.Machine = Machine
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def prepend(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            new_node.next = self.head
            current.next = new_node
            self.head = new_node

    def delete(self, key):
        if self.is_empty():
            return

        if self.head.data == key:
            current = self.head
            while current.next != self.head:
                current = current.next
            if self.head == self.head.next:
                self.head = None
            else:
                current.next = self.head.next
                self.head = self.head.next
        else:
            current = self.head
            prev = None
            while current.next != self.head:
                prev = current
                current = current.next
                if current.data == key:
                    prev.next = current.next
                    break

    def display(self):
        if self.is_empty():
            print("La lista está vacía")
            return
        current = self.head
        while True:
            print(current.Machine, end=" -> ")
            current = current.next
            if current == self.head:
                break
        print(" (vuelta al inicio)")

    def __iter__(self):
        if self.is_empty():
            return
        current = self.head
        while True:
            yield current.Machine
            current = current.next
            if current == self.head:
                break
