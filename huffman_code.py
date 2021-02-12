import collections

class Node:
    def __init__(self, key, val, left=None, right=None):
        self.key = key
        self.val = val
        self.left = left
        self.right = right


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

    def insert_node(self, node_insert):
        self.heap.append(node_insert)
        self.size += 1
        self.hash_table[node_insert.val] = self.size - 1
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


class HuffmanCode:
    def __init__(self, char_str=None):
        self.char_str = char_str
        self.freq_dict = None
        self.tree_root = None
        self.code_dict = {}

    def _set_char_str(self, char_str):
        self.char_str = char_str

    def _set_frequency(self):
        freq_dict = collections.defaultdict(int)
        for c in self.char_str:
            freq_dict[c] += 1
        self.freq_dict = freq_dict

    def _compute_huffman_tree(self):
        heap = Heap()
        for char, freq in self.freq_dict.items():
            node = Node(key=freq, val=char)
            heap.insert_node(node_insert=node)

        while heap.size >= 2:
            left, right = heap.extract_min(), heap.extract_min()
            node_merged = Node(key=left.key+right.key, val=left.val+right.val, left=left, right=right)
            heap.insert_node(node_insert=node_merged)
        self.tree_root = node_merged
        self._generate_code(root=self.tree_root)
        return node_merged

    def _generate_code(self, root, prev=''):
        if root is None:
            return
        if root.left is None and root.right is None:
            self.code_dict[root.val] = prev
        self._generate_code(root.left, prev + '0')
        self._generate_code(root.right, prev + '1')

    def encode(self, string):
        self._set_char_str(char_str=string)
        self._set_frequency()
        self._compute_huffman_tree()
        self._generate_code(root=self.tree_root)

        ret = ''
        for c in self.char_str:
            ret += self.code_dict[c]
        return ret

    def decode(self, encoding):
        ret = ''
        node_curr = self.tree_root
        for i in encoding:
            if i == '0':
                node_curr = node_curr.left
            else:
                node_curr = node_curr.right
            if node_curr.left is None and node_curr.right is None:
                ret += node_curr.val
                node_curr = self.tree_root
        return ret


a = HuffmanCode()
print(a.encode('AASDASNFNKASDNKJWKQEJNKSDNKJASNDNAKSDAS'))
print(a.decode('1101100110011001001111000010111001100001011110111101101111111111110111000101011000010111101100100100001101010110011001'))
print('AASDASNFNKASDNKJWKQEJNKSDNKJASNDNAKSDAS' == a.decode('1101100110011001001111000010111001100001011110111101101111111111110111000101011000010111101100100100001101010110011001'))
