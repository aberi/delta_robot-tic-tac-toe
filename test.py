import board
import numpy as np
import argparse

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

def full_board(b):
    for i in range(0, 3):
        for j in range(0, 3):
            if b[i][j] == 0:
                return False 
        
    return True

def play_boards(boards, letters):
    for i in range(0, len(boards)):
        play(boards[i], letters[i])

def play(b, letter):
    board.print_board(b)
    play = board.move(b, letter)
    while play != 0 and not full_board(b):
        letter = board.opponent(letter)
        play = board.move(b, letter)
    
    if play != 0:
        print "Ends in a draw"
    

if __name__ == "__main__":
    ap = argparse.ArgumentParser() 
    ap.add_argument("-b", "--board", required=False, help="Board that the user would like to input, represented as a stringof 9 numbers: 0 for a blank space, 1 for an \'X\', and 2 for an \'O\'. An X or O must follow the 9 digits (also separated by a single space)")
    
    args = vars(ap.parse_args())
    
    print "Board that was input: " + str(args["board"])
    (b, letter) = board.string_to_board(str(args["board"]))
   
    board.move(b, letter) 
    
    print "Last space modified: " + str(board.last()) 
    # play(b, letter) 
    
    # boards = [[[0, 0, 1], [0, 2, 0], [1, 0, 0]], [[1, 1, 2], [0, 2, 0], [0,  0, 0]], [[1, 2, 1],[0, 0, 0], [2, 0, 0]]]
    # letters = ["O", "X", "X"]
    # 
    # play_boards(boards, letters)
