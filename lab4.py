#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url

# NO ADDITIONAL IMPORTS!


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
    from the given filenames (using read_osm_data), and returns three structures,
    the first of which is a map of the nodes to other nodes it is connected to by
    a way. The second is a dictionary map of nodes to their individual locations,
    and the third is a map of the nodes to the connected nodes by way as well as
    the speed limit of the associate way connecting them
    """
    final_data_structure_1 = {}
    final_data_structure_2 = {}
    final_data_structure_3 = {}
    for way in read_osm_data(ways_filename):
         if 'highway' in way['tags'].keys():
            if way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
                if 'maxspeed_mph' in way['tags']:
                    limit = way['tags']['maxspeed_mph']
                else:
                    limit = DEFAULT_SPEED_LIMIT_MPH[way['tags']['highway']]
                if 'oneway' in way['tags'].keys() and way['tags']['oneway'] == 'yes':
                    index = 0
                    while index < len(way['nodes']) - 1:
                        id1, id2 = way['nodes'][index], way['nodes'][index +1]
                        if id1 not in final_data_structure_1:
                            final_data_structure_1[id1] = {id2}
                            final_data_structure_3[id1] = {id2 : limit}
                        else:
                            final_data_structure_1[id1].add(id2)
                            final_data_structure_3[id1][id2] = limit 
                        index = index + 1
                    if way['nodes'][len(way['nodes']) - 1] not in final_data_structure_1.keys():
                        final_data_structure_1[way['nodes'][len(way['nodes']) - 1]] = set()
                        final_data_structure_3[way['nodes'][len(way['nodes']) - 1]] = dict()
                else:
                    index = 0
                    while index < len(way['nodes']) - 1:
                        id1, id2 = way['nodes'][index], way['nodes'][index +1]
                        if id1 not in final_data_structure_1:
                            final_data_structure_1[id1] = {id2}
                            final_data_structure_3[id1] = {id2 : limit}
                        else:
                            final_data_structure_1[id1].add(id2)
                            final_data_structure_3[id1][id2] = limit
                        index = index +1
                    index2 = len(way['nodes']) - 1
                    while index2 >0:
                        id1, id2 = way['nodes'][index2], way['nodes'][index2 -1]
                        if id1 not in final_data_structure_1:
                            final_data_structure_1[id1] = {id2}
                            final_data_structure_3[id1] = {id2 : limit}
                        else:
                            final_data_structure_1[id1].add(id2)
                            final_data_structure_3[id1][id2] = limit
                        index2 = index2 - 1
    for node in read_osm_data(nodes_filename):
        location = (node['lat'], node['lon'])
        if node['id'] in final_data_structure_1.keys():
            final_data_structure_2[node['id']] = location
    for node in final_data_structure_1:
        for neighbor in final_data_structure_1[node]:
            loc1 = final_data_structure_2[node]
            loc2 = final_data_structure_2[neighbor]
            first_cost_distance = great_circle_distance(loc1, loc2)
            time = first_cost_distance / final_data_structure_3[node][neighbor]
            final_data_structure_3[node][neighbor] = time
    return final_data_structure_1, final_data_structure_2, final_data_structure_3


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
    considered_paths = [([node1], 0, 0)] 
    previous_nodes = set() 
    while len(considered_paths) != 0: 
        considered_paths.sort(key= lambda tup: tup[1] + tup[2]) 
        shortest_value = considered_paths.pop(0) 
        if shortest_value[0][-1] in previous_nodes: 
            continue
        if shortest_value[0][-1] == node2: 
            return shortest_value[0]
        else:
            previous_nodes.add(shortest_value[0][-1])
            for node in aux_structures[0].get(shortest_value[0][-1], {}):
                loc1 = aux_structures[1][shortest_value[0][-1]]
                loc2 = aux_structures[1][node]
                cost = great_circle_distance(loc1, loc2) 
                if node in previous_nodes:
                    continue
                else:
                    considered_paths.append((shortest_value[0] + [node], shortest_value[1] + cost, great_circle_distance(loc2, aux_structures[1][node2])))
    return None


def find_short_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of distance) from loc1 to loc2.
    """
    location = aux_structures[1]
    final_path = []
    distance_1 = float('inf')
    distance_2 = float('inf')
    for node in location:
        distance_new = great_circle_distance(loc1, location[node])
        distance_2_new = great_circle_distance(loc2, location[node])
        if distance_new < distance_1:
                node1 = node
                distance_1 = distance_new
        if distance_2_new < distance_2:
                node2 = node
                distance_2 = distance_2_new
    path = find_short_path_nodes(aux_structures, node1, node2)
    if path == None:
        return None
    for node in path:
        final_path.append(location[node])
    return final_path


def find_fast_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations, in terms of expected
    time (taking into account speed limits).

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """
    location = aux_structures[1]
    final_path = []
    distance_1 = float('inf')
    distance_2 = float('inf')
    for node in location:
        distance_new = great_circle_distance(loc1, location[node])
        distance_2_new = great_circle_distance(loc2, location[node])
        if distance_new < distance_1:
                node1 = node
                distance_1 = distance_new
        if distance_2_new < distance_2:
                node2 = node
                distance_2 = distance_2_new
                
    considered_paths = [([node1], 0, 0)] 
    previous_nodes = set()
    node_path = []
    while len(considered_paths) != 0: 
        considered_paths.sort(key= lambda tup: tup[1] + tup[2]) 
        shortest_value = considered_paths.pop(0) 
        if shortest_value[0][-1] in previous_nodes: 
            continue
        if shortest_value[0][-1] == node2: 
            node_path.extend(shortest_value[0])
            break
        else:
            previous_nodes.add(shortest_value[0][-1])
            for node in aux_structures[0].get(shortest_value[0][-1], {}):
                cost = aux_structures[2][shortest_value[0][-1]][node]
                if node in previous_nodes:
                    continue
                else:
                    considered_paths.append((shortest_value[0] + [node], shortest_value[1] + cost, 0))
    if len(node_path) == 0:
        return None
    for node in node_path:
        final_path.append(location[node])
    return final_path


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
#    data_list = []
#    data_list_2 = []
#    for node in read_osm_data('resources/midwest.ways'):
#        data_list.append(node)
#    for node in read_osm_data('resources/midwest.nodes'):
#        data_list_2.append(node)
#    dist = 0
#    for n in data_list:
#        if n['id'] == 21705939:
#            counter = 0
#            final_list = []
#            for num in data_list_2:
#                if num['id'] in n['nodes']:
#                    final_list.append(num)
#            for x in range(len(final_list)):
#                if x < len(final_list) - 1:
#                    n1 = final_list[x]
#                    n2 = final_list[x+1]
#                    dist = dist + great_circle_distance((n1['lat'], n1['lon']),(n2['lat'], n2['lon']))
#    print(dist)
    data = build_auxiliary_structures('resources/mit.nodes', 'resources/mit.ways')
    print(data[0])
    print(find_short_path_nodes(data, 2, 5))
    
#    pass
