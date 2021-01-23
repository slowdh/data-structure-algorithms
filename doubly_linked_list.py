class Node:
    def __init__(self, val, prev=None, next=None):
        self.val, self.prev, self.next = val, prev, next


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def search(self, val):
        node_curr = self.head
        while node_curr is not None:
            if node_curr.val == val:
                return node_curr
            node_curr = node_curr.next
        raise ValueError(f'Object with value {val} doesn\'t exist!')

    def visit(self, idx):
        if not (0 <= idx < self.size):
            raise ValueError('Index out of range!')
        if idx < self.size // 2:
            node_curr = self.head
            for _ in range(idx):
                node_curr = node_curr.next
        else:
            node_curr = self.tail
            for _ in range(self.size - 1 - idx):
                node_curr = node_curr.prev
        return node_curr
    
    def insert_at(self, idx, val):
        if idx > self.size:
            raise ValueError('Index out of range!')
        node_insert = Node(val=val)
        if idx == 0:
            node_insert.next = self.head
            self.head.prev = node_insert
            self.head = node_insert
        else:
            node_prev = self.visit(idx - 1)
            node_next = node_prev.next
            node_prev.next = node_insert
            node_insert.prev = node_prev
            node_insert.next = node_next
            if node_next == self.tail:
                self.tail = node_insert
        self.size += 1

    def append(self, val):
        node_append = Node(val=val)
        node_tail = self.tail
        if self.size == 0:
            self.head = self.tail = node_append
        else:
            node_tail.next = node_append
            node_append.prev = node_tail
            self.tail = node_append
        self.size += 1

    def remove_at(self, idx):
        node_remove = self.visit(idx=idx)
        node_prev, node_next = node_remove.prev, node_remove.next
        if node_prev is None and node_next is None:
            self.head = self.tail = None
        elif node_prev is None:
            node_next.prev = None
            self.head = node_next
        elif node_next is None:
            node_prev.next = None
            self.tail = node_prev
        else:
            node_prev.next = node_next
            node_next.prev = node_prev
        self.size -= 1
        return node_remove.val

    def delete(self, val):
        node_delete = self.search(val=val)
        node_prev, node_next = node_delete.prev, node_delete.next
        if node_prev is None and node_next is None:
            self.head = self.tail = None
        elif node_prev is None:
            node_next.prev = None
            self.head = node_next
        elif node_next is None:
            node_prev.next = None
            self.tail = node_prev
        else:
            node_prev.next = node_next
            node_next.prev = node_prev
        self.size -= 1
        return node_delete.val

    def pop(self):
        node_tail = self.tail
        if node_tail is None:
            raise ValueError(f'Object doesn\'t exist!')
        node_prev = node_tail.prev
        if node_prev is None:
            self.head = self.tail = None
        else:
            node_prev.next = None
            self.tail = node_prev
        self.size -= 1
        return node_tail.val

    def __str__(self):
        ret = []
        node_curr = self.head
        while node_curr is not None:
            ret.append(str(node_curr.val))
            node_curr = node_curr.next
        return 'Size: ' + str(self.size) + '|  ' + ' '.join(ret)


lst = DoublyLinkedList()
lst.append(1)
lst.append(2)
lst.append(3)
lst.append(4)
lst.append(5)
lst.insert_at(0, 0)
print(lst)
lst.insert_at(6, 6)
print(lst)
lst.remove_at(0)
print(lst)
lst.remove_at(0)
print(lst)
lst.remove_at(0)
print(lst)
lst.remove_at(0)
print(lst)
lst.remove_at(0)
print(lst)
lst.delete(6)
print(lst)
lst.pop()
print(lst)

