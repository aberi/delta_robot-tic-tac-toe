import numpy
import sys
import argparse
import copy

spaces = {"blank": 0, "X": 1, "O": 2}

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
    letter = spaces[letter]
    rows = all_two_rows(b, "X") 
    for r in rows:  
        third = third_space(r[0][0], r[0][1], r[1][0], r[1][1])
        if third != None:
            if b[third[0]][third[1]] == letter or b[third[0]][third[1]] == 0:
                return third

    return None

def all_winning_moves(b, letter):
    a = []
    rows = all_two_rows(b, letter) 
    letter = spaces[letter]
    for r in rows:  
        third = third_space(r[0][0], r[0][1], r[1][0], r[1][1])
        if third != None:
            if b[third[0]][third[1]] == letter or b[third[0]][third[1]] == 0:
                a.append(third)

    return a

# Win, if possible
def win(b, letter):
    space = winning_move(b, letter)
    if space != None:
        print letter + " plays at " + str(space) + ". " + letter + " wins."
        b[space[0]][space[1]] = spaces[letter] 
        print_board(b)
        return True
    
    return False
    

# Block some space that your opponent could win by occupying
def block(b, letter):
    space = winning_move(b, opponent(letter))
    if space != None:
        b[space[0]][space[1]] = spaces[letter] 
        print letter + " plays at " + str(space) + " (Block)"
        print_board(b)
        return True
    
    return False

def copy_board(b):
    new_b = [[0,0,0],[0,0,0],[0,0,0]]
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


def fork(b, letter):
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
                    print letter + " plays at " + str((i, j)) + " (Fork)"
                    print_board(b)
                    
                    return True
    
    return False
                 
