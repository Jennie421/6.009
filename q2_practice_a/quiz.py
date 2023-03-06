# No imports!


#############
# Problem 1 #
#############

with open('resources/words2.txt') as f:
    allwords = set(f.read().splitlines())

def is_word(x):
    return x in allwords

def split_words(s):
    raise NotImplementedError


############################################################
## Problem 2
############################################################

# Infinite lists

class InfiniteList:
    def __init__(self, f):
        """Create an infinite list where position i contains value f(i)."""
        pass

    def __getitem__(self, i):
        """Standard Python method for defining notation ls[i], which expands to ls.__getitem__(i)"""
        pass

    def __setitem__(self, i, val):
        """Standard Python method for defining notation ls[i] = val, which expands to ls.__setitem__(i, val)"""
        pass

    def __iter__(self):
        """Standard Python method for producing a generator where called for, e.g. to loop over.
        Note that this iterator has infinitely many values to return, so a usual loop over it will never finish!
        It should yield values from index 0 to infinity, one by one."""
        pass

    def __add__(self, other):
        """Standard Python method for defining notation a + b, which expands to a.__add__(b).
        For this quiz question, other will be another InfiniteList, and the generated InfiniteList should
        add the elements of self and other, at each position."""
        pass

    def __mul__(self, other):
        """Standard Python method for defining notation a * b, which expands to a.__mul__(b).
        For this quiz question, other will be a number, and the generated InfiniteList should
        multiply each position of self by other."""
        pass


##################################################
##  Problem 3
##################################################

def k_queens_coverage(k, size):
    """
    Checks if it is possible to place less than or equal to 'k' queens on a
    chess board of size 'size' such that every cell on the board is
    reachable by at least one queen and no two queens can attack each other.
    Returns any such board if it is possible, otherwise returns None.

    Given:
        k: the maximum number of queens you may place on the board
        size: size of the chess board

    Returns:
        A 1-D array of length size representing any board that satisfies
        the problem. Each index (i) in the array represents column i of the
        board. If there is a queen placed on column i, array[i] must equal
        the row index of the queen. If no queen is placed on column i,
        array[i] = -1. If there is no such board that satisfies the problem,
        return None.
    """
    raise NotImplementedError

if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
