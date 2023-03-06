def all_coordinates(game):
    """
    A function that returns (or a generator that yields) 
    all possible coordinates in a given board.
    Parameter: dimention of the board 
    """
    dimensions = game['dimensions']

    if len(dimensions) == 0:
        yield [()]
    
    coordinates = []
    for d in range(dimensions[0]):
        for rest in all_coordinates(dimensions[1:]):
            coordinates.append((d,) + rest)
    
    yield coordinates


def get_neighbors(game, loc):
    """
    A function that returns (or a generator that yields) 
    all the neighbors of a given location (maybe try a set of coordinates?) in a given game.
    """
    D = game['dimensions']

    if len(loc) == 0:
        return [()]

    neighbors = []
    for x in [loc[0]-1, loc[0], loc[0]+1]:
        for rest in get_neighbors(loc[1:], D[1:]):
            if x >= 0 and x < D[0]:
                neighbors.append((x,) + rest)

    return neighbors 


def update(array, loc, val):
    """
    A function that, given an N-d game, a location, and a value, 
    replaces the value at the location in the array with the given value.
    """
    arr = array

    for d in loc[:-1]: # save the last layer as reference 
        arr = arr[d]
    
    arr[loc[-1]] = val


def init_array(dimensions, val):
    """
    A function that, given a list of dimensions and a value, 
    creates a new N-d array with those dimensions, 
    where each value in the array is the given value.
    """
    if len(dimensions) == 1:
        return [val] * dimensions[0]
    # if len(dimensions) == 0:
    #     return [[]]

    arr = []
    for d in range(dimensions[0]):
        inner_arr = []
        for rest in init_array(dimensions[1:], val):
            inner_arr.append(rest)
        arr.append(inner_arr)   

    return arr

print(init_array((2,4,2), 0))

def check_state(game):
    """
    A function that, given a game, returns the state of that game ('ongoing', 'defeat', or 'victory').
    """
    return game['state']


