#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


def update(f, var, boolean):
    """
    updating a formula to model the effect of a variable assignment
    """
    update = f[:]
    for i, literal in enumerate(update):
        for clause in literal: 
            if clause == (var, boolean):
                update[i] = None
                continue
            
            elif clause == (var, not boolean):
                update[i] = [c for c in literal if c != clause]
        
    new_f = []

    for literal in update:
        if literal == []:
            return 'falsifies'
        if literal != None:
            new_f.append(literal)

    if not new_f:
        # if every literal is None
        return 'truthifies'

    return new_f


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    variables = set()
    for clause in formula:
        for literal in clause:
            variables.add(literal[0])
    
    # Return a solution is there is one, otherwise None.
    def helper(formula):
        # base case
        if not formula or formula == 'truthifies':
            return {}
        elif formula == 'falsifies':
            return None

        formula = sorted(formula, key=len)

        # pick any unassigned variable x
        x = formula[0][0][0]

        # try x = True / False
        for x_value in [True, False]:
            f = update(formula, x, x_value)
            rest = helper(f)
            if rest != None: 
                rest[x] = x_value
                return rest 
        return None 

    return helper(formula)


# Helper Functions to generate formula for each of the three rules 

# Students are only assigned to rooms included in their preferences.
def preferences(student_preferences):
    """
    Takes a dict mapping a student to a set of rooms they prefer. 
    Returns a CNF expression of all students assigned to at least one preferred session. 
    """
    rule = []

    for student in student_preferences:
        literal = []
        for room in student_preferences[student]:
            literal.append( (str(student)+'_'+str(room), True) )
        rule.append(literal)
    
    return rule


# Each student is assigned to exactly one room.
def no_repetition(student_preferences, rooms):
    """
    Takes a dict mapping a student to a set of rooms.
    Returns a CNF expression that each student to be in at most one room
    i.e., for any pair of rooms, any given student can be in only one of them.
    """ 
    rule = []
    for student in student_preferences:
        for i in range(len(rooms)):
            for j in range(i+1, len(rooms)):
                if rooms[i] != rooms[j]:
                    literal = [ (str(student)+'_'+str(rooms[i]), False), (str(student)+'_'+str(rooms[j]), False) ]
                    rule.append(literal) 
    return rule


def subsets(S: set, k: int):
    """
    Returns all possible subsets with length k. 
    """
    if len(S) < k:
        return
    if k == 0:
        yield set()
    elif len(S) == k:
        yield set(S)
    else:
        # elem = S.pop()
        # if len(S) >= k:
        #     yield from subsets(S, k)
        # if len(S) >= k - 1:
        #     for s in subsets(S, k-1):
        #         yield {elem} | s
        # S.add(elem)
        elem = S.pop()
        yield from subsets(S, k)
        for s in subsets(S, k-1):
            yield {elem} | s
        S.add(elem)


# No room has more assigned students than it can fit.
def no_oversubscribed(student_preferences, room_capacities):
    """
    If a given room can contain N students, then in every possible group of N+1 students, 
    there must be at least one student who is not in the given room.
    If total num of people <= capacity, the room can be ignored. 
    """
    rule = []

    all_students = {s for s in student_preferences}

    for room in room_capacities:
        capacity = room_capacities[room]
        if capacity >= len(student_preferences): continue 
        
        sets = subsets(all_students, capacity + 1)
        for subset in sets: 
            literal = []
            for student in subset:
                literal.append( (str(student)+'_'+str(room), False) )
            rule.append(literal)

    return rule


def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """

    rule1 = preferences(student_preferences)

    rule2 = no_repetition(student_preferences, list(room_capacities.keys()))

    rule3 = no_oversubscribed(student_preferences, room_capacities)

    return rule1 + rule2 + rule3 




if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)
    # doctest.run_docstring_examples(satisfying_assignment, globals(), optionflags=_doctest_flags, verbose=False)


    # test soln: b = True, a = False 
    # example = [[('b', True), ('a', True)], [('b', True)], [('b', False), ('a', False)], [('c', True), ('d', True)]]
    # print(satisfying_assignment(example))


    # problem = boolify_scheduling_problem({'Alice': {'basement', 'penthouse'},
    #                             'Bob': {'kitchen'},
    #                             'Charles': {'basement', 'kitchen'},
    #                             'Dana': {'kitchen', 'penthouse', 'basement'}},
    #                             {'basement': 1,
    #                             'kitchen': 2,
    #                             'penthouse': 4})

    # print(satisfying_assignment(problem))

    # CNF expressing that students only in desired session 
    # rule1 = [
    #         [('Alice_basement', True), ('Alice_penthouse', True)], 
    #         [('Bob_kitchen', True)], 
    #         [('Charles_basement', True), ('Charles_kitchen', True)], 
    #         [('Dana_kitchen', True), ('Dana_penthouse', True), ('Dana_basement', True)]
    # ]

    # rule1_result = preferences({'Alice': {'basement', 'penthouse'},
    #                             'Bob': {'kitchen'},
    #                             'Charles': {'basement', 'kitchen'},
    #                             'Dana': {'kitchen', 'penthouse', 'basement'}})
    # print(rule1_result)

    # CNF Each Student In Exactly One Session
    # rule2 = [
    #     [('Alice_basement', False), ('Alice_kitchen', False)],
    #     [('Alice_basement', False), ('Alice_penthouse', False)],
    #     [('Alice_kitchen', False), ('Alice_penthouse', False)],
    #     [('Bob_basement', False), ('Bob_kitchen', False)],
    #     [('Bob_basement', False), ('Bob_penthouse', False)],
    #     [('Bob_kitchen', False), ('Bob_penthouse', False)],
    #     [('Charles_basement', False), ('Charles_kitchen', False)],
    #     [('Charles_basement', False), ('Charles_penthouse', False)],
    #     [('Charles_kitchen', False), ('Charles_penthouse', False)],
    #     [('Dana_basement', False), ('Dana_kitchen', False)],
    #     [('Dana_basement', False), ('Dana_penthouse', False)],
    #     [('Dana_kitchen', False), ('Dana_penthouse', False)]
    # ]

    # rule2_result = no_repetition({'Dana': {'kitchen', 'penthouse', 'basement'}})
    # print(rule2_result)

    # No Oversubscribed Sessions
    # rule3 = [
    #     [('Alice_basement', False), ('Bob_basement', False)],
    #     [('Alice_basement', False), ('Charles_basement', False)],
    #     [('Alice_basement', False), ('Dana_basement', False)],
    #     [('Bob_basement', False), ('Charles_basement', False)],
    #     [('Bob_basement', False), ('Dana_basement', False)],
    #     [('Charles_basement', False), ('Dana_basement', False)],
        
    #     [('Alice_kitchen', False), ('Bob_kitchen', False), ('Charles_kitchen', False)],
    #     [('Alice_kitchen', False), ('Bob_kitchen', False), ('Dana_kitchen', False)],
    #     [('Alice_kitchen', False), ('Charles_kitchen', False), ('Dana_kitchen', False)],
    #     [('Bob_kitchen', False), ('Charles_kitchen', False), ('Dana_kitchen', False)],
    # ]
    # print(subsets(['Alice', 'Bob', 'Charles', 'Dana'], 5))
    # rule3_result = no_oversubscribed({'Alice': {'basement', 'penthouse'},
    #                             'Bob': {'kitchen'},
    #                             'Charles': {'basement', 'kitchen'},
    #                             'Dana': {'kitchen', 'penthouse', 'basement'}},
    #                             {'basement': 1,
    #                             'kitchen': 2,
    #                             'penthouse': 4})
    # print(rule3_result)


"""
# c and (a or d) and (not b or a) and (not a or e or not d)
[ [('c', True)], [('a', True), ('d', True)], [('b', False), ('a', True)], [('a', False), ('e', True), ('d', False)] ]


# a and (not b or (c and d)) -> boolean
# a and (not b or c) and (not b or d) -> CNF
[[('a', True)], [('b', False), ('c', True)], [('b', False), ('d', True)]]


[
    [('a', True), ('b', True), ('c', True)],
    [('a', False), ('f', True)],
    [('d', False), ('e', True), ('a', True), ('g', True)],
    [('h', False), ('c', True), ('a', False), ('f', True)],
]

# CNF
(a or b or c) and (not a or f) and (not d or e or a or g) and (not h or c or not a or f)

# a CNF formula for the case where a = True
f and (not h or c or f)
[ [('f', True)], [('h', False), ('c', True), ('f', True)] ]

# a CNF formula for the case where a = False
[ [('b', True), ('c', True)], [('d', False), ('e', True), ('g', True)] ]

# a CNF formula for the case where a = True and f = True
'truthifies'

# a CNF formula for the case where a = True and f = False
'falsifies'

"""