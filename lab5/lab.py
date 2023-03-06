#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)


def dig_2d(game, row, col, is_first=True):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)
       is_first (bool): default parameter that indicates the first call to function 

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """

    return dig_nd(game, (row, col))


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """

    return render_nd(game, xray)

    # dimensions = game['dimensions']
    # board = game['board']
    # mask = game['mask']

    # render = init_array(dimensions, '') # initialize 
    
    # for loc in all_coordinates(dimensions):
    #     if not xray and not is_revealed(mask, loc): 
    #         update(render, loc, '_')            
    #     elif get_val(board, loc) == 0:
    #         update(render, loc, ' ')
    #     else: 
    #         new_val = str(get_val(board, loc))
    #         update(render, loc, new_val)

    # return render


def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    nrows, ncols = game['dimensions']
    board = game['board']
    mask = game['mask']

    asc = ''
    for r in range(nrows):
        s = ''
        for c in range(ncols):
            if not xray and mask[r][c] == False: 
                s += '_'            
            elif board[r][c] == 0:
                s += ' '
            else: 
                s += str(board[r][c])
        asc = asc + s + '\n'
    asc = asc[:-1]

    return asc 



# N-D IMPLEMENTATION

# Helper Functions 
def init_array(dimensions, val):
    """
    Given a list of dimensions and a value, 
    creates a new N-d array with those dimensions, 
    where each value in the array is the given value.
    """
    if len(dimensions) == 1:
        return [val] * dimensions[0]
    arr = []
    for d in range(dimensions[0]):
        inner_arr = []
        for rest in init_array(dimensions[1:], val):
            inner_arr.append(rest)
        arr.append(inner_arr)   
    return arr


def update(board, loc, val):
    """
    A function that, given an N-d game, a location, and a value, 
    replaces the value at the location in the array with the given value.
    """
    arr = board 

    for d in loc[:-1]: # save the last layer as reference 
        arr = arr[d]
    
    assert isinstance(arr, list), (board, loc)
    arr[loc[-1]] = val


def is_bomb(board, loc):
    """
    check whether a given location is a bomb. 
    """
    arr = board 
    for d in loc[:-1]: # save the last layer as reference 
        arr = arr[d]
    return arr[loc[-1]] == '.'


def is_revealed(mask, loc):
    """
    check whether a tile is revealed
    """
    arr = mask 
    for d in loc[:-1]: # save the last layer as reference 
        arr = arr[d]
    return arr[loc[-1]]


def get_val(board, loc):
    """
    Returns the value at a given location. 
    """
    arr = board 
    for d in loc[:-1]: # save the last layer as reference 
        arr = arr[d]
    return arr[loc[-1]]


def get_neighbors(D, loc):
    """
    A function that returns (or a generator that yields) 
    all the neighbors of a given location (maybe try a set of coordinates?) in a given game.
    """
    if len(loc) == 0:
        return [()]

    neighbors = []
    for x in [loc[0]-1, loc[0], loc[0]+1]:
        for rest in get_neighbors(D[1:], loc[1:]):
            if x >= 0 and x < D[0]:
                neighbors.append((x,) + rest)
    return neighbors 


def all_coordinates(dimensions):
    """
    A function that returns (or a generator that yields) 
    all possible coordinates in a given board.
    Parameter: dimention of the board 
    """
    if len(dimensions) == 0:
        return [()]

    coordinates = []
    for d in range(dimensions[0]):
        for rest in all_coordinates(dimensions[1:]):
            assert isinstance(rest, tuple), rest
            coordinates.append((d,) + rest)
    
    return coordinates


def update_game_state(game):
    """
    Given a game, update it's state to 'victory' if all safe tiles are revealed. 
    """
    remain = 0 # count the number of remaining safe tiles 
    for loc in all_coordinates(game['dimensions']):
        if not is_revealed(game['mask'], loc):  # if tile is not revealed 
            if not is_bomb(game['board'], loc):  # and the tile is not a bomb 
                remain += 1
    
    if remain > 0:
        game['state'] = 'ongoing'
    else:
        game['state'] = 'victory'
    


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    # initialize mask, all False 
    mask = init_array(dimensions, False)

    # initialize board, fill in bombs 
    board = init_array(dimensions, 0)
    for bomb in bombs: 
        update(board, bomb, '.')

    for loc in all_coordinates(dimensions):
        if not is_bomb(board, loc):
            # count number of bombs around each location
            neighbor_bombs = [n for n in get_neighbors(dimensions, loc) if is_bomb(board, n)]
            update(board, loc, len(neighbor_bombs))

    return {
        'dimensions': dimensions,
        'board' : board,
        'mask' : mask,
        'state': 'ongoing'}


def dig_nd(game, coordinates, is_first=True):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:s
        coordinates (tuple): Where to start digging
        is_first (bool): default parameter that indicates the first call to function 
    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    dimensions = game['dimensions']
    board = game['board']
    mask = game['mask']
    state = game['state']

    if state == 'defeat' or state == 'victory':
        return 0

    # if dig a bomb, defeated
    if is_bomb(board, coordinates):
        update(mask, coordinates, True)
        game['state'] = 'defeat'
        return 1

    # if the tile is safe and unrevealed, reveal it 
    if not is_revealed(mask, coordinates):
        update(mask, coordinates, True)
        revealed = 1
    else:
        return 0

    # dig neighbors recursively 
    if get_val(board, coordinates) == 0:
        neighbors = get_neighbors(dimensions, coordinates) # a list of neighbor coordinates
        for n in neighbors:
            if not is_bomb(board, n):
                if not is_revealed(mask, n):
                    revealed += dig_nd(game,n, is_first=False)

    if is_first:
        update_game_state(game)

    return revealed


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """ 
    dimensions = game['dimensions']
    board = game['board']
    mask = game['mask']

    render = init_array(dimensions, '') # initialize 
    
    for loc in all_coordinates(dimensions):
        if not xray and not is_revealed(mask, loc): 
            update(render, loc, '_')            
        elif get_val(board, loc) == 0:
            update(render, loc, ' ')
        else: 
            new_val = str(get_val(board, loc))
            update(render, loc, new_val)

    return render



if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.

    # doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=True)
    # doctest.run_docstring_examples(dig_2d, globals(), optionflags=_doctest_flags, verbose=False)
    doctest.run_docstring_examples(render_nd, globals(), optionflags=_doctest_flags, verbose=False)
