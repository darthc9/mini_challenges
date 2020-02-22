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

    def get_min_key_node(self):
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


def delete_node(root, key):
    """ delete key and return new root of tree """

    # empty tree
    if root is None:
        return root
        
    # smaller key lies in the left subtree
    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        # this is the node with the key to be deleted
        # Node with only one child or no child
        if root.left is None:
            return root.right
        
        elif root.right is None:
            return root.left
            
        # Node with two children - replace node with the inorder successor
        temp = root.right.get_min_key_node()
        
        # Copy the inorder successor's content to this node
        root.key = temp.key
        root.data = temp.data
        
        # Delete the inorder successor
        root.right = delete_node(root.right, temp.key)
    
    return root


class BST(object):
    def __init__(self):
        self.root = None
    
    def insert(self, key, data=0):
        """ add a new node with key and data or find the existing node according to key
            and accumulate (+=) the data in that pre-existing node """
        self.root = insert(self.root, key, data)
    
    def isin(self, key):
        """ return True if key is found in tree, false otherwise """
        if self.root:
            return self.root.isin(key)
        else:
            return False
    
    def find(self, key) -> Node:
        return self.root.find(key)
        
        
    def remove(self, key):
        self.root = delete_node(self.root, key)
    
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