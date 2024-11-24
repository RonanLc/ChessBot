from main import DEBUG
from main import UI_interface
from main import UI_terminal

import piece_move
import os
import sys

label = "[move] "

#if UI_interface:
#    from UI import ChessDisplay
#    chess_display = ChessDisplay()

PieceMove = piece_move.PieceMove()

pieces_trad = {"K": 6, "Q": 5, "B": 4, "N": 3, "R": 2, "P": 1}
pieces_trad_inv = {v: k for k, v in pieces_trad.items()}
score_trad = {"Q": 9, "B": 3, "N": 3, "R": 5, "P": 1}

class moveTools:

    def moveConvert(string_square):
        
        x = ord(string_square[0]) - 97
        y = 8 - int(string_square[1])

        int_square = y * 8 + x
        
        return int_square
    

    def pieceConvert(string_piece):
        return pieces_trad[string_piece]


class ChessMove:

    if UI_interface:
        def __init__(self, chess_display):
            self.chess_display = chess_display
    else:
        def __init__(self):
            pass

    def setMove(self, board, move, turn, score):
        
        if len(move):

            if move == "exit":
                if not DEBUG and UI_terminal:
                    os.system('cls')
                print("Thanks for using ChessBot. Bye...")
                sys.exit(0)

            if ord(move[0]) > 90:
                move = "P" + move
                if DEBUG:
                    print(label + "P added.")
                    print(label + str(move))

        if len(move) < 5:
            if DEBUG:
                print(label + "The string of the action is too short.")
            return 3

        if (move[0] in 'KNPQR') and (move[1] in 'abcdefgh') and (move[2] in '12345678') and (move[3] in 'abcdefgh') and (move[4] in '12345678'):
            pass
        else:
            if DEBUG:
                print(label + "The string of the action don't correspond to the format *Piece * start letter * start number * end letter * end number*.")
            return 3
        
        if DEBUG:
            print(label + "Start spliting the string.")

        piece = move[0]

        actualSquare = moveTools.moveConvert(move[1]+move[2])

        nextSquare = moveTools.moveConvert(move[3]+move[4])

        if DEBUG:
            print(label + "Piece : " + piece)
            print(label + "From : " + str(actualSquare))
            print(label + "To : " + str(nextSquare))

        _error = PieceMove.moveCheck(board, piece, actualSquare, nextSquare)

        if DEBUG:
            print(label + "error is " + str(_error))

        if _error == 0:
            
            if PieceMove.nextState == 2:
                score[turn] += score_trad[pieces_trad_inv[abs(board[nextSquare])]]
            elif PieceMove.nextState == 3:
                shift = nextSquare%8 - actualSquare%8
                if DEBUG:
                    print(label + "Shift : " + str(shift))
                    print(label + "Actual square : " + str(actualSquare))
                score[turn] += score_trad[pieces_trad_inv[abs(board[actualSquare+shift])]]
                board[actualSquare+shift] = 0

            board[nextSquare] = moveTools.pieceConvert(piece)
            board[actualSquare] = 0

            if PieceMove.nextState == 4:
                for i in range(57,63):
                    if board[i] == 6:
                        if i < 60:
                            if DEBUG:
                                print(label + "Roque gauche pour i : " + str(i))
                            board[i+1] = 2
                            board[56] = 0
                        else:
                            if DEBUG:
                                print(label + "Roque droite pour i : " + str(i))
                            board[i-1] = 2
                            board[63] = 0

            for i in range(8):
                if board[i] == 1:
                    if not DEBUG and UI_terminal:
                        os.system('cls')
                    if UI_terminal:
                        print("Promotion !")
                    if UI_terminal:
                        if UI_interface:
                            self.chess_display.plot(board)
                            selection = self.chess_display.inputKey("Choose the piece you want to get : ")
                        else:
                            selection = input("Choose the piece you want to get : ")
                    else:
                        selection = input() # Demander une action par l'IA

                    if selection[0] == "Q":
                        board[i] = 5
                    elif selection[0] == "R":
                        board[i] = 2
                    elif selection[0] == "B":
                        board[i] = 4
                    elif selection[0] == "N" or selection[0] == "K":
                        board[i] = 3

        return _error