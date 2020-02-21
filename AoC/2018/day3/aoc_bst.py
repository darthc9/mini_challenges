# adapted from https://github.com/stephengrice/education/blob/master/BST/bst.py

# a Binary Search Tree is a structure where the key in the left child is less the the key in the node
# and the key in the right child is bigger than the key in the node


class Node(object):
    def __init__(self, k, d):
        self.key = k
        self.data = d       # the data is separate from the key and can be used as rank in some algorithms
        self.left = None
        self.right = None
        
    def find(self, k):
        """ returns the node with given key or None if not found """
        if self.key == k:
            return self
        elif k < self.key and self.left:
            return self.left.find(k)
        elif k > self.key and self.right:
            return self.right.find(k)
        return None
    
    def isin(self, k):
        """ returns True if the key k is stored in a node in the tree """
        return self.find(k) is not None

    def get_min_key(self):
        """ return the node with minimum key value found in that tree """
        current = self
        
        while current.left is not None:
            current = current.left
        
        return current

    def preorder(self, l):
        """ populate the list l with the (key,data) of a pre-order traversal output of the tree """
        l.append((self.key, self.data))
        if self.left:
            self.left.preorder(l)
        if self.right:
            self.right.preorder(l)
        return l
    
    def postorder(self, l):
        """ populate the list l with the (key, data) of a post-order traversal output of the tree """
        if self.left:
            self.left.postorder(l)
        if self.right:
            self.right.postorder(l)
        l.append((self.key, self.data))
        return l
    
    def inorder(self, l):
        """ populate the list l with the (key,data) of an in-order traversal output of the tree """
        if self.left:
            self.left.inorder(l)
        l.append((self.key, self.data))
        if self.right:
            self.right.inorder(l)
        return l


def insert(node, key, data):
    """ A utility function to insert a new node with given key in BST,
        for existing keys accumulate the data rather than replace it. returns root """
    
    # If the tree is empty, return a new node
    if node is None:
        return Node(key, data)
        
    if node.key == key:
        node.data += data  # accumulate data rather than replace it.
    
    # otherwise find a place to insert new node down the tree
    elif key < node.key:
        node.left = insert(node.left, key, data)
    else:
        node.right = insert(node.right, key, data)
        
    return node


class BST(object):
    def __init__(self):
        self.root = None
    
    def insert(self, key, data):
        """ add a new node with key and data or find the existing node according to key
            and accumulate (+=) the data in that pre-existing node """
        self.root = insert(self.root, key, data)
    
    def isin(self, key):
        """ return True if key is found in tree, false otherwise """
        if self.root:
            return self.root.isin(key)
        else:
            return False
    
    def remove(self, k):
        """ remove a node with a given key k from the tree.
            returns True if node was present """
        
        # Case 1: Empty Tree?
        if self.root is None:
            return False
        
        # Case 2: Deleting root node
        if self.root.key == k:
            # Case 2.1: Root node has no children
            if self.root.left is None and self.root.right is None:
                self.root = None
                return True
            # Case 2.2: Root node has left child
            elif self.root.left and self.root.right is None:
                self.root = self.root.left
                return True
            # Case 2.3: Root node has right child
            elif self.root.left is None and self.root.right:
                self.root = self.root.right
                return True
            # Case 2.4: Root node has two children
            else:
                moveNode = self.root.right
                moveNodeParent = None
                while moveNode.left:
                    moveNodeParent = moveNode
                    moveNode = moveNode.left
                self.root.key = moveNode.key
                if moveNode.key < moveNodeParent.key:
                    moveNodeParent.left = None
                else:
                    moveNodeParent.right = None
                return True
        # Find node to remove
        parent = None
        node = self.root
        while node and node.key != k:
            parent = node
            if k < node.key:
                node = node.left
            elif k > node.key:
                node = node.right
        # Case 3: Node not found
        if node is None or node.key != k:
            return False
        # Case 4: Node has no children
        elif node.left is None and node.right is None:
            if k < parent.key:
                parent.left = None
            else:
                parent.right = None
            return True
        # Case 5: Node has left child only
        elif node.left and node.right is None:
            if k < parent.key:
                parent.left = node.left
            else:
                parent.right = node.left
            return True
        # Case 6: Node has right child only
        elif node.left is None and node.right:
            if k < parent.key:
                parent.left = node.right
            else:
                parent.right = node.right
            return True
        # Case 7: Node has left and right child
        else:
            moveNodeParent = node
            moveNode = node.right
            while moveNode.left:
                moveNodeParent = moveNode
                moveNode = moveNode.left
            node.key = moveNode.key
            if moveNode.right:
                if moveNode.key < moveNodeParent.key:
                    moveNodeParent.left = moveNode.right
                else:
                    moveNodeParent.right = moveNode.right
            else:
                if moveNode.key < moveNodeParent.key:
                    moveNodeParent.left = None
                else:
                    moveNodeParent.right = None
            return True
    
    # return list of data elements resulting from preorder tree traversal
    def preorder(self):
        if self.root:
            return self.root.preorder([])
        else:
            return []
    
    # return list of postorder elements
    def postorder(self):
        if self.root:
            return self.root.postorder([])
        else:
            return []
    
    # return list of inorder elements
    def inorder(self):
        if self.root:
            return self.root.inorder([])
        else:
            return []