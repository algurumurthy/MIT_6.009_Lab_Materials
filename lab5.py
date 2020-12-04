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
    dimensions = (num_rows, num_cols)
    return new_game_nd(dimensions, bombs)


def dig_2d(game, row, col):
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
    coordinate = (row, col)
    return dig_nd(game, coordinate)


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
    mask_list = game['mask']
    board_list = game['board']
    dimensions = game['dimensions']
    render_list = []
    for r in range(dimensions[0]): 
        row = []
        for c in range(dimensions[1]):
            row.append(False)
        render_list.append(row)
    for y in range(dimensions[0]):
        for x in range(dimensions[1]):
            if xray:
                if board_list[y][x] == 0:
                    render_list[y][x] = ' '
                else:
                    render_list[y][x] = str(board_list[y][x])
            else:
                if mask_list[y][x]:
                    if board_list[y][x] == 0:
                        render_list[y][x] = ' '
                    else:
                        render_list[y][x] = str(board_list[y][x])
                else:
                    render_list[y][x] = '_'
    return render_list


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
    rendered_list = render_2d(game, xray)
    string_row = ''
    for row_num in range(len(rendered_list)):
        string_value = ''.join(str(r) for r in rendered_list[row_num])
        if row_num == len(rendered_list) - 1:
            string_row = string_row + string_value
        else:
            string_row = string_row + string_value + '\n'
    return string_row


# N-D IMPLEMENTATION

def get_value_in_ndarray(ndarray, coordinate_tuple):
    """
    Given an array that represents the board/its dimensions as a list of lists
    and a tuple with a coordinate, returns the value at that place in the list
    """
    coordinate_list = list(coordinate_tuple)
    if len(coordinate_list) == 1:
        return ndarray[coordinate_list[0]]
    else:
        value = coordinate_list.pop(0)
        return get_value_in_ndarray(ndarray[value], coordinate_list)


def set_ndarray_value(ndarray, coordinate_tuple, value):
    """
    Given an array that represents the board/its dimensions as a list of lists
    and a tuple with a coordinate as well as a value, returns nothing but 
    changes the value at the coordinate to inputed value
    """
    coordinate_list = list(coordinate_tuple)
    if len(coordinate_list) == 1:
         ndarray[coordinate_list[0]] = value
    else:
        coordinate_value = coordinate_list.pop(0)
        set_ndarray_value(ndarray[coordinate_value], coordinate_list, value)


def create_new_ndarray(dimensions, value):
    """
    Given a tuple or list containing dimensions for a board/array, as well as a
    value with which to initialize each coordinate, return the new board/array
    """
    dimensions_list = list(dimensions) 
    if len(dimensions_list) == 1:
        final_list = []
        for i in range(dimensions_list[0]):
            final_list.append(value)
        return final_list
    else:
        list_rep = dimensions_list.pop(0)
        im_list = []
        for i in range(list_rep):
            im_list.append(create_new_ndarray(dimensions_list, value))
        return im_list


def get_all_coords(dims):
    """
    Given a tuple or list of dimensions, returns a list of tuples representing 
    all of the coordinates in the grid/board
    """
    dimensions = list(dims)
    if len(dimensions) == 1:
        for coord in range(dimensions[0]):
            yield (coord,)
    else:
        dimension = dimensions.pop(0)
        for num in range(dimension):
            for tup in get_all_coords(dimensions):
                yield (num,) + tup


def game_state(game):
    """
    Given a game, returns the state of the game
    """
    return game['state']


def get_neighbors(board, location, dimensions):
    """
    Given a list of lists, a tuple of a coordinate and the dimensions of a grid
    return a list of tuple coordinates representing all the neighbors of a certain
    location in the grid
    """
    location_tracker = 1
    if len(location) == 0:
        yield ()
        return
    for previous in get_neighbors(board, location[location_tracker:], dimensions[location_tracker:]):
        if location[0] < dimensions[0] - 1 and location[0] > 0:
            yield (location[0] + 1,) + previous
            yield (location[0] - 1,) + previous
        if location[0] == 0:
            yield (location[0] + 1,) + previous
        if location[0] == dimensions[0] - 1:
            yield (location[0] - 1,) + previous
        yield (location[0],) + previous

    
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
    board_list = create_new_ndarray(dimensions, 0)
    mask_list = create_new_ndarray(dimensions, False)
    for bomb in bombs:
        set_ndarray_value(board_list, bomb, '.')
        for bomb_neighbor in get_neighbors(board_list, bomb, dimensions):
            if get_value_in_ndarray(board_list, bomb_neighbor) != '.':
                set_ndarray_value(board_list, bomb_neighbor, 1+ get_value_in_ndarray(board_list, bomb_neighbor))
    new_game = {'dimensions': dimensions, 'state': 'ongoing', 'board': board_list, 'mask': mask_list}
    return new_game


def dig_nd(game, coordinates):
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

    Args:
       coordinates (tuple): Where to start digging

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
    board_list = game['board']
    mask_list = game['mask']
    dimensions = game['dimensions']
    revealed = 0
    value = get_value_in_ndarray(board_list, coordinates)
    if game['state'] == 'victory' or game['state'] == 'defeat':
        return revealed
    if get_value_in_ndarray(mask_list, coordinates) == True:
        return 0
    if value == '.':
        set_ndarray_value(mask_list, coordinates, True)
        game['state'] = 'defeat'
        revealed += 1
        return revealed
    if value != 0:
        set_ndarray_value(mask_list, coordinates, True)
        revealed += 1
    else:
        revealed += 1
        set_ndarray_value(mask_list, coordinates, True)
        for neighbor in get_neighbors(board_list, coordinates, dimensions):
            revealed += dig_nd(game, neighbor)
    all_coords = get_all_coords(dimensions)
    for coord in all_coords:
        if get_value_in_ndarray(board_list, coord) != '.' and get_value_in_ndarray(mask_list, coord) == False:
            game['state'] = 'ongoing'
            return revealed
    game['state'] = 'victory'
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
    # load the list of coordinates, loop through them, get from board,
    dimensions = game['dimensions']
    board_list = game['board']
    new_board = create_new_ndarray(dimensions, 0)
    mask_list = game['mask']
    all_coords = get_all_coords(dimensions)
    for coord in all_coords:
        board_val = get_value_in_ndarray(board_list, coord)
        mask_val = get_value_in_ndarray(mask_list, coord)
        if xray:
            if board_val == 0:
                set_ndarray_value(new_board, coord, ' ')
            else:
                set_ndarray_value(new_board, coord, str(board_val))
        else:
            if mask_val:
                if board_val == 0:
                    set_ndarray_value(new_board, coord, ' ')
                else:
                    set_ndarray_value(new_board, coord, str(board_val))
            else:
                set_ndarray_value(new_board, coord, '_')
    return new_board


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    #doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=False)
    
