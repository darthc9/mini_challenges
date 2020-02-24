"""
Advent of code 2018 - python coding contest
challenge for day 3 - https://adventofcode.com/2018/day/3

solving the same challenge but using BST and PriorityQueue instead of dictionaries
while saving only the endpoints of the square claims rather than all the points they cover
to calculate the requested area I'll use the same trick presented in the solution for
the Oversized Pancake Flipper challenge: https://code.google.com/codejam/contest/3264486/dashboard


the solution outline:
    1. read all the claims into a priority queue of end points sorting by the X coord
    2. scan the claims from left to right (hence the queue) and for each new end point of a square
        - calc area covered by previous BST to accumulator
        - build a BST while the top endpoint of the square has a value of +1 in the tree
        - and the bottom endpoint has the value of -1 (signaling the end of the area covered by square)
        - using in-order traversal over BST calculate area covered by more than one square
          (in this portion of the x-scan - using the same trick from flipper challenge)



overall expected complexity of O(M*log(M)) time where M is the number of claims
and space of O(M)

"""

import re
import heapq
import time
import aoc_bst


class Claim:
    """ Parse a claim string """
    
    def __init__(self, claim_str: str):
        """ turn string into claim object
            '#10 @ 936,278: 13x27'
          =  id    left,top  COLSxROWs
        """
        claim_tokens = filter(None, re.split("[ #@,:x]", claim_str))  # filter = (item for item in iterable if item)
        self.claim_id, self.left_margin, self.top_margin, self.columns_n, self.rows_n = map(int, claim_tokens)
        
    # while the top-left square of the canvas is in (0,0) -
    def top_left_x(self):
        return self.left_margin
   
    def top_left_y(self):
        return self.top_margin

    def bottom_left_x(self):
        return self.left_margin

    def bottom_left_y(self):
        return self.top_margin + self.rows_n - 1

    def top_right_x(self):
        return self.left_margin + self.columns_n - 1
    
    def top_right_y(self):
        return self.top_margin

    def bottom_right_x(self):
        return self.left_margin + self.columns_n - 1
    
    def bottom_right_y(self):
        return self.top_margin + self.rows_n - 1


class Claims:
    """ A Class to parse and iterate over the claims file """
    
    def __init__(self, filename: str):
        self.claimsfilename = filename
        
    def __enter__(self):
        self.claimsfile = open(self.claimsfilename, 'r')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.claimsfile.close()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = next(self.claimsfile)
        return Claim(line)
    

# to mark the points in the priority queue as the start of a square or the end of it:
ADD_POINT = 1
REMOVE_POINT = -1


def read_claims_into_pq(filename: str):
    """ read all the claims into a priority queue (key = X coord of endpoints)
        the queue stores tuples of the form:
        (X coord, start or end of rectangle, (top y coord, bottom y coord))
    """
    squares_endpoints = []
    
    with Claims(filename) as claims:
        for claim in claims:
            x_start = claim.top_left_x()
            y_top = claim.top_left_y()
            y_bottom = claim.bottom_left_y()
            x_end = claim.top_right_x()
            
            # adding left endpoints of square to queue
            heapq.heappush(squares_endpoints, (x_start, ADD_POINT, (y_top, y_bottom + 1)))

            # adding right endpoints of square to queue
            heapq.heappush(squares_endpoints, (x_end + 1, REMOVE_POINT, (y_top, y_bottom + 1)))

            # note the end-segment-signal (value = -1) is placed on the next cell after the last cell
            # hence the +1

    return squares_endpoints


def calculate_requested_area_for_bst(bst: list):
    """ given an in-order traversal of the segment BST of a single column,
        calculate the area in that column that is covered by more than 1 square
    """
    
    last_segment = 0  # scan the column from index Y=0 upwards
    square_num = 0    # number of squares currently 'live' while scanning the column
    area = 0          # the area covered by more than one claim in this column
    
    for segment in bst:
        segment_len = segment[0] - last_segment
        last_segment = segment[0]
        if square_num > 1:
            area += segment_len
        square_num += segment[1]   # segment[1] is positive if claim boundary is opening, negative if closing
        
    return area


def add_segment_to_bst(bst, y_coord, value):
    """ add the Y_coord to the BST while allowing for segments to intersect
        in the case of intersection add the value to the node in the bst rather than replace the node
        note: a +value signals the start of a square and a - value signals the end of that square
        a 0 value in a BST node has no effect on the calculations and can be deleted
    """
    bst.insert(y_coord, value)
    # if the value is negative and it ends up accumulating to a 0-rank node delete that node
    n = bst.find(y_coord)
    if n and n.data == 0:
        bst.remove(y_coord)


def process_rectangle_edge(segment_bst, add_or_remove_edge, y_top, y_bottom):
    """ add or remove a vertical edge of a claim rectangle to the segment tree """
    
    # assuming add_or_remove_edge = 1 to signal adding an edge to the segment tree,
    # and -1 to remove the same edge
    # using insert() to add a segment to the tree and
    # the same function with a flipped sign for the value will effectively remove it
    # because insert() removes nodes with a value of 0
    
    segment_bst.insert(y_top, add_or_remove_edge * 1)
    segment_bst.insert(y_bottom, add_or_remove_edge * -1)


def all_segments_of_x(x, h):
    """ given x generate all the segments in heap h for the given x coordinate """
    while h and h[0][0] == x:
        yield heapq.heappop(h)
        
        
def next_x_on_heap(h):
    return h[0][0]  # the minimum X is always in index 0 in the heap


def bst_ospf_puzzle_solution(filename: str) -> int:
    """
    parse claims file and return the intersecting area (in square inches)
    returns: total_intersecting_area

    """
    multi_rect_covered_area = 0

    # read and parse the input file, adding the
    # rectangles right and left edges to a priority queue
    rectangles_edges_heap = read_claims_into_pq(filename)

    start_time = time.time()
    
    # for every X coordinate having edges in the queue create a BST of
    # horizontal segments along that column defined by that X coordinate
    column_segments_bst = aoc_bst.BST()
    last_x = 0
    area = 0

    while rectangles_edges_heap:
        last_x = next_x_on_heap(rectangles_edges_heap)
        
        # construct segment tree from all the segments of current x in the scan
        for edge_points in all_segments_of_x(last_x, rectangles_edges_heap):
            _, add_or_remove, y_coords = edge_points
            y_top, y_bottom = y_coords
            process_rectangle_edge(column_segments_bst, add_or_remove, y_top, y_bottom)
            
        # calculate the area covered by multiple claims in this vertical segment
        ordered_list_of_segments = column_segments_bst.inorder()
        area = calculate_requested_area_for_bst(ordered_list_of_segments)
        
        # calc the number of columns this tree spans over until the next one
        col_num = 0
        if rectangles_edges_heap:
            col_num = next_x_on_heap(rectangles_edges_heap) - last_x
            # note: last tree is only closing segments and does not contribute to area
            
        # add the total area covered by multiple claims in this tree to total
        multi_rect_covered_area += col_num * area

    end_time = time.time()
    print(f"The algorithm took {end_time - start_time} seconds to complete")
    
    return multi_rect_covered_area
    

if __name__ == "__main__":
    print(bst_ospf_puzzle_solution('claims.txt'))
