class RedBlackNode:
    def __init__(self, val, color='red', left=None, right=None, parent=None):
        self.val, self.color, self.left, self.right, self.parent = val, color, left, right, parent


class RedBlackTree:
    """
    Red-Black-Tree guarantees that tree's height is upper bounded by O(log(n))
    """

    def __init__(self):
        self.root = None

    def _search_helper(self, val, root):
        if root is None:
            return None
        if root.val == val:
            return root
        elif root.val < val:
            return self._search_helper(val=val, root=root.right)
        else:
            return self._search_helper(val=val, root=root.left)

    def _insert_helper(self, node_insert, root):
        if root.val < node_insert.val:
            if root.right is None:
                root.right = node_insert
                node_insert.parent = root
                self._restore_rbt_property(node=node_insert)
            else:
                self._insert_helper(node_insert=node_insert, root=root.right)
        else:
            if root.left is None:
                root.left = node_insert
                node_insert.parent = root
                self._restore_rbt_property(node=node_insert)
            else:
                self._insert_helper(node_insert=node_insert, root=root.left)

    def _match_parent_reference(self, node_prev, node_curr):
        if node_curr.parent is None:
            self.root = node_curr
            node_curr.parent = None
            return
        node_parent = node_curr.parent
        if node_parent.left == node_prev:
            node_parent.left = node_curr
        else:
            node_parent.right = node_curr

    def _rotate_left(self, node):
        # node.right becomes a new root of a subtree
        node_child = node.right
        assert node_child is not None, 'Rotation not possible: Child node doesn\'t exist.'
        node.right = node_child.left
        if node_child.left is not None:
            node_child.left.parent = node
        node_child.left = node
        node_child.parent = node.parent
        node.parent = node_child
        self._match_parent_reference(node_prev=node, node_curr=node_child)
        return node_child

    def _rotate_right(self, node):
        # node.left becomes a new root of a subtree
        node_child = node.left
        assert node_child is not None, 'Rotation not possible: Child node doesn\'t exist.'
        node.left = node_child.right
        if node_child.right is not None:
            node_child.right.parent = node
        node_child.right = node
        node_child.parent = node.parent
        node.parent = node_child
        self._match_parent_reference(node_prev=node, node_curr=node_child)
        return node_child

    def _restore_rbt_property(self, node):
        if node.color == 'black':
            return
        if node.parent is None:
            self.root.color = 'black'
            return
        if node.parent.color == 'black':
            return
        node_parent, node_grandparent, node_uncle = node.parent, node.parent.parent, node.parent.parent.left if node.parent == node.parent.parent.right else node.parent.parent.right
        assert node_parent.color == 'red' and node_grandparent.color == 'black'
        if node_uncle is None or node_uncle.color == 'black':
            if node_grandparent.left == node_parent:
                if node_parent.left == node:
                    self._rotate_right(node=node_grandparent)
                    node_grandparent.color = 'red'
                    node_parent.color = 'black'
                else:
                    self._rotate_left(node=node_parent)
                    self._restore_rbt_property(node=node_parent)
            elif node_grandparent.right == node_parent:
                if node_parent.right == node:
                    self._rotate_left(node=node_grandparent)
                    node_grandparent.color = 'red'
                    node_parent.color = 'black'
                else:
                    self._rotate_right(node=node_parent)
                    self._restore_rbt_property(node=node_parent)
        else:
            assert node_uncle.color == 'red'
            node_grandparent.color = 'red'
            node_parent.color = node_uncle.color = 'black'
            self._restore_rbt_property(node=node_grandparent)

    def _inorder_traversal_under_sub_tree(self, root):
        if root is None:
            return []
        else:
            return self._inorder_traversal_under_sub_tree(root=root.left) + [root.val] + self._inorder_traversal_under_sub_tree(root=root.right)

    def _level_order_traversal_under_sub_tree_with_color(self, root):
        ret = []
        queue = [root]
        while len(queue) != 0:
            level = []
            for i in range(len(queue)):
                node_popped = queue.pop(0)
                level.append((node_popped.val, node_popped.color))
                for child in (node_popped.left, node_popped.right):
                    if child is not None:
                        queue.append(child)
            ret.append(level)
        return ret

    def search(self, val):
        if self.root is None:
            return None
        else:
            return self._search_helper(val=val, root=self.root)

    def insert(self, val):
        node_insert = RedBlackNode(val=val)
        if self.root is None:
            self.root = node_insert
            node_insert.color = 'black'
        else:
            self._insert_helper(node_insert=node_insert, root=self.root)

    def inorder_traversal(self):
        if self.root is None:
            return []
        return self._inorder_traversal_under_sub_tree(root=self.root)

    def level_order_traversal_with_color(self):
        if self.root is None:
            return []
        return self._level_order_traversal_under_sub_tree_with_color(root=self.root)


bst = RedBlackTree()
bst.insert(8)
bst.insert(18)
bst.insert(5)
bst.insert(15)
bst.insert(17)
bst.insert(25)
bst.insert(40)
bst.insert(4)
bst.insert(6)
bst.insert(7)
print(bst.level_order_traversal_with_color())
