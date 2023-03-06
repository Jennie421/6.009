import doctest

# NO OTHER IMPORTS!


##################################################
#  Problem 1
##################################################


def most_after(L):
    """
    >>> most_after([]) is None
    True
    >>> most_after([0]) is None
    True
    >>> most_after([0, 0])
    0
    >>> most_after([0, 1])
    0
    >>> most_after([0, 1, 0, 1])
    1
    >>> most_after([0, 1, 0, 1, 2])
    1
    >>> most_after([0, -1, 0, 1, 2])
    0
    >>> most_after([1, 1, 1, 1, 2, 2, 1])
    2
    >>> most_after([2, 2, 2, 2, 1, 1, 2])
    2
    >>> most_after(list(range(100)))
    98
    >>> L = []
    >>> for x in range(5,10):
    ...     for y in range(7,14):
    ...         for z in range(3,8):
    ...             L.extend([x,y]*z)
    >>> len(L)
    1750
    >>> most_after(L)
    9
    """

    if len(L) == 0 or len(L) == 1:
        return None 

    follow = dict() # map a number to the numbers following it  

    number_of_distinct_nums = dict()

    for i in range(len(L)-1):
        cur = L[i]
        nxt = L[i+1]
        if cur not in follow:
            follow[cur] = set()
        follow[cur].add(nxt)
        number_of_distinct_nums[cur] = len(follow[cur])

    answer = None
    length = 0 

    for num in sorted(L[:-1]):
        if number_of_distinct_nums[num] >= length:
            length = number_of_distinct_nums[num]
            answer = num 
    return answer 

    


##################################################
#  Problem 2
##################################################

def verify(seq):
    for l in range(1, len(seq) // 2 + 1):
        if seq[-l:] == seq[-2 * l:-l]: # 这里如果有必要还可以优化
            return False
    return True


def nonrepeating_sequences(L, vals):
    """
    >>> set(nonrepeating_sequences(1, 'abc')) == {('a',), ('b',), ('c',)}
    True
    >>> x = {('a', 'c'), ('c', 'a'), ('a', 'b'), ('b', 'c'), ('c', 'b'), ('b', 'a')}
    >>> set(nonrepeating_sequences(2, 'abc')) == x
    True
    >>> len(set(nonrepeating_sequences(4, 'abc')))
    18
    >>> set(nonrepeating_sequences(3, 'ab')) == {('a', 'b', 'a'), ('b', 'a', 'b')}
    True
    >>> set(nonrepeating_sequences(4, 'ab'))
    set()
    """

    if L == 0:
        yield ()
        return
    
    for subseq in nonrepeating_sequences(L-1, vals):
        for item in vals:
            if verify(subseq + (item,)):
                yield subseq + (item,)




##################################################
#  Problem 3
##################################################

"""
an explanation of your original bug or lack of functionality:
1. used DFS instead of BFS. Concerning the speed, we want to look for shortest path, so BFS is better in this case
2. traditional BFS goes through layers one by one. But here we only need to keep record of one path for a given result
e.g. 4 + 4 and 4 + 4 + 4 - 4 gives the same value, so no need to store both paths. 
this saves memory and time on keeping track of the agenda and layers.
"""

operations = {
    '+': lambda x, y: x+y,
    '-': lambda x, y: x-y,
    '/': lambda x, y: x//y,
    '*': lambda x, y: x*y,
    '%': lambda x, y: x%y,
}

# bfs approach 
# def find_expression(T, n, limit=None):
#     depth = 0
#     values = { () : n } # Cache
#     current_layer = [()]

#     while depth < limit:
#         next_layer = []
#         while current_layer:
#             parent_path = current_layer.pop()
#             parent_value = values[parent_path]
            
#             for op, op_func in operations.items():
#                 value = op_func(parent_value, n)
#                 path = (*parent_path, op)
#                 values[path] = value

#                 if value == T:
#                     return path
                
#                 next_layer.append(path)
        
#         depth += 1
#         current_layer = next_layer
    
#     return None


def find_expression(T, n, limit=None):
    
    values = { n : () } # Shortest path to key

    for depth in range(limit):
        for parent_value in list(values.keys()):
            parent_path = values[parent_value]
            
            for op, op_func in operations.items():
                value = op_func(parent_value, n)
                path = (*parent_path, op)

                if value == T:
                    return path
                
                if value not in values:
                    values[value] = path
    
    return None


if __name__ == '__main__':
    # doctest.testmod()
    print(find_expression(7, 4, 5))