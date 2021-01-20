class RedBlackNode:
    def __init__(self, val, color='red', left=None, right=None, parent=None):
        self.val, self.color, self.left, self.right, self.parent = val, color, left, right, parent


class RedBlackTree:
    """
    Red-Black-Tree guarantees that tree's height is always theta(log(n))
    """

    def __init__(self):
        self.root = None

    def _search_helper(self, val, root):
        if root is None:
            raise ValueError(f'Node with value ({val}) doesn\'t exist.')
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
                self._restore_rbt_property_after_insertion(node=node_insert)
            else:
                self._insert_helper(node_insert=node_insert, root=root.right)
        else:
            if root.left is None:
                root.left = node_insert
                node_insert.parent = root
                self._restore_rbt_property_after_insertion(node=node_insert)
            else:
                self._insert_helper(node_insert=node_insert, root=root.left)

    def _match_parent_reference(self, node_prev, node_curr):
        # transfer node_prev and parent reference to node_curr
        node_parent = node_prev.parent
        if node_parent is None:
            self.root = node_curr
        else:
            if node_parent.left == node_prev:
                node_parent.left = node_curr
            else:
                node_parent.right = node_curr
        if node_curr is not None:
            node_curr.parent = node_parent
        node_prev.parent = None

    def _rotate_left(self, node):
        # node.right becomes a new root of a subtree
        node_child = node.right
        assert node_child is not None, 'Rotation not possible: Child node doesn\'t exist.'
        node.right = node_child.left
        if node_child.left is not None:
            node_child.left.parent = node
        node_child.left = node
        self._match_parent_reference(node_prev=node, node_curr=node_child)
        node.parent = node_child

    def _rotate_right(self, node):
        # node.left becomes a new root of a subtree
        node_child = node.left
        assert node_child is not None, 'Rotation not possible: Child node doesn\'t exist.'
        node.left = node_child.right
        if node_child.right is not None:
            node_child.right.parent = node
        node_child.right = node
        self._match_parent_reference(node_prev=node, node_curr=node_child)
        node.parent = node_child

    def _restore_rbt_property_after_insertion(self, node):
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
                    self._restore_rbt_property_after_insertion(node=node_parent)
            elif node_grandparent.right == node_parent:
                if node_parent.right == node:
                    self._rotate_left(node=node_grandparent)
                    node_grandparent.color = 'red'
                    node_parent.color = 'black'
                else:
                    self._rotate_right(node=node_parent)
                    self._restore_rbt_property_after_insertion(node=node_parent)
        else:
            assert node_uncle.color == 'red'
            node_grandparent.color = 'red'
            node_parent.color = node_uncle.color = 'black'
            self._restore_rbt_property_after_insertion(node=node_grandparent)

    def _delete_helper(self, node_delete):
        if node_delete.left is not None and node_delete.right is not None:
            node_max = self._get_maximum_node_under_sub_tree(root=node_delete.left)
            node_delete.val, node_max.val = node_max.val, node_delete.val
            self._delete_helper(node_delete=node_max)
        else:
            # at least one of children is None
            node_parent = node_delete.parent
            node_child = node_delete.left if node_delete.right is None else node_delete.right
            self._match_parent_reference(node_prev=node_delete, node_curr=node_child)
            if node_child is None:
                return
            if node_delete.color == 'black':
                if node_child is None or node_child.color == 'black':
                    self._restore_rbt_property_after_deletion(node=node_child, node_parent=node_parent)
                else:
                    assert node_child.color == 'red'
                    node_child.color = 'black'

    def delete(self, val):
        node_delete = self.search(val=val)
        self._delete_helper(node_delete=node_delete)

    def _restore_rbt_property_after_deletion(self, node, node_parent):
        if node_parent is None:
            node.color = 'black'
            return
        node_sibling = node_parent.left if node_parent.right == node else node_parent.right
        assert node_sibling is not None
        if node_sibling.color == 'red':
            if node_parent.right == node_sibling:
                self._rotate_left(node=node_parent)
            else:
                self._rotate_right(node=node_parent)
            node_parent.color = 'red'
            node_sibling.color = 'black'
            self._restore_rbt_property_after_deletion(node=node, node_parent=node_parent)
        else:
            # node_sibling.color == 'black'
            if node_parent.color == 'red' and (node_sibling.left is None or node_sibling.left.color == 'black') and (node_sibling.right is None or node_sibling.right.color == 'black'):
                node_parent.color = 'black'
                node_sibling.color = 'red'
            elif node_parent.color == 'black' and (node_sibling.left is None or node_sibling.left.color == 'black') and (node_sibling.right is None or node_sibling.right.color == 'black'):
                node_sibling.color = 'red'
                self._restore_rbt_property_after_deletion(node=node_parent, node_parent=node_parent.parent)
            else:
                if node_parent.right == node_sibling:
                    if node_sibling.right.color == 'red':
                        self._rotate_left(node=node_parent)
                        node_parent.color, node_sibling.color = node_sibling.color, node_parent.color
                        node_sibling.right.color = 'black'
                    else:
                        self._rotate_right(node=node_sibling)
                        node_sibling.left.color, node_sibling.color = node_sibling.color, node_sibling.left.color
                        self._restore_rbt_property_after_deletion(node=node, node_parent=node_parent)
                else:
                    if node_sibling.left.color == 'red':
                        self._rotate_right(node=node_parent)
                        node_parent.color, node_sibling.color = node_sibling.color, node_parent.color
                        node_sibling.right.color = 'black'
                    else:
                        self._rotate_left(node=node_sibling)
                        node_sibling.right.color, node_sibling.color = node_sibling.color, node_sibling.right.color
                        self._restore_rbt_property_after_deletion(node=node, node_parent=node_parent)

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

    def _get_maximum_node_under_sub_tree(self, root):
        if root.right is None:
            return root
        return self._get_maximum_node_under_sub_tree(root.right)

    def search(self, val):
        if self.root is None:
            raise ValueError(f'Node with value ({val}) doesn\'t exist.')
        else:
            return self._search_helper(val=val, root=self.root)

    def get_maximum_node(self):
        if self.root is None:
            return None
        return self._get_maximum_node_under_sub_tree(root=self.root)

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
bst.delete(18)
bst.delete(8)
bst.delete(5)
bst.delete(15)
bst.delete(7)
bst.delete(6)
bst.delete(4)
bst.delete(25)
bst.delete(40)
bst.delete(17)
print(bst.level_order_traversal_with_color())
