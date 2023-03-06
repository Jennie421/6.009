import os
import sys

if '.' not in sys.path:
    sys.path.insert(0, '.')
sys.setrecursionlimit(3000)

from search import search

import doctest

# NO OTHER IMPORTS!



##################################################
#  Problem 1
##################################################


def grid_mode(grid):
    """
    Given a 2-d array of values, return a new 2-d array whose element at
    position (r, c) is the most commonly occurring element from the input in
    location (r, c) and all of its neighbors.

    >>> inp = [
    ...     ['o', 'O',   7, 'o'],
    ...     [  7,  7,  'o', 'o'],
    ...     ['C',  7,  'o', 'f'],
    ...     ['a', 'C', 'O', 'O'],
    ... ]
    >>> exp = [
    ...     [  7,   7, 'o', 'o'],
    ...     [  7,   7, 'o', 'o'],
    ...     [  7,   7, 'o', 'o'],
    ...     ['C', 'C', 'O', 'O']
    ... ]
    >>> grid_mode(inp) == exp
    True
    """
    nrows = len(grid)
    ncols = len(grid[0])
    result = [ [None] * ncols for _ in range(nrows) ]

    for r in range(nrows):
        for c in range(ncols):
            neighbors = [grid[r][c]]
            
            if r - 1 >= 0:
                neighbors.append( grid[r-1][c] )
                if c - 1 >= 0:
                    neighbors.append( grid[r-1][c-1] )

            if c - 1 >= 0:
                neighbors.append( grid[r][c-1] )
                if r+1<nrows:
                    neighbors.append( grid[r+1][c-1] )
            
            if r + 1 < nrows:
                neighbors.append( grid[r+1][c] )
                if c + 1 < ncols:
                    neighbors.append( grid[r+1][c+1] )
            
            if c + 1 < ncols:
                neighbors.append( grid[r][c+1] )
                if r-1 >= 0:
                    neighbors.append( grid[r-1][c+1] )
    
            greatest_freq = 0 
            mode = 0 
            count = {} # neighbor: frequency 
            for neighbor in neighbors:
                freq = count.get(neighbor, 0)
                count[neighbor] = freq + 1
                if freq > greatest_freq:
                    greatest_freq = freq
                    mode = neighbor 
            result[r][c] = mode

    return result


##################################################
#  Problem 2
##################################################


def setup_bus_catcher(start_location, bus_schedule_function):
    start_state = (0, start_location)
    """
    start_state should contain the initial state (vertex label) for the search
    process
    """

    def successors(state):
        """
        Given a state, successors(state) should be an interable object
        containing all valid states that can be reached within one move.
        """
        result = []
        row, col = state[1]
        
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                result.append((state[0] + 1, (row + r, col + c)))
        return result 


    def goal_test(state):
        """
        Return True if the given state satisfies the goal condition, and False
        otherwise.
        """
        return state[1] == bus_schedule_function(state[0])
        
    return successors, start_state, goal_test


def interpret_result(path):
    """
    Given a path as returned from the search process, return a list of (r, c)
    tuples required to catch the bus.
    """
    return [x[1] for x in path]


def catch_bus(start_location, bus_schedule_function):
    """
    This end-to-end function is included here for testing.  You should not
    change it.

    >>> path = catch_bus((0,0), lambda t: (1, t-3))
    >>> len(path)
    3
    >>> path[-1]
    (1, -1)
    >>> path[0]
    (0, 0)
    """
    result = search(*setup_bus_catcher(start_location, bus_schedule_function))
    return interpret_result(result)



##################################################
#  Problem 3
##################################################


with open(os.path.join(os.path.dirname(__file__), 'words.txt')) as f:
    ALL_WORDS = set(f.read().splitlines())


def words_at_location(board, location):
    """
    Given a 2-d array (list of lists) containing letters and a starting
    location, return a set of all words that can be formed starting from that
    location, according to the rules of Boggle as described in the quiz
    writeup.

    >>> board = [
    ...     ['t', 'w', 'y', 'r'],
    ...     ['e', 'n', 'p', 'h'],
    ...     ['g', 's', 'c', 'r'],
    ...     ['o', 'n', 's', 'e'],
    ... ]
    >>> r1 = words_at_location(board, (2, 1))
    >>> e1 = {'sego', 'sent', 'set', 'sew', 'sewn', 'son', 'song', 'sons', 'spry', 'spy'}
    >>> r1 == e1
    True
    >>> r2 = words_at_location(board, (0, 0))
    >>> e2 = {'ten', 'tens'}
    >>> r2 == e2
    True
    >>> words_at_location(board, (0, 3))
    set()
    """
    R = len(board)
    C = len(board[0])
    visited = set()

    def words_with_prefix(prefix):
        return {w for w in ALL_WORDS if w.startswith(prefix)}
    
    def neighbors(r, c):
        n = set()
        if r > 0 and c > 0: # Top left
            n |= {(r - 1, c - 1), (r - 1, c), (r, c - 1)}
        if r + 1 < R and c > 0: # Top right
            n |= {(r + 1, c - 1), (r + 1, c), (r, c - 1)}
        if r + 1 < R and c + 1 < C: # Bottom right
            n |= {(r + 1, c + 1), (r + 1, c), (r, c + 1)}
        if r > 0 and c + 1 < C: # Bottom left
            n |= {(r - 1, c + 1), (r - 1, c), (r, c + 1)}

        n.difference_update(visited) # remove all visited locations
        # for neighbor in n: if neighbor in visited: n.remove(neighbor)
        return n

    def words_at(r, c, prefix):
        new_prefix = prefix + board[r][c] 
        
        # Base case
        if not words_with_prefix(new_prefix): return set()
        
        words_found = set()
        if new_prefix in ALL_WORDS: words_found.add(new_prefix) 

        # Recursive step
        visited.add((r, c))
        for (nr, nc) in neighbors(r, c):
            words_found |= words_at(nr, nc, new_prefix)

        visited.remove((r, c))
        
        return words_found


    return words_at(location[0], location[1], '')


if __name__ == '__main__':
    doctest.testmod()

    path = catch_bus((0,0), lambda t: (1, t-3))
    # print(path)
