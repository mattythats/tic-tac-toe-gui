#Python 3.7.3
#Dependencies: numpy v1.16, pyforms v4

import sys
import numpy as np
from tkinter import *
from tkinter import ttk
from functools import partial
        
def check_win(score, scores): #TODO: generalize to mxn
  s = str(f'{score:09b}') #convert into a binary number padded with zeros in front to 9 digits to make comparison easier
  for i in range(len(scores)): #for every possible winning score
    num_ones = 0;
    t = str(f'{scores[i]:09b}') #also convert to a zero left padded 9 digit binary number
    for j in range(len(t)): #compare characters front to back
      if s[j] == t[j] and s[j] == '1': #if they're both one at a given position
        num_ones+=1 #increase number of ones
      if num_ones == 3: #if there are 3 ones then you win
        return True
  return False

def fail_check(board):
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == '0.0': #if theres a 0.0 it means a spot hasnt been filled yet
        return False
  return True

def ttt_setup(): #TODO: generalize to mxn?
  board = np.zeros(shape=(3,3)).astype('str') #this is the x/o board
  points = np.zeros(shape=(3,3)).astype('int') #this holds the point values for the cells
  scores = np.array([7,56,73,84,146,273,292,448]) #this array holds the sum of winning combos
  player_scores = np.zeros(shape=(2)).astype('int') #this holds the scores for the x/o players
  current_score = 1;
  for i in range(len(points)):
    for j in range(len(points[i])):
      points[i][j] = current_score;
      current_score+=current_score; #all cell point values are powers of 2 so the all winning scores are unique
  player_x_turn = True;
  winner = False;
  t = (board, points, scores, player_scores, player_x_turn, winner)
  return t
        
def print_board(board):
  for i in range(len(board)):
    for j in range(len(board[i])):
      c = ' '
      if(board[i][j] != '0.0'):
        c = board[i][j]
      print('|' + c, end='')
    print('\n------')
  print('\n')

def ttt_cli():
  (board, points, scores, player_scores, player_x_turn, winner) = ttt_setup()
  while(winner == False):
    print_board(board)
    ins = ' ' #whats gonna be put in the board
    pts = -1 #who gets the point
    if(player_x_turn):
      print("Player X", end = ' ')
      ins = 'x'
      pts = 0
    else:
      print("Player O", end = ' ')
      ins = 'o'
      pts = 1
    col = -1;
    row = -1;
    while(col < 0 or col > 2):
      col = int(input("Enter a column. 0 is the leftmost column.\n"))
      if(col < 0 or col > 2):
        print("Invalid column number.")
    while(row < 0 or row > 2):
      row = int(input("Enter a row. 0 is the top row.\n"))
      if(row < 0 or row > 2):
        print("Invalid row number.")
    while(board[row][col] != '0.0'):
      print("["+str(col)+"]["+str(row)+"] is already taken! Choose again!")
      col = -1
      row = -1
      while(col < 0 or col > 2):
        col = int(input("Enter a column. 0 is the leftmost column.\n"))
        if(col < 0 or col > 2):
          print("Invalid column number.")
      while(row < 0 or row > 2):
        row = int(input("Enter a row. 0 is the top row.\n"))
        if(row < 0 or row > 2):
          print("Invalid row number.")
    board[row][col] = ins
    player_scores[pts]+=points[row][col]
    if check_win(player_scores[pts],scores):
      print_board(board)
      if pts == 0:
        print("Player X Wins!")
        winner = True
      else:
        print("Player O Wins!")
        winner = True
    elif fail_check(board):
        print_board(board)
        print("Tie!")
        winner = True
    player_x_turn = not player_x_turn

class GameObj():
  def __init__(self):
    (self.board, self.points, self.scores, self.player_scores, self.player_x_turn, self.winner) = ttt_setup()

def cmd(i,j, o):
  c = ' '
  pts = -1;
  if(o.player_x_turn):
    c = 'x'
    pts = 0
  else:
    c = 'o'
    pts = 1
  if(o.board[j][i] == '0.0'):
    o.board[j][i] = c
    print_board(o.board)
    o.player_scores[pts]+=o.points[j][i]
    if check_win(o.player_scores[pts],o.scores):
      print_board(o.board)
      if pts == 0:
        print("Player X Wins!")
        o.winner = True
      else:
        print("Player O Wins!")
        o.winner = True
    elif fail_check(o.board):
        print_board(o.board)
        print("Tie!")
        o.winner = True
    o.player_x_turn = not o.player_x_turn
  else:
    print("Please pick another spot!");
    if(o.player_x_turn):
      print("It's X's turn")
    else:
      print("It's O's turn")
    
def ttt_gui():
  o = GameObj()
  root = Tk()
  root.title('Tic Tac Toe')
  main_frame = ttk.Frame(root, padding=25, relief='flat')
  main_frame.grid(column=0, row=0)
  root.columnconfigure(0, weight=1)
  root.rowconfigure(0, weight=1)
  for i in range(0,3):
    for j in range(0,3):
      b = Button(main_frame, text=' ', command=partial(cmd,i,j,o), height=10, width=20, justify='center')
      b.grid(column=i, row=j)
  if(o.player_x_turn):
    print("It's X's turn")
  else:
    print("It's O's turn")
  root.mainloop()
  
def main():
  if(len(sys.argv) < 2 or sys.argv[1].lower() != 'gui'):
    ttt_cli()
  else:
     ttt_gui()
  
if __name__ == "__main__":
  main()