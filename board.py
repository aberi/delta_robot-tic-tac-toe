import numpy
import sys
import argparse
import copy

spaces = {"blank": 0, "X": 1, "O": 2}

last_space = -1

spaces_played = []

def last():
    return last_space

def empty_board(b):
    for i in range(0, 3):
        for j in range(0, 3):
            if b[i][j] != 0:
                return False 
    
    return True

def same_row((x1, y1), (x2, y2)):
    return x1 == x2

    
def same_col((x1, y1), (x2, y2)):
    return y1 == y2


def same_diag((x1, y1), (x2, y2)):
    return abs(x1 - x2) == abs(y1 - y2)


def in_line((x1, y1), (x2, y2)):
    return same_col((x1, y1), (x2, y2)) or same_row((x1, y1), (x2, y2)) or same_diag((x1, y1), (x2, y2))


def opponent(letter):
    if letter == "X":
        return "O"
    else:
        return "X"


def inbounds(i, j, width, length):
    return i >= 0 and j >= 0 and i < width and j < length


def two_row(b, letter): 
    if letter != "X" and letter != "O":
        raise Exception ("Invalid letter: must be X or O") 

    letter = spaces[letter]

    for i in range(0, 3):
        for j in range(0, 3):
            if b[i][j] == letter: 
    
                for i1 in range(i - 1, i + 2):
                    for j1 in range(j - 1, j + 2):
                        if (i1 != i or j1 != j) and inbounds(i1, j1, 3, 3) and b[i1][j1] == letter:
                            return [(i1, j1), (i, j)]                     

def all_two_rows(b, letter):
    if letter != "X" and letter != "O":
        raise Exception ("Invalid letter: must be X or O") 

    letter = spaces[letter]

    a = []

    for i in range(0, 3):
        for j in range(0, 3):
            if b[i][j] == letter: 
   
                # This is WRONG !!!
                for i1 in range(i - 2, i + 3):
                    for j1 in range(j - 2, j + 3):
                        if in_line((i, j), (i1, j1)) and (i1 != i or j1 != j) and inbounds(i1, j1, 3, 3) and b[i1][j1] == letter:
                            coord = [(i1, j1), (i, j)]
                            third = third_space(i1, j1, i, j)
                            if third != None and b[third[0]][third[1]] != opponent(letter):
                                coord.sort()
                                if coord not in a:
                                    a.append(coord)
    return a 

def num_two_rows(b, letter):
    return len(all_two_rows(b, letter))

def string_to_board(s):
    if len(s) != 19:
        raise Exception("String must be formatted as 9 digits followed by an X or O, each character having 1 space between one another")
    params = s.split(" ")
  
    new_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] 
    for i in range(0, 3):
        for j in range(0, 3):
            new_board[i][j] = int(params[i * 3 + j])
    
    return (new_board, params[9])

def third_space(x1, y1, x2, y2):
    # print "Current spaces are " + str((x1, y1)) + ", " + str((x2, y2))
    if (abs(x1 - x2) == 1 and abs(y1 - y2) == 2) or (abs(x1 - x2) == 2 and abs(y1 - y2) == 1):
        raise Exception ("Spaces are not within the same row!")
    
    if x1 == x2:
        if min(y1, y2) == 1:
            return (x1, 0) 
        elif max(y1, y2) == 2:
            return (x1, 1)
        else:
            return (x1, 2)
            
    elif y1 == y2:
        if min(x1, x2) == 1:
            return (0, y1)
        elif max(x1, x2) == 2:
            return (1, y1)
        else:
            return (2, y1)

    else: # abs(y1 - y2) == abs(x1 - x2) because this must be a diagonal row! If error checking was done properly
        max_y = max(y1, y2)
        min_y = min(y1, y2)
        max_x = max(x1, x2)   
    
        if max_y - min_y == 2:
            return (1, 1)
    
        else:
            if (x1, y1) == (2, 0) or (x2, y2) == (2, 0): 
                return (0, 2)
            elif (x1, y1) == (0, 2) or (x2, y2) == (0, 2):
                return (2, 0)
            elif (x1, y1) == (0, 0) or (x2, y2) == (0, 0):
                return (2, 2)
            elif (x1, y1) == (2, 2) or (x2, y2) == (2, 2):
                return (0, 0)
                
    return None 
    
        
def winning_move(b, letter):
    opp = spaces[opponent(letter)]
    rows = all_two_rows(b, letter) 
    letter = spaces[letter]
    for r in rows:  
        third = third_space(r[0][0], r[0][1], r[1][0], r[1][1])
        if third != None:
            if b[third[0]][third[1]] != opp:
                return third

    return None

def all_winning_moves(b, letter):
    a = []
    rows = all_two_rows(b, letter) 
    letter = spaces[letter]
    for r in rows:  
        third = third_space(r[0][0], r[0][1], r[1][0], r[1][1])
        if third != None:
            if b[third[0]][third[1]] != spaces[opponent(letter)]:
                a.append(third)

    return a

# 1 indicates to continue, 0 indicates that we are done
def move(b, letter):
    if win(b, letter) == None:
        if block(b, letter) == None and fork(b, letter) == None and block_fork(b, letter) == None and center(b, letter) == None and opposite_corner(letter, b) == None and empty_corner(letter, b) == None:
            return 1
        return 1
    return 0

def move(b, letter):
    space = win(b, letter) 
    if space == None:
        space = block(b, letter)
        if space == None:
            space = fork(b, letter)
            if space == None:   
                space = block_fork(b, letter)
                if space == None:
                    space = center(b, letter)
                    if space == None:
                        space = opposite_corner(b, letter)
                        if space == None:
                            space = empty_corner(b, letter)
                            else:
                                return space
                        else:
                            return space
        if block(b, letter) == None:
            if fork(b, letter) == None:
                if block_fork(b, letter) == None:
                    if center(b, letter) == None:
                        if opposite_corner(b, letter) == None:
                            if empty_corner(letter, b) == None:
                                

# Win, if possible
def win(b, letter):
    space = winning_move(b, letter)
    if space != None:
        print letter + " plays at " + str(space) + ". " + letter + " wins."
        b[space[0]][space[1]] = spaces[letter]
        print_board(b)
        last_space = space[0] * 3 + space[1]
        return space 
    
    return None 
   
def can_move(b, letter, (x, y)):
    return b[x][y] != spaces[opponent(letter)]

# Block some space that your opponent could win by occupying
def block(b, letter, debug=True):
    space = winning_move(b, opponent(letter))
    if space != None and can_move(b, letter, space):
        b[space[0]][space[1]] = spaces[letter] 
        last_space = space[0] * 3 + space[1]
        if debug:
            print letter + " plays at " + str(space) + " (Block)"
            print_board(b)
        return space 
    
    return None 

def center(b, letter, debug=True):
    if empty_board(b):
        return empty_corner(b, letter, debug)
    if can_move(b, letter, (1, 1)):
        b[1][1] = spaces[letter]
        last_space = 4
        if debug:
            print letter + " plays at " + str((1, 1)) + " (Center)"
            print_board(b)
        return (1, 1)

    return None

def opposite_corner(b, letter, debug=True):
    for corner in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        opposite = (abs(2 - corner[0]), abs(2 - corner[1]))
        if (b[corner[0]][corner[1]] == spaces[opponent(letter)]) and can_move(opposite):
            b[opposite[0]][opposite[1]] = spaces[letter]
            last_space = opposite[0] * 3 + opposite[1]
            if debug:
                print letter + " plays at " + str(opposite) + " (Opposite Corner)"
                print_board(b)
            return opposite

    return None 

def empty_corner(b, letter, debug=True):
    for corner in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if can_move(b, letter, corner):
            b[corner[0]][corner[1]] = spaces[letter]
            last_space = corner[0] * 3 + corner[1]
            if debug:
                print letter + " plays at " + str(corner) + " (Corner)"
                print_board(b)
            return corner  
    return None
            
             
def block_fork(b, letter, debug=True):
    prev_num_twos = num_two_rows(b, letter)
    
    for i in range(0, 3):
        for j in range(0, 3):
            if b[i][j] == spaces["blank"]:
                b_copy = copy_board(b)
                b_copy[i][j] = spaces[letter]
                new_num_twos = num_two_rows(b_copy, letter)
                diff_num_twos = new_num_twos - prev_num_twos 
    
                if diff_num_twos == 1:
    
                    # Check that this move does not force the opponent to create a fork
                    num_twos = num_two_rows(b_copy, opponent(letter)) 
                    winner = winning_move(b_copy, letter)
                    if winner != None:
                        b_copy[winner[0]][winner[1]] = spaces[opponent(letter)]
                        if num_two_rows(b_copy, opponent(letter)) >= num_twos + 2:
                            continue
                        else:
                            b[i][j] = spaces[letter]
                            last_space = i * 3 + j
                            print "Last space played at " + str(last_space)
                            if debug:
                                print letter + " plays at " + str((i, j)) + " (Block Fork)"
                                print_board(b)
                            return (i, j)
                    
                    
    b_copy = copy_board(b)
    space = fork(b_copy, opponent(letter), False) 
    if space != None: 
        b[space[0]][space[1]] = letter
        last_space = space[0] * 3 + space[1]
   
    return space 
    

def copy_board(b):
    new_b = [[0,0,0],
             [0,0,0],
             [0,0,0]]

    for i in range(0, 3):
        for j in range(0, 3):
            new_b[i][j] = b[i][j]

    return new_b

def print_board(b):
    print "._._._."
    for i in range(0, 3):
        s = "|"
        for j in range(0, 3):
            if b[i][j] == 0:
                s += " " 
            elif b[i][j] == 1:
                s += "X"
            else:
                s += "O"
            s += "|"
        print s
        print "._._._."
    print "\n"


def fork(b, letter, debug=True):
    prev_num_twos = num_two_rows(b, letter)
    
    for i in range(0, 3):
        for j in range(0, 3):
            if b[i][j] == spaces["blank"]:
                b_copy = copy_board(b)
                b_copy[i][j] = spaces[letter]
                new_num_twos = num_two_rows(b_copy, letter)
                diff_num_twos = new_num_twos - prev_num_twos 
    
                if diff_num_twos >= 2:
                    
                    b[i][j] = spaces[letter]
                    last_space = i * 3 + j
                    if debug:
                        print letter + " plays at " + str((i, j)) + " (Fork)"
                        print_board(b)
                    
                    return (i, j) 
    
    return None 
                 
