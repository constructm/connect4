#!/usr/bin/env python3
from termcolor import colored, cprint
import os

# grid: 7 x 6

board = []
x = colored(' X ', 'red', attrs=['bold'])
o = colored(' O ', 'blue', attrs=['bold'])
empty = " - "
winning_score = 4

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def index_in_list(list,index):
    if index < 0 or index > len(list) - 1:
        return False
    else:
        return True

def calc_diag(player,row,column,direction):
    loop_diagonally = True
    row_ = row
    col_ = column
    scenario_ = 0

    while loop_diagonally:
        if index_in_list(board,row_) and index_in_list(board[row_],col_):
            if board[row_][col_] == player:
                scenario_ += 1
            else:
                scenario_ = 0

            if direction == "up,right":
                row_ -= 1
                col_ += 1
            elif direction == "down,left":
                row_ += 1
                col_ -= 1
            elif direction == "down,right":
                row_ += 1
                col_ += 1
            elif direction == "up,left":
                row_ -= 1
                col_ -= 1
        else:
            loop_diagonally = False
        
        if scenario_ == winning_score:
            break

    return scenario_

def is_win_calc(player,row,column):
    scenario_1 = 0
    scenario_2 = 0
    scenario_3 = 0
    scenario_4 = 0
    scenario_5 = 0
    scenario_6 = 0

    # scenario 01: bottom up
    for i in range(len(board),0,-1):
        if scenario_1 != winning_score:
            row_ = i - 1
            if board[row_][column] == player:
                scenario_1 += 1
            else:
                scenario_1 = 0

    # scenario 02: left to right
    for row_ in board:
        for i in row_:
            if scenario_2 != winning_score:
                if i == player:
                    scenario_2 += 1
                else:
                    scenario_2 = 0

    # scenario 03: diagonal (bottom up - right)
    scenario_3 = calc_diag(player,row,column,"up,right")

    # scenario 04: diagonal (top down - left)
    scenario_4 = calc_diag(player,row,column,"down,left")

    # scenario 05: diagonal (top down - right)
    scenario_5 = calc_diag(player,row,column,"down,right")

    # scenario 06: diagonal (bottom up - left)
    scenario_6 = calc_diag(player,row,column,"up,left")

    # check scenerio scores
    if scenario_1 >= 4 or scenario_2 >= 4 or scenario_3 >= 4 or scenario_4 >= 4 or scenario_5 >= 4 or scenario_6 >= 4:
        return True
    else:
        return False

def start_board():
    global board
    board = [[],[],[],[],[],[]]
    for i in range(0,6):
        board[i] = [empty,empty,empty,empty,empty,empty,empty]
    #return board

def print_board():
    global board
    print()
    line = 0
    for row in board:
        print(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        line += 1
    print(" 0 "," 1 "," 2 "," 3 "," 4 "," 5 "," 6 ")
    print()

def add_play(player,column):
    global board
    play_allocated = False
    is_win = False
    for i in range(len(board),0,-1):
        row = i - 1
        if board[row][column] == empty:
            board[row][column] = player
            play_allocated = True
            is_win = is_win_calc(player,row,column)
            break
    return {"play_allocated":play_allocated, "is_win":is_win}

def switch_players():
    # switch players around for next play
    global current_player
    if current_player == x:
        current_player = o
    else:
        current_player = x

def play():   
    # initialise game
    global current_player
    start_board()
    game_over = False
    current_player = x
    feedback=""

    # start game
    while game_over != True:
        # display prompt
        print("\nActive player:"+current_player)
        print("Type in q and enter to quit game or R to reset game")
        cprint(feedback,'magenta')

        # display board and prompt for play
        print_board()
        play = input("Please select a column number (0 - 6): ")
        print()

        if play == "q":
            game_over = True
            clear()
            cprint("G A M E   O V E R !  T h a n k s  f o r  p l a y i n g .",'magenta')
        elif play == "R":
            start_board()
            feedback = ""
        elif play.isnumeric() == False or int(play) > 6 or int(play) < 0:
            feedback = "Invalid input. Please try again."
        else:
            # make play
            the_play = add_play(current_player,int(play))

            if the_play["play_allocated"] == False:
                feedback = "Column "+play+" is full, please try another column."
            else:
                # check for a win
                if the_play["is_win"]:
                    game_over = True
                    clear()
                    print_board()
                    cprint("G A M E  O V E R !  W I N N E R  I S  P L A Y E R  "+current_player,"magenta")
                else:
                    # reset feedback
                    feedback = ""

                    # switch players around for next play
                    switch_players()
                    clear()

play()
