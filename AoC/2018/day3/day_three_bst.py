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



overall expected complexity of O(MlogM) time where M is the number of claims
and space of O(M)

"""
import re
import heapq
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
    

ADD_POINT    = '+'
REMOVE_POINT = '-'

def read_claims_into_pq(filename: str):
    """ read all the claims into a priority queue (key = X coord of endpoints) """
    squares_endpoints = []
    
    with Claims(filename) as claims:
        for claim in claims:
            x_start  = claim.top_left_x()
            y_top    = claim.top_left_y()
            y_bottom = claim.bottom_left_y()
            x_end    = claim.top_right_x()
            
            # adding left endpoints of square to queue
            heapq.heappush(squares_endpoints, (x_start, ADD_POINT, (y_top, y_bottom)))

            # adding right endpoints of square to queue
            heapq.heappush(squares_endpoints, (x_end, REMOVE_POINT, (y_top, y_bottom)))

    return squares_endpoints


def print_end_points(hq):
    last_x = -1
    queues = {ADD_POINT: [], REMOVE_POINT: []}
    
    while hq:
        this_x = hq[0][0]     # hq[0] = hq.top() - the minimum is always in index 0
    
        if this_x != last_x:
            # print the lists and reset
            print(f"for x = {last_x} the queues were:")
            print(queues)
            queues = {ADD_POINT: [], REMOVE_POINT: []}
            last_x = this_x
        else:
            points = heapq.heappop(hq)
            queues[points[1]].append((points[2][0], 1))       # top adds a segment to tree
            queues[points[1]].append((points[2][1], -1))      # bottom removes that segment


def calculate_requested_area_for_bst(bst: list):
    """ given an inorder traveral of the segment BST of a single column,
        calculate the area in that column that is covered by more than 1 square """
    
    last_segment = 0  # scan the column from index Y=0 upwards
    sqaure_num = 0    # number of squares currently 'live' while scanning the column
    area = 0          # the area covered by more than one claim in this column
    
    for segment in bst:
        segment_len = segment[0] - last_segment
        last_segment = segment[0]
        if sqaure_num > 1:
            area += segment_len
        sqaure_num += segment[1]   # segment[1] is positive if claim boundary is opening, negative if closing
        
    return area


def add_segment_to_bst(bst, Y_coord, value):
    """ add the Y_coord to the BST while allowing for segments to intersect
        in the case of intersection add the value to the node in the bst rather than replace the node
    """
    bst.find((Y_coord, value))  # wrong !!! you can't know the value stored in the node.


def print_end_points_with_bst(hq):
    last_x = -1
    queues = {ADD_POINT: [], REMOVE_POINT: []}
    bst = aoc_bst.BST()
    
    while hq:
        this_x = hq[0][0]  # hq[0] = hq.top() - the minimum is always in index 0
        
        if this_x != last_x:
            # print the lists and reset
            print(f"for x = {last_x} the Y segment tree inorder was:")
            bstio = bst.inorder()
            print(bstio)
            area = calculate_requested_area_for_bst(bstio)
            print(f"for which the requested area was = {area}")
            last_x = this_x
        else:
            points = heapq.heappop(hq)
            
            if points[1] == ADD_POINT:
                bst.insert((points[2][0], 1))
                bst.insert((points[2][1], -1))
            else:
                bst.remove((points[2][0], 1))
                bst.remove((points[2][1], -1))


def naive_puzzle_solution(filename: str) -> (int, int):
    """
    parse claims file and return the intersecting area (in square inches)
    returns:
      total_intersecting_area, id_of_the_one_patch_without_intersection
    
    >>> naive_puzzle_solution("claims.txt")
    (115304, 275)
    
    """
    
    def mark_claim_on_map(c: Claim, fm: dict):
        for column in range(c.columns_n):
            for row in range(c.rows_n):
                try:
                    dict_key = (c.left_margin + column, c.top_margin + row)
                    fm[dict_key] = fm.get(dict_key, int()) + 1
                except IndexError as err:
                    print("error: ", err)
                    print(f"row:{c.left_margin + column} column:{c.top_margin + row}")
                    
    def claim_itersects(c: Claim, fm: dict) -> bool:
        """ function checks if claim c intesects with any other claim in the map ..
        ie. the square inches of the claim == 1 for all the squares of the claim
        returns True of claim intersects with other claims  """
        for column in range(c.columns_n):
            for row in range(c.rows_n):
                dict_key = (c.left_margin + column, c.top_margin + row)
                if fm[dict_key] != 1:
                    return True  # never marked or intersects with another
        # else
        return False
        # if we reached here
        # then all the claim's squares are marked with 1
        # (only one claim was made)
                
    fabric_map = {}  # a map of the square inches laid claim to on the fabric

    with Claims(filename) as claims:
        for claim in claims:
            mark_claim_on_map(claim, fabric_map)

    # count intersecting square inch blocks:
    intersection_area = 0
    for (_row, _column), square_inch_occupancy_num in fabric_map.items():
        if square_inch_occupancy_num > 1:
            intersection_area += 1

    # find the only patch that doesn't intersect other patches
    with Claims(filename) as claims:
        for claim in claims:
            if not claim_itersects(claim, fabric_map):
                return intersection_area, claim.claim_id   # there is only one claim that doesn't intersect.

    return None, None   # should never get here.



if __name__ == "__main__":
    #print_end_points(read_claims_into_pq('testclaims.txt'))
    print_end_points_with_bst(read_claims_into_pq('testclaims.txt'))