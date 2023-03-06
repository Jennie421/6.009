#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url

import time


# NO ADDITIONAL IMPORTS!

"""
Each node (representing a location) is represented as a dictionary containing the following keys:
    'id' maps to an integer ID number for the node.
    'lat' maps to the node's latitude (in degrees).
    'lon' maps to the node's longitude (in degrees).
    'tags' maps to a dictionary containing additional information about the node, including information about the type of object represented by the node (traffic lights, speed limit signs, etc.).

Each way (representing an ordered sequence of connected nodes) is represented as a dictionary with the following keys:
    'id' maps to an integer ID number for the way.
    'nodes' maps to a list of integers representing the nodes that comprise the way (in order).
    'tags' maps to a dictionary containing additional information about the way (e.g., is this a one-way street? is it a highway or a pedestrian path? etc.).
"""

ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}


DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,
    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}


def build_auxiliary_structures(nodes_filename, ways_filename):
    """
    Create any auxiliary structures you are interested in, by reading the data
    from the given filenames (using read_osm_data)
    """
    adjacent = dict() # map a node to a dictionary in which its adjacent nodes are mapped to the speed limit  

    for way in read_osm_data(ways_filename):
        if  'highway' in way['tags'] and way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
            for i in range(len(way['nodes'])-1):
                start = way['nodes'][i]
                end = way['nodes'][i+1]
                speed = 0
                if 'maxspeed_mph' in way['tags']:
                    speed = way['tags']['maxspeed_mph']
                else:
                    way_type = way['tags']['highway']
                    speed = DEFAULT_SPEED_LIMIT_MPH[way_type]

                if start not in adjacent: adjacent[start] = dict()
                speed = max(speed, adjacent[start].get(end, 0)) # update speed
                adjacent[start][end] = speed

                if way['tags'].get('oneway', 'no') == 'no':   # if is twoway 
                    if end not in adjacent: adjacent[end] = dict() 
                    speed = max(speed, adjacent[end].get(start, 0)) # update speed
                    adjacent[end][start] = speed

            if way['nodes'][-1] not in adjacent:   # handle a way ending
                adjacent[way['nodes'][-1]] = dict()

    nodes_info = dict()
    for node in read_osm_data(nodes_filename):
        if node['id'] in adjacent: 
            info = {k:v for k, v in node.items() if k == 'lat' or k == 'lon'}
            nodes_info[node['id']] = info

    return {'adjacent': adjacent, 'nodes_info': nodes_info} 



def find_nearest_node (target, nodes_info): 
    """ Find the nearest relevant node to target location. """
    nearest = None 
    shortest_dis = None 
    for node in nodes_info.keys():
        loc = (nodes_info[node]['lat'], nodes_info[node]['lon'])
        dis = great_circle_distance(loc, target)
        if shortest_dis == None or dis < shortest_dis:
            shortest_dis = dis
            nearest = node
    return nearest



def optimal_path (adjacent, nodes_info, node1, node2, cost_func, heuristic = lambda x, y: 0):
    """
    Return an optimal path between the two nodes, given a cost function and a heuristic function. 
    """

    agenda = [([node1], 0, 0)] # a list of tuples ([path], actual_cost, estimate_cost)
    expanded = set() # keep track of expanded nodes 

    index = 0 # keep track of number of path popped off agenda 
    while True: 
        if not agenda: return None # if agenda is empty yet didn't get to goal = no valid path 

        group = agenda.pop(0) # pop the path with minimum cost 
        current_path = group[0]
        current = current_path[-1]
        cur_actual_cost = group[1]
        cur_h_cost = group[2]
        index += 1

        if current in expanded: continue 
        expanded.add(current)

        if current == node2: 
            print(index)
            return current_path # test whether the removed item is the goal node2 

        if current not in adjacent: continue # if doesn't have adjacent nodes and is not at goal = wrong path 
        
        for node in adjacent[current]: # find its adjacent nodes 
            if node not in expanded:
                speed = adjacent[current][node]
                new_path = current_path[:] + [node]
                actual_cost = cur_actual_cost + cost_func(current, node, speed) 
                estimate_total = actual_cost + heuristic(node, speed)
                agenda.append((new_path, actual_cost, estimate_total))

        agenda.sort(key=lambda x: x[2]) # sort agenda by estimate cost



def find_short_path_nodes(aux_structures, node1, node2):
    """
    Return the shortest path between the two nodes
    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        node1: node representing the start location
        node2: node representing the end location
    Returns:
        a list of node IDs representing the shortest path (in terms of
        distance) from node1 to node2
    """
    def distance_adjacent_nodes(n1, n2, speed):
        # return the distance between two given nodes
        loc1 = (nodes_info[n1]['lat'], nodes_info[n1]['lon'])
        loc2 = (nodes_info[n2]['lat'], nodes_info[n2]['lon'])
        distance = great_circle_distance(loc1, loc2)
        return distance
    
    def heuristic(n, speed):
        # return the herestic distance of a node 
        loc_n = (nodes_info[n]['lat'], nodes_info[n]['lon'])
        goal = (nodes_info[node2]['lat'], nodes_info[node2]['lon'])
        h_distance = great_circle_distance(loc_n, goal) 
        return h_distance

    adjacent = aux_structures['adjacent']
    nodes_info = aux_structures['nodes_info']

    return optimal_path(adjacent, nodes_info, node1, node2, distance_adjacent_nodes, heuristic)
    # return optimal_path(adjacent, nodes_info, node1, node2, distance_adjacent_nodes)



def find_short_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations
    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end location
    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of distance) from loc1 to loc2.
    """
    nodes_info = aux_structures['nodes_info']
    
    # finding the nearest node to loc1 and loc2 that is part of a relevant way 
    start = find_nearest_node(loc1, nodes_info)
    end = find_nearest_node(loc2, nodes_info)

    # finding the shortest path from n1 to n2 (in terms of miles)
    path_nodes = find_short_path_nodes(aux_structures, start, end)
    if path_nodes == None: return None 
    # convert the resulting path into (latitude, longitude) tuples.
    path = []
    for node in path_nodes:
        loc = (nodes_info[node]['lat'], nodes_info[node]['lon'])
        path.append(loc)
    return path



def find_fast_path_nodes(aux_structures, node1, node2):
    """
    Return the fastest path between the two nodes
    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        node1: node representing the start location
        node2: node representing the end location
    Returns:
        a list of node IDs representing the fastest path (in terms of
        time) from node1 to node2
    """
    def time_cost(node1, node2, speed): 
        # return the time cost between two given nodes
        loc1 = (nodes_info[node1]['lat'], nodes_info[node1]['lon'])
        loc2 = (nodes_info[node2]['lat'], nodes_info[node2]['lon'])
        distance = great_circle_distance(loc1, loc2)
        time = distance / speed
        return time

    adjacent = aux_structures['adjacent']
    nodes_info = aux_structures['nodes_info']

    return optimal_path(adjacent, nodes_info, node1, node2, time_cost)



def find_fast_path(aux_structures, loc1, loc2):
    """
    Return the fastest path between the two locations, in terms of expected
    time (taking into account speed limits).
    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end location
    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """
    nodes_info = aux_structures['nodes_info']
    # finding the nearest node to loc1 and loc 2that is part of a relevant way 
    start = find_nearest_node(loc1, nodes_info)
    end = find_nearest_node(loc2, nodes_info)

    fast_path_nodes = find_fast_path_nodes(aux_structures, start, end)
    if fast_path_nodes == None: return None 
   
    # convert the resulting path into (latitude, longitude) tuples.
    path = []
    for node in fast_path_nodes:
        loc = (nodes_info[node]['lat'], nodes_info[node]['lon'])
        path.append(loc)
    return path


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.

    # for node in read_osm_data('resources/mit.nodes'):
    #     print(node['tags'])
    # print(list(read_osm_data('resources/mit.ways')))

    # 2.1 the data 
    # count_nodes = 0 
    # count_names = 0
    # id_77_Massachusetts_Ave = None
    # for node in read_osm_data('resources/cambridge.nodes'):
    #     count_nodes += 1  
    #     if 'name'  in node['tags']:
    #         count_names += 1  
    #         if node['tags']['name'] == '77 Massachusetts Ave':
    #             id_77_Massachusetts_Ave = node['id'] 
    # print('total number of nodes:', count_nodes)
    # print('number of nodes that have a name:', count_names)
    # print('id of 77 MA Ave:', id_77_Massachusetts_Ave)

    # count_ways = 0
    # count_oneway = 0 
    # for way in read_osm_data('resources/cambridge.ways'):
    #     count_ways+= 1 
    #     if  'oneway' in way['tags']:
    #         if way['tags']['oneway'] == 'yes':
    #             count_oneway +=  1 
    # print("total number of ways:", count_ways)
    # print('number of oneway:', count_oneway)

    # 3.1 
    # print(great_circle_distance((42.363745, -71.100999), (42.361283, -71.239677)))
    
    # loc1, loc2 = None, None
    # for node in read_osm_data('resources/midwest.nodes'):
    #     if node['id'] == 233941454:
    #         loc1 = (node['lat'], node['lon'])
    #     if node['id'] == 233947199:
    #         loc2 = (node['lat'], node['lon'])
    # print(great_circle_distance(loc1, loc2))
    
    # path = None
    # for way in read_osm_data('resources/midwest.ways'):
    #     if way['id'] == 21705939:
    #         path = way['nodes']
    #         break
    # distance = 0
    # for i in range(len(path)-1):
    #     for node in read_osm_data('resources/midwest.nodes'): 
    #         if node['id'] == path[i]:
    #             loc1 = (node['lat'], node['lon'])
    #         elif node['id'] == path[i+1]:
    #             loc2 = (node['lat'], node['lon'])
    #     distance += great_circle_distance(loc1, loc2)
    # print(distance)

    # aux = build_auxiliary_structures('resources/midwest.nodes', 'resources/midwest.ways')
    # n1 = (41.375288, -89.459541)
    # n2 = (41.452802, -89.443683)
    # print(find_fast_path(aux, n1, n2))

    # loc1 = (42.355, -71.1009) # New House
    # loc2 = (42.3612, -71.092) # 34-501
    # print(find_fast_path(aux, loc1, loc2))
    # expected_path = [
    #     (42.355, -71.1009), (42.3575, -71.0927), (42.3582, -71.0931),
    #     (42.3592, -71.0932), (42.3601, -71.0952), (42.3612, -71.092),
    # ]
    # print('exp', expected_path)
    
    # 4.1 
    # aux = build_auxiliary_structures('resources/midwest.nodes', 'resources/midwest.ways')
    # nodes_info = aux['nodes_info']
    # loc1 = (41.4452463, -89.3161394)
    # n1 = None
    # shortest_dis_1 = None
    # for node in nodes_info.keys():
    #     loc = (nodes_info[node]['lat'], nodes_info[node]['lon'])
    #     dis = great_circle_distance(loc, loc1)
    #     if shortest_dis_1 == None:
    #         shortest_dis_1 = dis
    #         n1 = node
    #     elif dis < shortest_dis_1:
    #         shortest_dis_1 = dis
    #         n1 = node
    # print(n1)

    # 5.2 Heuristic 
    aux = build_auxiliary_structures('resources/cambridge.nodes', 'resources/cambridge.ways')
    loc1 = (42.3858, -71.0783)
    loc2 = (42.5465, -71.1787)
    find_short_path(aux, loc1, loc2)

    """
    total number of paths pulled off of the agenda in each case:
        no heuristic: 386,255
        heuristic: 47,609
    """


    # start_time = time.time()
    # build_auxiliary_structures('resources/cambridge.nodes', 'resources/cambridge.ways')
    # print("--- %s seconds ---" % (time.time() - start_time))