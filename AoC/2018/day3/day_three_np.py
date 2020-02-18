import re
import itertools
import numpy as np

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


def naive_puzzle_solution(filename: str) -> int:
    """
    parse claims file and return the intersecting area (in square inches)

    >>> naive_puzzle_solution("claims.txt")
    115304

    """
    
    def mark_claim_on_map(c, fm):
        fm[c.left_margin:c.left_margin + c.columns_n, c.top_margin:c.top_margin + c.rows_n] += 1
    
    FABRIC_SIZE = 1050  # a little larger than 1000
    fabric_map = np.zeros((FABRIC_SIZE, FABRIC_SIZE))
    
    with Claims(filename) as claims:
        for claim in claims:
            mark_claim_on_map(claim, fabric_map)
    
    intersection_area = 0
    for square_inch_occupancy_num in itertools.chain.from_iterable(fabric_map):
        if square_inch_occupancy_num > 1:
            intersection_area += 1
    
    return intersection_area


#################################################################################

def run_doctests():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    run_doctests()
