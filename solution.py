assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    likewise with columns
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
    pass

def display(values):
    "Display these values as a 2-D grid."
    pass

def eliminate(values):
    pass

def only_choice(values):
    pass

def reduce_puzzle(values):
    pass

def solve(grid):
    pass

def search(values):
    pass

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(grid_values(diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
