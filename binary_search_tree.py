class TreeNode:
    def __init__(self, val, left=None, right=None, parent=None):
        self.val, self.left, self.right, self.parent = val, left, right, parent


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, val, root=None, node_insert=None):
        if node_insert is None:
            node_insert = TreeNode(val=val)
        if self.root is None:
            self.root = node_insert
            return
        if root is None:
            root = self.root

        if root.val < val:
            if root.right is None:
                root.right = node_insert
                node_insert.parent = root
            else:
                self.insert(val=val, root=root.right, node_insert=node_insert)
        else:
            if root.left is None:
                root.left = node_insert
                node_insert.parent = root
            else:
                self.insert(val=val, root=root.left, node_insert=node_insert)

    ### This implementation can handle case when self.root is None ###
    def insert2(self, val):
        node_insert = TreeNode(val=val)
        if self.root is None:
            self.root = node_insert
        else:
            self._insert_under_sub_tree(root=self.root, node_insert=node_insert)

    def _insert_under_sub_tree(self, root, node_insert):
        if root.val <= node_insert.val:
            if root.right is None:
                root.right = node_insert
                node_insert.parent = root
            else:
                self._insert_under_sub_tree(root.right, node_insert)
        else:
            if root.left is None:
                root.left = node_insert
                node_insert.parent = root
            else:
                self._insert_under_sub_tree(root.left, node_insert)

    def search(self, val, root=None):
        if root is None:
            root = self.root
        if root.val == val:
            return root
        elif root.val < val:
            if root.right is not None:
                return self.search(val, root=root.right)
            else:
                return None
        else:
            if root.left is not None:
                return self.search(val, root=root.left)
            else:
                return None

    def delete(self, val):
        node_delete = self.search(val)
        node_parent = node_delete.parent
        if node_delete.left is None and node_delete.right is None:
            if node_parent is None:
                self.root = None
            else:
                if node_parent.left == node_delete:
                    node_parent.left = None
                else:
                    node_parent.right = None
        elif node_delete.left is None:
            node_child = node_delete.right
            if node_parent is None:
                node_child.parent = None
                self.root = node_child
            else:
                if node_parent.left == node_delete:
                    node_parent.left = node_child
                    node_child.parent = node_parent
        elif node_delete.right is None:
            node_child = node_delete.left
            if node_parent is None:
                node_child.parent = None
                self.root = node_child
            else:
                if node_parent.right == node_delete:
                    node_parent.right = node_child
                    node_child.parent = node_parent
                else:
                    node_parent.left = node_child
                    node_child.parent = node_parent
        else:
            max_val = self.get_maximum_node(node_delete.left).val
            self.delete(max_val)
            node_delete.val = max_val

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

    def get_minimum_node(self, root=None):
        if root is None:
            root = self.root
        if root.left is None:
            return root
        else:
            return self.get_minimum_node(root=root.left)

    def get_maximum_node(self, root=None):
        if root is None:
            root = self.root
        if root.right is None:
            return root
        else:
            return self.get_maximum_node(root=root.right)


tree = BinarySearchTree()
tree.insert2(3)
print(tree.inorder_traversal())
tree.insert2(4)
print(tree.inorder_traversal())
tree.insert2(2)
print(tree.inorder_traversal())
tree.insert2(100)
print(tree.inorder_traversal())
tree.insert2(1)
print(tree.inorder_traversal())
tree.insert2(5)
print(tree.inorder_traversal())
print(tree.get_minimum_node().val)

tree.delete(2)
print(tree.inorder_traversal())
tree.delete(3)
print(tree.inorder_traversal())
tree.delete(1)
print(tree.inorder_traversal())
tree.delete(4)
print(tree.inorder_traversal())
tree.delete(5)
print(tree.inorder_traversal())
tree.delete(100)
print(tree.inorder_traversal())