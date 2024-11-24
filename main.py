UI_interface    = True
UI_terminal     = True
DEBUG           = False

if UI_interface:
    import UI

import move
import os

label = "[main] "

"""board = [-2, -3, -4, -5, -6, -4, -3, -2,
         -1, -1, -1, -1, -1, -1, -1, -1,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          1,  1,  1,  1,  1,  1,  1,  1,
          2,  3,  4,  5,  6,  4,  3,  2,
          99]"""

board = [ 0,  0,  0,  0,  0,  0,  0,  0,
          0,  1,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  1, -1,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          1,  1,  1,  1,  1,  1,  1,  1,
          2,  0,  0,  0,  6,  0,  3,  2,
          99]

score = [0,0] # W & B
turn = 1
action = ""
lastAction = ""
_error = 0

def error_terminal_print(_error):
    if _error == 1:
        print("Please select the correct piece you want to use.")       
    elif _error == 2:
        print("Please select a possible move.")       
    elif _error == 3:
        print("Please select a correct command.")

def board_terminal_print(board):
    print("    a  b  c  d  e  f  g  h")  # Coordonnées des colonnes
    print("  +------------------------+")

    for row in range(8):
        row_data = board[row * 8:(row + 1) * 8]  # Les 8 cases de la ligne
        row_str = " ".join(
            f"{'-' + move.pieces_trad_inv.get(abs(item), '.') if item < 0 else ' ' + move.pieces_trad_inv.get(item, '.') if item > 0 else ' .'}"
            for item in row_data
        )
        print(f"{8 - row} |{row_str} | {8 - row}")  # Coordonnées des rangées

    print("  +------------------------+")
    print("    a  b  c  d  e  f  g  h")  # Coordonnées des colonnes

def interface():
    if DEBUG:
        print(label + str(board))
    
    if UI_terminal:

        if not DEBUG:
            os.system('cls')

    if UI_interface:
        chess_display.plot(board)
    elif UI_terminal:
        board_terminal_print(board)

    if UI_terminal:
        error_terminal_print(_error)

        print("W : " + str(score[0]) + " | B : " + str(score[1]))
        print("The last move was : " + str(lastAction))

        if turn:
            print("Black turn")
        else:
            print("White turn")


if __name__ == "__main__":
    
    if UI_interface:
        chess_display = UI.ChessDisplay()
        chess_move = move.ChessMove(chess_display)
    else:
        chess_move = move.ChessMove()

    print("Welcome to ChessBot.")

    while(1):

        interface()

        if UI_interface:
            action = chess_display.inputKey("Next move : ")
        elif UI_terminal:
            action = input("Next move : ")
        else:
            action = input() # Demander une action par l'IA

        _error = chess_move.setMove(board, action, turn, score)

        if _error == 0:
            turn = (turn+1)%2
            lastAction = action

        error_terminal_print(_error)