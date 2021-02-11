import collections

class Node:
    def __init__(self, key, val, prev):
        self.key = key
        self.val = val
        self.prev = prev

    def __str__(self):
        return self.val


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

    def insert(self, key, val, prev=None):
        node_insert = Node(key, val, prev)
        self.heap.append(node_insert)
        self.size += 1
        self.hash_table[val] = self.size - 1
        self._bubble_up(self.size - 1)

    def extract_min(self):
        if self.size <= 0:
            raise ValueError('No value to extract.')
        else:
            self._swap_node(self.size-1, 0)
            node_extracted = self.heap.pop()
            self.size -= 1
            self.hash_table.pop(node_extracted.val)
            self._bubble_down(0)
            return node_extracted

    def update_key(self, key_updated, val, prev=None):
        idx_current = self._search_idx(val)
        assert idx_current is not None

        key_original = self.heap[idx_current].key
        prev_original = self.heap[idx_current].prev
        self._swap_node(idx_current, self.size - 1)
        self.heap.pop()
        self.size -= 1
        self._bubble_down(idx_current)

        key_updated = min(key_original, key_updated)
        val_updated = prev_original if key_original < key_updated else prev
        self.insert(key_updated, val, val_updated)

    def print_current_status(self):
        print(f'Current Heap status : {[(i.key, i.val) for i in self.heap]}')


class Graph:
    def __init__(self):
        self.graph_dict = collections.defaultdict(list)
        self.vertices = set()

    def convert_adjacency_lst_to_dict(self, weighted_graph):
        for weight, start, end in weighted_graph:
            self.vertices.update([start, end])
            self.graph_dict[start].append((weight, end))
            self.graph_dict[end].append((weight, start))

    def get_minimum_spanning_tree(self):
        adjacency_lst = []
        total_weight = 0
        heap = Heap()
        start_vertex = None
        explored = set()
        for vertex in self.vertices:
            heap.insert(key=float('inf'), val=vertex)

        while heap.size != 0:
            node_smallest_weight = heap.extract_min()
            explored.add(node_smallest_weight.val)
            for weight, neighbor in self.graph_dict[node_smallest_weight.val]:
                if neighbor not in explored:
                    heap.update_key(key_updated=weight, val=neighbor, prev=node_smallest_weight.val)
            if start_vertex is None:
                start_vertex = node_smallest_weight.val
            else:
                adjacency_lst.append((node_smallest_weight.key, node_smallest_weight.prev, node_smallest_weight.val))
                total_weight += node_smallest_weight.key
        return (total_weight, adjacency_lst)


graph = [
    (7, 'A', 'B'), (5, 'A', 'D'),
    (8, 'B', 'C'), (9, 'B', 'D'), (7, 'B', 'E'),
    (5, 'C', 'E'), (7, 'D', 'E'), (6, 'D', 'F'),
    (8, 'E', 'F'), (9, 'E', 'G'), (11, 'F', 'G')
]

g = Graph()
g.convert_adjacency_lst_to_dict(graph)
print(g.get_minimum_spanning_tree())