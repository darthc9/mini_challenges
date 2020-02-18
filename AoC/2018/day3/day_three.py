"""
Advent of code 2018 - python coding contest
challenge for day 3 - https://adventofcode.com/2018/day/3



The problem outline:
-------------------------------
Each Elf has made a claim about which area of fabric would be ideal for Santa's suit.
All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric.
Each claim's rectangle is defined as follows:

- The number of inches between the left edge of the fabric and the left edge of the rectangle.
- The number of inches between the top edge of the fabric and the top edge of the rectangle.
- The width of the rectangle in inches.
- The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4
means that claim ID 123 specifies a rectangle
3 inches from the left edge,
2 inches from the top edge,
5 inches wide, and 4 inches tall.

claims.txt holds all the elves' claims for the fabric
How many square inches of fabric are within two or more claims?



better (not best) solution:
-------------------------------------------------------------------
1. keep a partial map of the fabric (dict of claimed square inches)
2. for each claim
    - identify the square inches of that claim on the map
    - increment the counter in those square inches.
3. for each claimed square inch in the map
    if it counts more than one claim add it to total
4. output total.




part 2: What is the ID of the only claim that doesn't overlap?
-------------------------------------------------------------------

I thought of adding the ID of the claim to the key of the map
and to a set, and removing it from the set in the case that
an intersection is detected. until one is left in the set.

a better solution is to go over the claims file one more time
and find the one claim that doesn't intersect with any other.

"""
import re


class Claim:
    """ Parse a claim string """
    
    def __init__(self, claim_str: str):
        """ turn string into claim object
            '#10 @ 936,278: 13x27'
          =  id    left,top  COLSxROWs
        """
        claim_tokens = filter(None, re.split("[ #@,:x]", claim_str))  # filter = (item for item in iterable if item)
        self.claim_id, self.left_margin, self.top_margin, self.columns_n, self.rows_n = map(int, claim_tokens)
        

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


def run_doctests():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    run_doctests()
