import board
import numpy as np
import argparse
import serial
import time

spaces = {"blank": 0, "X": 1, "O": 2}

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

def play(b, letter, ser=None):
    our_turn = True
    board.print_board(b)
    p = board.move(b, letter)
    c = board.last()[0] + 1
    if ser != None:
        print "Writing to Arduino at space" + str(c)
        ser.write(chr(c))
    print p
    while p != 0 and not full_board(b):
        print "continuing loop"
        letter = board.opponent(letter)
        our_turn = not our_turn
        ser.write(chr(10))
        if our_turn:
            p = board.move(b, letter)
            c = board.last()[0] + 1
        else:
            space = int(raw_input("Enter a space from 1 to 9: ")) % 9 
            print (((space - 1) / 3), ((space - 1) % 3))
            b[(space - 1) / 3][(space - 1) % 3] = spaces[letter]
            board.print_board(b)
            c = space
        if ser != None:
            if c == 0:
                c = 9
            print "Writing to Arduino at space" + str(c)
            time.sleep(1)
            ser.write(chr(c))
            time.sleep(1)
    
    if p != 0:
        print "Ends in a draw"
    
def run():
    ap = argparse.ArgumentParser() 
    ap.add_argument("-b", "--board", required=False, help="Board that the user would like to input, represented as a stringof 9 numbers: 0 for a blank space, 1 for an \'X\', and 2 for an \'O\'. An X or O must follow the 9 digits (also separated by a single space)")
    
    args = vars(ap.parse_args())
    
    print "Board that was input: " + str(args["board"])
    (b, letter) = board.string_to_board(str(args["board"]))
     
    ser = serial.Serial('/dev/cu.usbmodemFD121', 9600)
    time.sleep(1)

    play(b, letter, ser) 

if __name__ == "__main__":
    status = run()
    exit(status)

