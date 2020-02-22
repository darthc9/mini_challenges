import unittest
from aoc_bst import BST


class TestBST(unittest.TestCase):
    def setUp(self):
        self.bst = BST()
    
    def test_insert(self):
        self.assertEqual([], self.bst.inorder())
        self.bst.insert(5, 0)
        self.assertEqual([(5, 0)], self.bst.inorder())
        self.bst.insert(4, 0)
        self.assertEqual([(4, 0), (5, 0)], self.bst.inorder())
        self.bst.insert(7, 0)
        self.assertEqual([(4, 0), (5, 0), (7, 0)], self.bst.inorder())

    def test_remove(self):
        """
                       50
                  30        70
               20   40    60   80
        """
        self.bst.insert(50, 0)
        self.bst.insert(30, 0)
        self.bst.insert(20, 0)
        self.bst.insert(40, 0)
        self.bst.insert(70, 0)
        self.bst.insert(60, 0)
        self.bst.insert(80, 0)
        self.assertEqual([(20, 0), (30, 0), (40, 0), (50, 0), (60, 0), (70, 0), (80, 0)], self.bst.inorder())
        
        # remove leaf
        self.bst.remove(20)
        self.assertEqual([(30, 0), (40, 0), (50, 0), (60, 0), (70, 0), (80, 0)], self.bst.inorder())
        
        # remove node with one child
        self.bst.remove(30)
        # remove non existent node (no effect)
        self.bst.remove(20)
        self.assertEqual([(40, 0), (50, 0), (60, 0), (70, 0), (80, 0)], self.bst.inorder())
        
        # remove root node with 2 children
        self.bst.remove(50)
        self.assertEqual([(40, 0), (60, 0), (70, 0), (80, 0)], self.bst.inorder())

    def test_remove_data(self):
        self.bst.insert(50, 1)
        self.bst.insert(30, 1)
        self.bst.insert(20, 1)
        self.bst.insert(40, 1)
        self.bst.insert(70, 1)
        self.bst.insert(60, 1)
        self.bst.insert(80, 1)
        # add 1 to the rank of node 60
        self.bst.insert(60, 1)
        self.assertEqual([(20, 1), (30, 1), (40, 1), (50, 1), (60, 2), (70, 1), (80, 1)], self.bst.inorder())
        # decrement one from the rank of node 50
        self.bst.insert(50, -1)
        self.assertEqual([(20, 1), (30, 1), (40, 1), (50, 0), (60, 2), (70, 1), (80, 1)], self.bst.inorder())
        # if node 50 has rank of 0 delete it.
        n = self.bst.find(50)
        if n and n.data == 0:
            self.bst.remove(50)
        self.assertEqual([(20, 1), (30, 1), (40, 1), (60, 2), (70, 1), (80, 1)], self.bst.inorder())

    def test_original_tests(self):
        """ these were the tests for the original version of the BST """
        # 2.1 Leaf node
        self.bst.insert(5)
        self.bst.remove(5)
        self.assertEqual([], self.bst.inorder())

        # 2.2 Left child only
        self.bst.insert(5)
        self.bst.insert(4)
        self.bst.insert(3)
        self.assertEqual(5, self.bst.root.key)
        self.assertEqual([(3,0), (4,0), (5,0)], self.bst.inorder())
        self.bst.remove(5)
        self.assertEqual([(3,0), (4,0)], self.bst.inorder())
        self.assertEqual(4, self.bst.root.key)  # works as expected but is that the best test?
        # i mean, it should test correctness rather than functionality IMO!
        # reset tree:
        self.bst.remove(3)
        self.bst.remove(4)
        self.assertEqual([], self.bst.inorder())

        # 2.3 Right child only
        self.bst.insert(5)
        self.bst.insert(7)
        self.bst.insert(6)
        self.assertEqual(5, self.bst.root.key)
        self.assertEqual([(5,0), (6,0), (7,0)], self.bst.inorder())
        self.bst.remove(5)
        self.assertEqual([(6,0), (7,0)], self.bst.inorder())
        self.assertEqual(7, self.bst.root.key)
        # reset tree:
        self.bst.remove(6)
        self.bst.remove(7)
        self.assertEqual([], self.bst.inorder())

        # 2.4 root with both children
        self.bst.insert(5)
        self.bst.insert(4)
        self.bst.insert(8)
        self.bst.insert(7)
        self.bst.insert(6)
        self.assertEqual(5, self.bst.root.key)
        self.assertEqual([(4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], self.bst.inorder())
        self.bst.remove(5)
        self.assertEqual([(4, 0), (6, 0), (7, 0), (8, 0)], self.bst.inorder())
        self.assertEqual(6, self.bst.root.key)
        # reset tree:
        self.bst.remove(4)
        self.bst.remove(8)
        self.bst.remove(6)
        self.bst.remove(7)
        self.assertEqual([], self.bst.inorder())

        # Node has left child only
        self.bst.insert(5)
        self.bst.insert(4)
        self.bst.insert(8)
        self.bst.insert(7)
        self.bst.insert(6)
        self.bst.remove(8)
        self.assertEqual([(4, 0), (5, 0), (6, 0), (7, 0)], self.bst.inorder())
        self.assertEqual(7, self.bst.root.right.key)

        # Node has right child only
        self.bst = BST()
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(4)
        self.bst.remove(3)
        self.assertEqual([(4, 0), (5, 0)], self.bst.inorder())
        self.assertEqual(4, self.bst.root.left.key)

        # Node has left and right child
        self.bst = BST()
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(4)
        self.bst.insert(1)
        self.bst.remove(3)
        self.assertEqual([(1, 0),(4, 0), (5, 0)], self.bst.inorder())
        self.assertEqual(4, self.bst.root.left.key)
