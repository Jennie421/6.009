#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).


def transform_data(raw_data):
    """
    Parameter: The raw database 
    Returns a tuple of three dictionaries: 
            1. a2m maps actors to movie id set 
            2. m2a maps movies to actor id set 
            3. a2a maps actors to actor id set 
    """
    a2m = {} # maps actor id to movie set
    m2a = {} # maps movie id to actor id set
    a2a = {} # maps actor id to actor id set
    
    for actor_id_1, actor_id_2, film_id in raw_data:
        if actor_id_1 not in a2m: a2m[actor_id_1] = set()
        if actor_id_2 not in a2m: a2m[actor_id_2] = set()
        if film_id not in m2a: m2a[film_id] = set()
        if actor_id_1 not in a2a: a2a[actor_id_1] = set()
        if actor_id_2 not in a2a: a2a[actor_id_2] = set()

        a2m[actor_id_1].add(film_id)
        a2m[actor_id_2].add(film_id)
        a2a[actor_id_1].add(actor_id_2)
        a2a[actor_id_2].add(actor_id_1)
        m2a[film_id] |= set([actor_id_1, actor_id_2])

    return a2m, m2a, a2a


def acted_together(data, actor_id_1, actor_id_2):
    """
    Parameters: 
        * The database to be used (the result of calling transform_data function on one of the databases)
        * Two IDs representing actors
    Returns:
        Return True if the two given actors ever acted together in a film and False otherwise. 
    """
    # we consider every actor to have acted with themselves
    if actor_id_1 == actor_id_2:
        return True 

    a2a = data[2] # dictionary that maps an actor to actors set 
    if actor_id_2 in a2a[actor_id_1]:
        return True 
    return False 


def actors_with_bacon_number(data, n):
    """
    Parameters: 
        * The database to be used (the result of calling transform_data function)
        * The desired Bacon number
    Returns:
        This function should return a Python set containing the ID numbers of all the actors with that Bacon number. 
    Note:
        Bacon number is defined as the smallest number of films separating a given actor from Kevin Bacon, whose actor ID is 4724.
    """
    baconid = 4724
    a2a = data[2] # map actor id to those acted together 

    this_Layer = {baconid} # set of id of current layer 
    parents = {baconid: None} # maps an actor id to its parent 

    num_layer = 0
    while num_layer != n and this_Layer: # stop if next layer is empty 
        next_layer = set()
        for actor in this_Layer:
            for neighbor in a2a[actor]:
                if neighbor not in parents: 
                    # only add to new layer if previously not seen 
                    parents[neighbor] = actor  # store parent relationship 
                    next_layer.add(neighbor)
        this_Layer = next_layer
        num_layer += 1

    return this_Layer 


def bacon_path(data, actor_id):
    """
    Parameters:
        * The database to be used 
        * An ID representing an actor
    Returns:
        Produce a list of actor IDs (any such shortest list if there are several) 
        detailing a "Bacon path" from Kevin Bacon to the actor denoted by actor_id. 
        If no path exists, return None.
    """
    def goal_test(id):
        return id == actor_id

    baconid = 4724
    path = find_path(data, baconid, goal_test)
    if path == None: return None
    return path
    


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    """
    Parameters:
        * The database to be used 
        * Two IDs representing actors
    Returns:
        Produce a list of actor IDs (any such shortest list if there are several) 
        detailing a path from the first actor to the second.
    """
    def goal_test(id):
        return id == actor_id_2 
    
    path = find_path(data, actor_id_1, lambda x: x==actor_id_2)
    if path == None: return None
    return path


# Extra Helper Function 
def find_path(data, actor_id_1, goal_test_function):
    """
    Parameters:
        * The database to be used 
        * Two IDs representing actors
    Returns:
        Produce a list of actor IDs (any such shortest list if there are several) 
        detailing a path from the first actor to the second.
    """
    start = actor_id_1 
    goal = None
    a2a = data[2]

    this_Layer = {start} # set of id of current layer 
    parents = {start: None} # maps an actor id to its parent 
    while this_Layer:
        next_layer = set()
        for actor in this_Layer:
            for child in a2a[actor]:
                if child not in parents: 
                    # only add to new layer if previously not seen 
                    parents[child] = actor  # store parent relationship 
                    next_layer.add(child)
                    
                if goal_test_function(child): # if satisfy requirement  
                    goal = child 
                    break 
            if goal != None: break 
        this_Layer = next_layer

    if goal not in parents: return None 

    # Find path
    path = []
    current = goal 
    while current is not None: 
        path.append(current)
        current = parents[current] # find its parent 

    path.reverse()
    return path


def movie_path(data, actor_id_1, actor_id_2):
    """
    Parameters:
        * The database 
        * two actor IDs
    Returns:
        A sequence of movies that traverses the path from actor 1 to actor 2. 
    """
    a2a_path = actor_to_actor_path(data, actor_id_1, actorid2) # the list representing actor to actor path 

    if a2a_path == None: return None 

    a2m = data[0] # a dict maps actor to movie set 

    path = []

    for i in range(len(a2a_path)-1):
        a1 = a2a_path[i]
        a2 = a2a_path[i+1]
        movie = a2m[a1] & a2m[a2]
        path.append(movie.pop())

    return path 


def actor_path(data, actor_id_1, goal_test_function):
    """
    Parameters: 
        * The database to be used (the same structure as before),
        * One actor ID to be used as our starting point, and
        * A function to be used as our goal test. 
            This function should take a single actor ID as input, 
            and it should return True if that actor represents a 
            valid ending location for the path, and False otherwise.
    Returns:
        Produce as output a list containing actor IDs, representing 
        the shortest possible path from the given actor ID to any actor 
        that satisfies the goal test function. 
        Return None if no actors satisfy the goal condition. 
    """
    # if the starting actor satisfies the goal test, 
    # return a length-1 list containing only that actor's ID.
    if goal_test_function(actor_id_1): return [actor_id_1]

    path = find_path(data, actor_id_1, goal_test_function) 
    if path == None: return None
    return path


def actors_connecting_films(data, film1, film2):
    """
    Parameters:
        * The database to be used 
        * Two film ID numbers
    Returns:
        Return the shortest possible list of actor ID numbers (in order) that connect those two films. 
        Your list should begin with the ID number of an actor who was in the first film, and it should end with the ID number of an actor who was in the second film.
        Return None if there is no path connecting those two films
    """
    def goal_test(id):
        if film2 in a2m[id]: return True
    
    a2m = data[0]
    m2a = data[1]
    
    # stores all paths that satisfy the requirement
    possible_paths = [] 
    i = 0 
    for actor in m2a[film1]:
        path = find_path(data, actor, goal_test)
        possible_paths.append(path)
        i += 1
    
    # find the shortest of all paths
    shortest_path = possible_paths[0] 
    for path in possible_paths:
        if len(path) < len(shortest_path):
            shortest_path = path

    return shortest_path 



if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
    with open('resources/small.pickle', 'rb') as f:
        smalldb = pickle.load(f) # a list of tuples (actor_id_1, actor_id_2, film_id)

    with open('resources/names.pickle', 'rb') as f:
        namedb = pickle.load(f) # dictionary, name: id

    with open('resources/tiny.pickle', 'rb') as f:
        tinydb = pickle.load(f) 
    
    with open('resources/large.pickle', 'rb') as f:
        largedb = pickle.load(f) 

    with open('resources/movies.pickle', 'rb') as f:
        moviedb = pickle.load(f) # dictionary, movie: id

    smalldb_trans = transform_data(smalldb)
    largedb_trans = transform_data(largedb)
    tinydb_trans = transform_data(tinydb)


    def get_name(db, val):
        # return key for any value
        for name, id in db.items():
            if val == id:
                return name
        return "name doesn't exist"

    # take a list of actor / movie ids, return a list of names 
    def id_to_name(ids, db): 
        names = []
        for id in ids:
            name = get_name(db, id)
            names.append(name)
        return names

    # 2.2 
    # print(namedb)
    # print(namedb['Maarten Dannenberg'])
    # print(get_name(namedb, 90117))

    # 4) acting together 
    # Jill_id = namedb['Jill Eikenberry']
    # Beatrice_id = namedb['Beatrice Winde']
    # print(acted_together(smalldb_trans, Jill_id, Beatrice_id))

    # Jim_id = namedb['Jim Hughes']
    # Paul_id = namedb['Paul Bru']
    # print(acted_together(smalldb_trans, Jim_id, Paul_id))

    # 5) Bacon Number 
    actor_id_6 = actors_with_bacon_number(largedb_trans, 6) # set of actors with bacon number 6
    actor_name_6 = set()

    for id in actor_id_6:
        name = get_name(namedb, id)
        actor_name_6.add(name)
    print(actor_name_6)
   
    # 6) Bacon Path 
    # print(bacon_path(tinydb_trans, 1640))

    # Rachelle_id = namedb['Rachelle Christine']
    # path_id = bacon_path(largedb_trans, Rachelle_id) # list of actors from Bacon to Rachelle 
    
    # Amy_id = namedb['Amy Meredith']
    # Miko_id = namedb['Miko Hughes']
    # path_id = actor_to_actor_path(largedb_trans, Amy_id, Miko_id)
    # path_name = id_to_name(path_id, namedb)
    # print(path_name)

    # 7) Movie Path
    # actor1 = namedb['Kevin Bacon']
    # actor2 = namedb['Julia Roberts']
    # movie_id = movie_path(largedb_trans, actor1, actor2) 
    # movie_name = id_to_name(movie_id, moviedb)
    # print(movie_name)

    # Verna_id = namedb['Verna Bloom']
    # Sven_id = namedb['Sven Batinic']
    # movie_id = movie_path(largedb_trans, Verna_id, Sven_id)
    # movie_name = id_to_name(movie_id, moviedb)
    # print(movie_name)

    #8) Generalizing 

    # film1 = 617
    # film2 = 74881
    # print('films:', film1, film2)
    # actors_connecting_path = actors_connecting_films(tinydb_trans, film1, film2)
    # actors_name = id_to_name(actors_connecting_path, moviedb)

