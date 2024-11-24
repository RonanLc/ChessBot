from main import DEBUG

label = "[piece_move] "

totalMenace = [[],[]]

class Tools:
        
    def boardValue(x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return 64
        else:
            return y * 8 + x
    
    def xValue(square):
        return square%8
    
    def yValue(square):
        return square//8


class PieceMove:

    nextState = None

    checkedMove = []  # Valeur de l'echiquier de 0 à 63
    stateMove = []    # 1 : Déplacement | 2 : Prend une pièce | 3 : Prend une piece en passant, une singerie ce move

    enPassant = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]
    
    castle = [[1, 1, 1],
              [1, 1, 1]]

    def moveCheck(self, board, piece, actualSquare, nextSquare):

        x = Tools.xValue(actualSquare)
        y = Tools.yValue(actualSquare)

        """
        Y|X 0   1   2   3   4   5   6   7 : X
        0 |   |   |   |   |   |   |   |   |
        1 |   |   |   |   |   |   |   |   |
        2 |   |   |   |   |   |   |   |   |
        3 |   |   |   |   |   |   |   |   |
        4 |   |   |   |   |   |   |   |   |
        5 |   |   |   |   |   |   |   |   |
        6 |   |   |   |   |   |   |   |   |
        7 |   |   |   |   |   |   |   |   |
        Y
        """

        if piece == "P":
            if self.pawnMove(board, x, y):
                return 1 # La pièce dite n'est pas à la case dite

        elif piece == "R":
            if self.rookMove(board, x, y):
                return 1 # La pièce dite n'est pas à la case dite

        elif piece == "N":
            if self.knightMove(board, x, y):
                return 1 # La pièce dite n'est pas à la case dite

        elif piece == "B":
            if self.bishopMove(board, x, y):
                return 1 # La pièce dite n'est pas à la case dite
            
        elif piece == "Q":
            if self.queenMove(board, x, y):
                return 1 # La pièce dite n'est pas à la case dite

        elif piece == "K":
            if self.kingMove(board, x, y):
                return 1 # La pièce dite n'est pas à la case dite
        
        if DEBUG :
            print(label + "Possible move : " + str(self.checkedMove))

        for i in range(len(self.checkedMove)):
            if self.checkedMove[i] == nextSquare:
                self.nextState = self.stateMove[i]

                if piece == "P":
                    if y == 6:
                        self.enPassant[0][x] = 0

                if piece == "K":
                    if Tools.boardValue(x,y) == 60:
                        self.castle[0][1] = 0

                if piece == "R":
                    if Tools.boardValue(x,y) == 56:
                        self.castle[0][0] = 0
                    if Tools.boardValue(x,y) == 63:
                        self.castle[0][2] = 0

                if DEBUG:
                    print(label + "En passant value : " + str(self.enPassant[0]))
                    print(label + "Castle value : " + str(self.castle[0]))

                return 0 # Move possible
        
        return 2 # Move impossible


    def pawnMove(self, board, x, y):

        self.checkedMove.clear()
        self.stateMove.clear()

        if board[Tools.boardValue(x,y)] == 1:

            if board[Tools.boardValue(x,y-1)] == 0:                         # Avance d'une case
                self.checkedMove.append(Tools.boardValue(x,y-1))
                self.stateMove.append(1)
            
            if board[Tools.boardValue(x-1,y-1)] < 0:                        # Mange en diagonale gauche
                self.checkedMove.append(Tools.boardValue(x-1,y-1))
                self.stateMove.append(2) 
            
            if board[Tools.boardValue(x+1,y-1)] < 0:                        # Mange en diagonale droite
                self.checkedMove.append(Tools.boardValue(x+1,y-1))
                self.stateMove.append(2)

            if board[Tools.boardValue(x-1,y)] < 0:                          # Mange en passant en diagonale gauche
                self.checkedMove.append(Tools.boardValue(x-1,y-1))
                self.stateMove.append(3)

            if board[Tools.boardValue(x+1,y)] < 0:                          # Mange en passant en diagonale droite
                self.checkedMove.append(Tools.boardValue(x+1,y-1))
                self.stateMove.append(3)

            if y == 6:                                                      # Avance de deux cases 
                if board[Tools.boardValue(x,y-1)] == 0 and board[Tools.boardValue(x,y-2)] == 0:
                    self.checkedMove.append(Tools.boardValue(x,y-2))
                    self.stateMove.append(1)

        else:
            return 1 # La pièce dites n'est pas à la case dites
        
    def rookMove(self, board, x, y):

        self.checkedMove.clear()
        self.stateMove.clear()

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Haut, Bas, Droite, Gauche

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                square = Tools.boardValue(nx, ny)
                if square == 64:  # Hors de l'échiquier
                    break
                if board[square] == 0:  # Case libre
                    self.checkedMove.append(square)
                    self.stateMove.append(1)
                elif board[square] < 0:  # Capture possible
                    self.checkedMove.append(square)
                    self.stateMove.append(2)
                    break
                else:  # Obstacle
                    break


    def knightMove(self, board, x, y):

        self.checkedMove.clear()
        self.stateMove.clear()

        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]  # Toutes les positions possibles

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            square = Tools.boardValue(nx, ny)
            if square == 64:  # Hors de l'échiquier
                continue
            if board[square] == 0:  # Case libre
                self.checkedMove.append(square)
                self.stateMove.append(1)
            elif board[square] < 0:  # Capture possible
                self.checkedMove.append(square)
                self.stateMove.append(2)


    def bishopMove(self, board, x, y):

        self.checkedMove.clear()
        self.stateMove.clear()

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonales

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                square = Tools.boardValue(nx, ny)
                if square == 64:  # Hors de l'échiquier
                    break
                if board[square] == 0:  # Case libre
                    self.checkedMove.append(square)
                    self.stateMove.append(1)
                elif board[square] < 0:  # Capture possible
                    self.checkedMove.append(square)
                    self.stateMove.append(2)
                    break
                else:  # Obstacle
                    break


    def queenMove(self, board, x, y):

        self.checkedMove.clear()
        self.stateMove.clear()

        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Directions de la tour
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Directions du fou
        ]

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                square = Tools.boardValue(nx, ny)
                if square == 64:  # Hors de l'échiquier
                    break
                if board[square] == 0:  # Case libre
                    self.checkedMove.append(square)
                    self.stateMove.append(1)
                elif board[square] < 0:  # Capture possible
                    self.checkedMove.append(square)
                    self.stateMove.append(2)
                    break
                else:  # Obstacle
                    break


    #def kingMove(self, board, x, y, danger_squares):
    def kingMove(self, board, x, y):
        """
        - board : tableau représentant l'échiquier
        - x, y : position actuelle du roi
        - danger_squares : liste des cases où le roi ne peut pas aller (cases attaquées par l'adversaire)
        """

        self.checkedMove.clear()
        self.stateMove.clear()

        moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Déplacements orthogonaux
            (1, 1), (-1, -1), (1, -1), (-1, 1)  # Déplacements diagonaux
        ]

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            square = Tools.boardValue(nx, ny)

            if square == 64:  # Hors de l'échiquier
                continue

            """if square in danger_squares:  # Case contrôlée par une pièce adverse
                continue"""

            if board[square] == 0:  # Case libre
                self.checkedMove.append(square)
                self.stateMove.append(1)

            elif board[square] < 0:  # Capture possible
                self.checkedMove.append(square)
                self.stateMove.append(2)

        square = Tools.boardValue(x, y)

        if self.castle[0][0] and self.castle[0][1]:  # Roque gauche
            flag = 0

            for i in range(1, square-(8*7)):
                if board[square-i] != 0:
                    flag = 1
            if not flag:
                self.checkedMove.append(Tools.boardValue(x-2, y))
                self.stateMove.append(4)  # Code 4 pour roque
 
        if self.castle[0][2] and self.castle[0][1]:  # Roque droite
            flag = 0
            for i in range(1, (8*8-1)-square):
                if board[square+i] != 0:
                    flag = 1
            if not flag:
                self.checkedMove.append(Tools.boardValue(x+2, y))
                self.stateMove.append(4)  # Code 4 pour roque
