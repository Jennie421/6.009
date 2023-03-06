# No imports!


#############
# Problem 1 #
#############

def binary_trees(n):
    """As a generator, return all possible binary trees of size `k`,
    in any order, with no duplicates."""
    raise NotImplementedError


#############
# Problem 2 #
#############

def n_bishops(n, bishop_locs, target):
    """
    Finds the placement of target amount of bishops such that
    no two bishops can attack each other.
    :param n: the length of a side of the board
    :param bishop_locs: the locations of the bishops already on the board
    :param target: the total number of bishops
    """
    def attack(loc1, loc2):
        row1, col1 = loc1
        row2, col2 = loc2
        if abs(row1 - row2) == abs(col1 - col2):
            return True 
        return False

    if target == 0: 
        return bishop_locs
    
    for r in range(n):
        for c in range(n):
            for bishop in bishop_locs:
                if not attack(bishop, (r,c)):
                    return n_bishops(n, bishop_locs | {(r,c)}, target-1)
    


#############
# Problem 2 #
#############

class QuadTree():
    """
    Contains points that range between x values [x_start, x_end) 
    and y values [y_start, y_end).

    If the QuadTree is a leaf node, self.children should be None and 
    self.points should contain a set of at most four points.
    If the QuadTree is an internal (non-leaf) node, self.points should be None and 
    self.children should contain a list of four QuadTree nodes.

    The QuadTree should not have children with ranges that overlap.
    """
    def __init__(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.points = set()
        self.children = None

    def __str__(self, level=0):
        """
        Returns a string representation of the quadtree
        :param level: current level in the quadtree (level = 0 if node is the root)
        """
        ret = "\t"*level+"start:("+str(self.x_start)+", "+str(self.y_start)+\
                "), end:("+str(self.x_end)+", "+str(self.y_end)+")\n"
        if self.children is not None:
            for child in self.children:
                ret += child.__str__(level+1)
        else:  
            if len(self.points) == 0:
                ret += "\t"*(level+1)+"<No points>\n"
            for (x, y) in self.points:
                ret += "\t"*(level+1)+"("+str(x)+", "+str(y)+")\n"
        return ret

    def insert(self, point):
        """
        Insert a point into this quadtree by modifying the tree 
        directly, without returning anything.
        :param point: a tuple of 2 integers (x, y)
        """
        raise NotImplementedError


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
