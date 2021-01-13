class TreeNode:
    def __init__(self, val, left=None, right=None, parent=None):
        self.val, self.left, self.right, self.parent = val, left, right, parent


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        node_insert = TreeNode(val=val)
        if self.root is None:
            self.root = node_insert
        else:
            self._insert_under_sub_tree(node_insert=node_insert, root=self.root)

    def _insert_under_sub_tree(self, node_insert, root):
        if root.val <= node_insert.val:
            if root.right is None:
                root.right = node_insert
                node_insert.parent = root
            else:
                self._insert_under_sub_tree(node_insert=node_insert, root=root.right)
        else:
            if root.left is None:
                root.left = node_insert
                node_insert.parent = root
            else:
                self._insert_under_sub_tree(node_insert=node_insert, root=root.left)

    def search(self, val):
        if self.root is None:
            raise ValueError(f'Node with value ({val}) doesn\'t exist.')
        else:
            return self._search_under_sub_tree(val, self.root)

    def _search_under_sub_tree(self, val, root):
        if root is None:
            raise ValueError(f'Node with value ({val}) doesn\'t exist.')
        if root.val == val:
            return root
        elif root.val < val:
            return self._search_under_sub_tree(val=val, root=root.right)
        else:
            return self._search_under_sub_tree(val=val, root=root.left)

    def delete(self, val):
        node_delete = self.search(val=val)
        new_root = self._get_new_root_after_delete(node_delete=node_delete)
        self._modify_parent_reference(root_before_delete=node_delete, root_after_delete=new_root)
        if self.root == node_delete:
            self.root = new_root
        return node_delete.val

    def _get_new_root_after_delete(self, node_delete):
        if node_delete.left is not None and node_delete.right is not None:
            node_max = self._get_maximum_node_under_sub_tree(node_delete.left)
            node_delete.val = node_max.val
            root_new_for_node_max = self._get_new_root_after_delete(node_delete=node_max)
            self._modify_parent_reference(root_before_delete=node_max, root_after_delete=root_new_for_node_max)
            new_root = node_delete
        else:
            node_child = node_delete.left if node_delete.right is None else node_delete.right
            new_root = node_child
        return new_root

    def _modify_parent_reference(self, root_before_delete, root_after_delete):
        node_parent = root_before_delete.parent
        if node_parent is not None:
            if node_parent.left == root_before_delete:
                node_parent.left = root_after_delete
            else:
                node_parent.right = root_after_delete
        if root_after_delete is not None:
            root_after_delete.parent = node_parent

    def _delete_under_sub_tree(self, node_delete):
        node_parent = node_delete.parent
        if node_delete.left is None and node_delete.right is None:
            if node_parent.left == node_delete:
                node_parent.left = None
            else:
                node_parent.right = None
        elif node_delete.left is None or node_delete.right is None:
            node_child = node_delete.left if node_delete.right is None else node_delete.right
            if node_parent.left == node_delete:
                node_parent.left = node_child
                node_child.parent = node_parent
            else:
                node_parent.right = node_child
                node_child.parent = node_parent
        else:
            node_max = self._get_maximum_node_under_sub_tree(root=node_delete.left)
            node_delete.val = node_max.val
            self._delete_under_sub_tree(node_delete=node_max)

    def inorder_traversal(self):
        if self.root is None:
            return []
        else:
            return self._inorder_traversal_under_sub_tree(root=self.root)

    def _inorder_traversal_under_sub_tree(self, root):
        if root is None:
            return []
        else:
            return self._inorder_traversal_under_sub_tree(root=root.left) + [root.val] + self._inorder_traversal_under_sub_tree(root=root.right)

    def get_minimum_node(self):
        if self.root is None:
            raise ValueError(f'Node doesn\'t exist.')
        else:
            return self._get_minimum_node_under_sub_tree(root=self.root)

    def _get_minimum_node_under_sub_tree(self, root):
        if root.left is None:
            return root
        return self._get_minimum_node_under_sub_tree(root=root.left)

    def get_maximum_node(self):
        if self.root is None:
            raise ValueError(f'Node doesn\'t exist.')
        else:
            return self._get_maximum_node_under_sub_tree(root=self.root)

    def _get_maximum_node_under_sub_tree(self, root):
        if root.right is None:
            return root
        return self._get_maximum_node_under_sub_tree(root=root.right)

    def get_predecessor(self, val):
        current_node = self.search(val=val)
        if current_node.left is not None:
            return self._get_maximum_node_under_sub_tree(root=current_node.left).val
        return self._get_predecessor_under_sub_tree(val=val, current_node=current_node)

    def _get_predecessor_under_sub_tree(self, val, current_node):
        node_parent = current_node.parent
        if node_parent is None:
            return None
        if node_parent.val < val:
            return node_parent.val
        return self._get_predecessor_under_sub_tree(val=val, current_node=node_parent)

    def get_successor(self, val):
        current_node = self.search(val=val)
        if current_node.right is not None:
            return self._get_minimum_node_under_sub_tree(root=current_node.right).val
        return self._get_successor_under_sub_tree(val=val, current_node=current_node)

    def _get_successor_under_sub_tree(self, val, current_node):
        node_parent = current_node.parent
        if node_parent is None:
            return None
        if node_parent.val > val:
            return node_parent.val
        return self._get_successor_under_sub_tree(val=val, current_node=node_parent)


# tree = BinarySearchTree()
# tree.insert(3)
# print(tree.inorder_traversal())
# tree.insert(4)
# print(tree.inorder_traversal())
# tree.insert(2)
# print(tree.inorder_traversal())
# tree.insert(100)
# print(tree.inorder_traversal())
# tree.insert(1)
# print(tree.inorder_traversal())
# tree.insert(5)
# print(tree.inorder_traversal())

# print(tree.get_successor(3))
# print(tree.get_successor(4))
# print(tree.get_successor(2))
# print(tree.get_successor(1))
# print(tree.get_successor(100))
# print(tree.get_successor(5))

# tree.delete(2)
# print(tree.inorder_traversal())
# tree.delete(3)
# print(tree.inorder_traversal())
# tree.delete(1)
# print(tree.inorder_traversal())
# tree.delete(4)
# print(tree.inorder_traversal())
# tree.delete(5)
# print(tree.inorder_traversal())
# tree.delete(100)
# print(tree.inorder_traversal())
