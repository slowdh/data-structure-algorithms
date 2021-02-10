class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class Heap:
    def __init__(self):
        self.heap = []
        self.size = 0
        self.hash_table = {}

    def _update_hash(self, val, idx_update):
        self.hash_table[val] = idx_update

    def _swap_node(self, left_idx, right_idx):
        self._update_hash(self.heap[left_idx].val, right_idx)
        self._update_hash(self.heap[right_idx].val, left_idx)
        self.heap[left_idx], self.heap[right_idx] = self.heap[right_idx], self.heap[left_idx]

    def _bubble_up(self, current_idx):
        if current_idx == 0:
            return
        parent_idx = (current_idx - 1) // 2
        if self.heap[parent_idx].key >= self.heap[current_idx].key:
            self._swap_node(current_idx, parent_idx)
            self._bubble_up(parent_idx)

    def _bubble_down(self, current_idx):
        child_left, child_right = current_idx * 2 + 1, current_idx * 2 + 2
        if child_left >= self.size:
            return
        elif child_right >= self.size:
            child_lower = child_left
        else:
            child_lower = child_left if self.heap[child_left].key <= self.heap[child_right].key else child_right

        if self.heap[current_idx].key > self.heap[child_lower].key:
            self._swap_node(current_idx, child_lower)
            self._bubble_down(child_lower)

    def _search_idx(self, val):
        if val in self.hash_table:
            return self.hash_table[val]
        return None

    def insert(self, key, val):
        node_insert = Node(key, val)
        self.hash_table[val] = self.size - 1
        self.heap.append(node_insert)
        self.size += 1
        self._bubble_up(self.size - 1)

    def extract_min(self):
        if self.size <= 0:
            raise ValueError('No value to extract.')
        else:
            self._swap_node(self.size-1, 0)
            node_extracted = self.heap.pop()
            self.size -= 1
            self._bubble_down(0)
            self.hash_table.pop(node_extracted.val)
            return node_extracted

    def update_key(self, key_updated, val):
        idx_current = self._search_idx(val)
        assert idx_current is not None

        key_original = self.heap[idx_current].key
        self._swap_node(idx_current, self.size - 1)
        self.heap.pop()
        self.size -= 1
        self._bubble_down(idx_current)

        key_updated = min(key_original, key_updated)
        self.insert(key_updated, val)

    def print_current_status(self):
        print(f'Current Heap status : {[(i.key, i.val) for i in self.heap]}')



a = Heap()
a.insert(5, 'A')
a.insert(1, 'B')
a.insert(2, 'C')
a.insert(4, 'D')
a.insert(0, 'E')
a.print_current_status()
a.extract_min()
a.print_current_status()
a.extract_min()
a.print_current_status()
a.extract_min()
a.print_current_status()
a.extract_min()
a.print_current_status()
a.extract_min()
a.print_current_status()
