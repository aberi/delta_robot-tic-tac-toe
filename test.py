import board
import numpy as np

def test_two_row(b):
    row = board.two_row(b, "X") 
    print row

def test_all_two_rows(b):
    row = board.all_two_rows(b, "X") 
    print row

def test_third_space(b, letter):
    print "\nPossible rows of three: "
    rows = board.all_two_rows(b, letter) 
    for r in rows:  
        third = board.third_space(r[0][0], r[0][1], r[1][0], r[1][1])
        if third != None:
            row = [r[0], r[1], third]
            row.sort()
            print row

def test_winning_move(b):
    r = board.winning_move(b, "O")
    print r

def test_all_winning_moves(b, letter):
    r = board.all_winning_moves(b, letter)
    print r
   
def test_fork(b, letter):
    board.fork(b, letter) 

if __name__ == "__main__":
    b = [[0, 1, 2], [1, 0, 0], [0, 0, 2]]

    print "\nTesting with " + str(b) 
    board.print_board(b)
    board.fork(b, "X") 
    board.block(b, "O")
    board.win(b, "X")
    board.fork(b, "X")
    board.block(b, "O")
    board.win(b, "X")
