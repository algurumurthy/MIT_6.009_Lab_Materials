#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).


def getActor(data, actorid):
    """ data is dicionary: {actor:actor id} """
    for actor in data.keys():
        if data[actor] == actorid:
            return actor
    raise Exception('actor id doesn\'t exist')


def transform_data(raw_data):
    """
    Parameter of raw_data in list of tuples made into two data structures,
    the first being a dictionary mapping actors to their every co-star, and
    a second dictionary mapping every movie to its set of actors
    """
    new_data = {}
    for tup in raw_data:
        if tup[0] not in new_data:
            new_data[tup[0]] = {tup[1]}
        else:
            new_data[tup[0]].add(tup[1])
        if tup[1] not in new_data:
            new_data[tup[1]] = {tup[0]}
        else:
            new_data[tup[1]].add(tup[0])
    new_data_movies = {}
    for tup in raw_data:
        if tup[2] not in new_data_movies:
            new_data_movies[tup[2]] = {tup[1],tup[2]}
        else:
            new_data_movies[tup[2]].add(tup[1])
            new_data_movies[tup[2]].add(tup[2])
    return new_data, new_data_movies


def acted_together(data, actor_id_1, actor_id_2):
    """
    Given two actor IDs and transformed data, returns either True or False
    depending on whether or not the actors have performed together
    """
    if actor_id_1 == actor_id_2:
        return True
    return actor_id_2 in data[0][actor_id_1]


def actor_sets(data, actor_id):
    """
    Given transformed data and an actor id, returns the "neighbors" or co-stars
    of given actor
    """
    if actor_id not in data.keys():
        return set()
    return data[actor_id]


def actors_with_bacon_number(data, n):
    """
    Given transformed data and a cerain bacon number, returns the set of actors
    in possession of that particular bacon number
    """
    connections = actor_sets(data[0], 4724)
    #case in which the bacon number is zero, return Kevin Bacon (4724)
    if n == 0:
        return set(4724)
    #when n = 1 just look at all actors connected to Kevin Bacon (4724)
    if n == 1:
        return set(connections)
    
    initial_actors = {0:{4724}, 1: connections}
    current_level = 1
    previous = {4724}
    previous |= connections
    while current_level <= n:
        current_actors = initial_actors[current_level]
        new_set = set()
        for actor in current_actors:
            new_set |= actor_sets(data[0], actor)
        new_set = new_set - previous
        current_level = current_level + 1
        initial_actors[current_level] = new_set
        previous |= new_set
        if n > len(data[0].keys()):
            if not new_set:
                return set()
    return initial_actors[n]


def bacon_path(data, actor_id):
    """
    Given transformed data and an actor ID, determines the shortest path through
    co-stars to the actor "4724" or Kevin Bacon as a list
    """
    if actor_id == 4724:
        return [4724]    
    initial_actors = {}
    current_actors = {4724}
    visited = {4724}
    path = []
    while True:
        new_set = set()
        if not current_actors:
            return None
        for actor in current_actors:
            for actor2 in actor_sets(data[0], actor):
                if actor2 not in visited:
                    new_set.add(actor2)
                    visited.add(actor2)
                    initial_actors[actor2] = actor
                if actor2 == actor_id:
                    path.append(actor_id)
                    current_id = actor_id
                    while current_id != 4724:
                        path.append(initial_actors[current_id])
                        current_id = initial_actors[current_id]
                    path.reverse()
                    return path
        current_actors = new_set
#call actor to actor in bacon path

def actor_to_actor_path(data, actor_id_1, actor_id_2):
    """
    Given transformed data and two actor IDs, determines the shortest path
    through co-stars from actor 1 to actor 2 as a list
    """
    if actor_id_1 == actor_id_2:
        return [actor_id_1]    
    initial_actors = {}
    current_actors = {actor_id_1}
    visited = {actor_id_1}
    path = []
    while True:
        new_set = set()
        if not current_actors:
            return None
        for actor in current_actors:
            for actor2 in actor_sets(data[0], actor):
                if actor2 not in visited:
                    new_set.add(actor2)
                    visited.add(actor2)
                    initial_actors[actor2] = actor
                if actor2 == actor_id_2:
                    path.append(actor_id_2)
                    current_id = actor_id_2
                    while current_id != actor_id_1:
                        path.append(initial_actors[current_id])
                        current_id = initial_actors[current_id]
                    path.reverse()
                    return path
        current_actors = new_set


def actor_path(data, actor_id_1, goal_test_function):
    """
    Given transformed data and two actor IDs, determines the shortest path
    through co-stars (as a more general function) from actor 1 until the
    parameter goal_test_function(actor_id_1) returns true (as a list).
    """
    if goal_test_function(actor_id_1):
        return [actor_id_1]    
    initial_actors = {}
    current_actors = {actor_id_1}
    visited = {actor_id_1}
    path = []
    while True:
        new_set = set()
        if not current_actors:
            return None
        for actor in current_actors:
            for actor2 in actor_sets(data[0], actor):
                if actor2 not in visited:
                    new_set.add(actor2)
                    visited.add(actor2)
                    initial_actors[actor2] = actor
                if goal_test_function(actor2):
                    path.append(actor2)
                    current_id = actor2
                    while current_id != actor_id_1:
                        path.append(initial_actors[current_id])
                        current_id = initial_actors[current_id]
                    path.reverse()
                    return path
        current_actors = new_set


def actors_connecting_films(data, film1, film2):
    """
    Given two film IDs, looks into transformed data's second return object to
    find the shortest path between any two actors in each film and returns the
    path as a list
    """
    film1_actors = data[1][film1]
    film2_actors = data[1][film2]
    path = {}
    for actor1 in film1_actors: #should take constant time because there are 2 actors
        for actor2 in film2_actors:
            temp_path = actor_to_actor_path(data, actor1, actor2)
            if temp_path == None:
                path_len = 0
            else:
                path_len = len(temp_path)
                path[path_len] = temp_path
    final_path_key = min(path.keys())
    return path[final_path_key]        


def movie_paths(data, film2, film2):
    """
    Given two films, find the shortest path connecting those two films
    """
    move_path = [film1]
    short_actors_path = actors_connecting_films(data, film1, film2)
    index = 0
    while index < range(len(short_actors_path)):
        for n in short_actors_path:
            if data[0][n]


if __name__ == '__main__':
#    Test Case 1
#    with open('resources/small.pickle', 'rb') as f:
#        smalldb = pickle.load(f)
#    names = pickle.load(open('resources/names.pickle','rb'))
#    print(names['Kevin Bacon'])
#    print(getActor(names,1389469))
    
    
#    Test Case 2
#    with open('resources/small.pickle', 'rb') as f:
#        smalldb = pickle.load(f)
#    names = pickle.load(open('resources/names.pickle','rb'))
#    id1 = names['Barbra Rae']
#    id2 = names['Danny Aiello']
#    database = transform_data(smalldb)
#    print(acted_together(database, id1, id2))
    
    
#    Test Case 3
#    with open('resources/tiny.pickle', 'rb') as f:
#        smalldb = pickle.load(f) 
#    database = transform_data(smalldb)
#    names = pickle.load(open('resources/names.pickle','rb'))
#    print(actors_with_bacon_number(database, 0))
#    print(actors_with_bacon_number(database, 1))
#    print(actors_with_bacon_number(database, 2))
#    print(actors_with_bacon_number(database, 3))
    

#    Test Case 4
#    with open('resources/large.pickle', 'rb') as f:
#        smalldb = pickle.load(f) 
#    names = pickle.load(open('resources/names.pickle','rb'))
#    database = transform_data(smalldb)
#    names_list = []
#    for ids in actors_with_bacon_number(database, 6):
#        names_list.append(getActor(names, ids))
#    print(names_list)

    
#    Test Case 5
#    with open('resources/tiny.pickle', 'rb') as f:
#        smalldb = pickle.load(f) 
#    database = transform_data(smalldb)
#    print(actor_to_actor_path(database, 4724, 1640))
    
#   Test Case 6
#    with open('resources/large.pickle', 'rb') as f:
#        smalldb = pickle.load(f) 
#    names = pickle.load(open('resources/names.pickle','rb'))
#    id1 = names['Kevin Bacon']
#    id2 = names['Karsten Speck']
#    database = transform_data(smalldb)
#    nums = actor_to_actor_path(database, id1, id2)
#    final = []
#    for n in nums:
#        final.append(getActor(database, n))
#    print(final)
    pass
