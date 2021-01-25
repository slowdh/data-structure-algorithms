from algorithm_stanford.doubly_linked_list import DoublyLinkedList

# Linked list implementation
class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.hash_array = [DoublyLinkedList() for _ in range(capacity)]

    def _hash_function(self, key):
        return hash(key) % self.capacity

    def insert(self, key):
        idx = self._hash_function(key=key)
        self.hash_array[idx].append(val=key)

    def delete(self, key):
        idx = self._hash_function(key=key)
        self.hash_array[idx].delete(val=key)

    def is_in(self, key):
        idx = self._hash_function(key=key)
        try:
            self.hash_array[idx].search(val=key)
        except ValueError:
            return False
        return True

ht = HashTable(capacity=123)
ht.insert(1)
ht.insert(2)
ht.insert(13)
ht.insert(14)
ht.insert(25)
print(ht.is_in(4))
print(ht.is_in(25))
ht.delete(25)
print(ht.is_in(25))




