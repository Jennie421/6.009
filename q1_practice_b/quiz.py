import sys
sys.setrecursionlimit(10000)

# NO OTHER IMPORTS!


##################################################
#  Problem 1 花费20min
##################################################

def get_mode(data):
    """ Finds the mode of a list of numbers. Breaks ties
        by preferring the greatest value. """
    
    greatest_freq = 0 
    mode = 0 
    count = {} # number: frequency 
    for num in data:
        # if num not in data: count[num] = 0 
        freq = count.get(num, 0)
        freq += 1 
        count[num] = freq
        if freq > greatest_freq:
            greatest_freq = freq
            mode = num 
        elif freq == greatest_freq:
            if num > mode:
                greatest_freq = freq
                mode = num     

    return mode 


##################################################
#  Problem 2  花费30min
##################################################

def find_anagram_groups(words, N):
    """ Given a list of words, returns the index i into 
        words that contains the Nth word of the first 
        appearing anagram group of size N.  """

    anagram = dict() # (tuple of chars): size count

    for idx in range(len(words)):
        chars = []
        for char in words[idx]:
            chars += [char]
        chars = sorted(chars)
        chars_t = tuple(chars)
        if chars_t in anagram: 
            anagram[chars_t] += 1 
            if anagram[chars_t] == N:
                return idx
        else:
            anagram[chars_t] = 1
    return None



##################################################
#  Problem 3
##################################################

def minimum_pegs2(peg_board): # 失败的
    """ Returns the minimum number of pegs that could be reached on
        the given peg board using valid peg solitaire moves.

        peg_board: a tuple representing a 1D peg board, where 1s are
                   holes with pegs and 0s are empty holes.
    """
    pb = list(peg_board)
    for i in range(len(pb)-2):
        if pb[i] == 1 and pb[i+1] == 1 and pb[i+2] == 0:
            pb[i], pb[i+1], pb[i+2] = 0, 0, 1
        elif pb[i] == 0 and pb[i+1] == 1 and pb[i+2] == 1:
            pb[i], pb[i+1], pb[i+2] = 1, 0, 0

    counter = 0
    for peg in pb:
        if peg == 1: counter += 1
    
    return counter 


def minimum_pegs(board):
    m = sum(board) # The min number of pegs is never greater than the number of 1s
    for i in range(len(board) - 2):
        if board[i : i + 3] == (0, 1, 1):
            new_board = board[:i] + (1, 0, 0) + board[i + 3:]
            m = min(m, minimum_pegs(new_board))
        elif board[i : i + 3] == (1, 1, 0):
            new_board = board[:i] + (0, 0, 1) + board[i + 3:]
            m = min(m, minimum_pegs(new_board))

    return m



def flip(s):

    if '(' not in s:
        return s
    
    new_s = ''
    for i in range(len(s)-1):
        if s[i] == '(':
            target = ''
            k = 0
            while s[i+1+k] != '(' and s[i+1+k] != ')':
                target += s[i+1+k]
                k+=1
            new_s = s[:i] + target[::-1] + s[i+k+2:]

    return flip(new_s)


if __name__ == "__main__":
    # print(flip('abc'))
    # print(flip('a(bc)d'))
    assert flip('a(b(cd))e') == 'acdbe'

    assert flip('((ab)(cd)(ef))g') == 'efcdabg'