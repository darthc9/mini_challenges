import unittest
from day_three_bst import calculate_requested_area_for_bst


class TestBST(unittest.TestCase):
    def setUp(self):
        pass

    def test_calculate_requested_area_for_bst(self):
        ordered_list_5_cells = [(0, 1), (5, 1), (10, -1), (15, -1)]
        ordered_list_0_cells = [(0, 1), (15, -1)]
        ordered_list_5_cells_2 = [(0, 1), (5, 1), (6, 1), (8, -1), (10, -1), (15, -1)]
        
        self.assertEqual(5, calculate_requested_area_for_bst(ordered_list_5_cells))
        self.assertEqual(0, calculate_requested_area_for_bst(ordered_list_0_cells))
        self.assertEqual(5, calculate_requested_area_for_bst(ordered_list_5_cells_2))
