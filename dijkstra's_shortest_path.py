class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class Heap:
    def __init__(self):
        self.heap = []
        self.size = 0

    def _swap_node(self, left_idx, right_idx):
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
        # If you use Hash table along with Heap, Search operation could be done in O(1) time complexity.
        for idx, node in enumerate(self.heap):
            if node.val == val:
                return idx
        return None

    def insert(self, key, val=0):
        node_insert = Node(key, val)
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
            return node_extracted

    def update_key(self, val, new_len):
        idx_update = self._search_idx(val)
        assert idx_update is not None

        original_len = self.heap[idx_update].key
        self._swap_node(idx_update, self.size - 1)
        self.heap.pop()
        self.size -= 1
        self._bubble_down(idx_update)

        len_updated = min(original_len, new_len)
        self.insert(len_updated, val)

    def print_current_status(self):
        print(f'Current Heap status : {[(i.key, i.val) for i in self.heap]}')


class Graph:
    def __init__(self):
        self.node_dict = {}
        self.shortest_path = {}

    def print_status(self):
        print(f'Current weighted node dictionary status : {self.node_dict}')

    def print_shortest_path(self):
        print(f'Dijkstra\'s shortest path : {self.shortest_path}')

    def convert_adjacency_list_to_dict(self, adjacency_list):
        for start, end, weight in adjacency_list:
            if start not in self.node_dict:
                self.node_dict[start] = [(end, weight)]
            else:
                self.node_dict[start].append((end, weight))
        return self.node_dict

    def get_dijkstras_shortest_path(self, start_node, nodes):
        heap_arr = Heap()
        for node in nodes:
            if node != start_node:
                heap_arr.insert(float('inf'), node)
            else:
                heap_arr.insert(0, node)

        while heap_arr.size != 0:
            node_extracted = heap_arr.extract_min()
            current_shortest_len = node_extracted.key
            self.shortest_path[node_extracted.val] = current_shortest_len
            if node_extracted.val in self.node_dict:
                for node_end, weight in self.node_dict[node_extracted.val]:
                    new_len = current_shortest_len + weight
                    heap_arr.update_key(node_end, new_len)
        return self.shortest_path


# # Test case_graph
# graph_with_weight = [( 'a' , 'f',  14),
#         ( 'a' , 'c',   9),
#         ( 'a' , 'b',   7),
#         ( 'c' , 'd',  11),
#         ( 'b' , 'c',  10),
#         ( 'd' , 'e',   6),
#         ( 'f' , 'e',   9)
#         ]

# # Heap structure test case
# a = Heap()
# a.insert(5)
# a.insert(1)
# a.insert(2)
# a.insert(4)
# a.insert(0)
# a.print_current_status()
# a.extract_min()
# a.print_current_status()
# a.extract_min()
# a.print_current_status()
# a.extract_min()
# a.print_current_status()
# a.extract_min()
# a.print_current_status()
# a.extract_min()
# a.print_current_status()

# # Shortest path alogorithm test case
# graph = Graph()
# graph.convert_adjacency_list_to_dict(graph_with_weight)
# graph.get_dijkstras_shortest_path('a', 'abcdef')
# graph.print_shortest_path()