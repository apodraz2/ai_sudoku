assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]

unitlist = row_units + column_units + square_units
diagonal_unit_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
all_diagonal_units = dict((s, [u for u in diagonal_unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


diagonal_peers = dict((s, set(sum(all_diagonal_units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values



def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    """My solution first gathers all the keys with two values.
    Then, I search and find all the naked twins by iterating through the peers of each key.
    Finally, if the twins match based on row, I search through all peers and only eliminate values from peers with matching rows,
    likewise with columns.
    """
    
    all_twins = [box for box in values.keys() if len(values[box]) == 2]
    
    naked_twins = []

    for box in all_twins:
        for peer in peers[box]:
            if values[box] == values[peer]:
                naked_twins.append( (box, peer) )

    for box in naked_twins:
        if box[0][0] == box[1][0]: 
            for peer in peers[box[0]]:
                if values[box[0]] != values[peer] and len(values[peer]) > 2 and box[0][0] == peer[0]:
                    
                    old_value = values[peer]
                
                    old_value = old_value.replace(values[box[0]][0], "")
                    old_value = old_value.replace(values[box[0]][1], "")
                    
                    assign_value(values, peer, old_value)
                    
        else:
            for peer in peers[box[0]]:
                if values[box[0]] != values[peer] and len(values[peer]) > 2 and box[0][1] == peer[1]:
                    
                    old_value = values[peer]
                    
                    old_value = old_value.replace(values[box[0]][0], "")
                    old_value = old_value.replace(values[box[0]][1], "")
                    
                    assign_value(values, peer, old_value)
    return values
    

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

#def cross(A, B):
 #   "Cross product of elements in A and elements in B."
  #  pass

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '.' for empties."
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)

    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    
    for box in solved_values:
        digit = values[box]
        for peer in diagonal_peers[box]:
            #values[peer] = values[peer].replace(digit, '')
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values

def only_choice(values):
    for unit in unitlist:
       for digit in '123456789':
           dplaces = [box for box in unit if digit in values[box]]
           if len(dplaces) == 1:
               #values[dplaces[0]] = digit
               assign_value(values, dplaces[0], digit)
    
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

    

def solve(grid):
    values = grid_values(grid)
    #print("beginning puzzle:")
    #display(values)
    values = reduce_puzzle(values)
    #print("solution after reduce:")
    #display(values)
    return search(values)

def search(values):
    #print("solution prior to search:")
    #display(values)
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(grid_values(diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
