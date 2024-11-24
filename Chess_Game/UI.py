from main import DEBUG
from main import UI_terminal

import pygame
import os
import sys

label = "[UI] "

# Dimensions de la fenêtre
WIDTH, HEIGHT = 480, 480  # Dimensions de l'échiquier (en pixel)
TILE_SIZE = WIDTH // 8    # Nombre de case par lignes

# Couleurs des cases
WHITE = (235, 236, 208)
BLACK = (119, 149, 86)

B_bishop = pygame.image.load(os.path.join('pieces', 'B_bishop.png'))
B_king = pygame.image.load(os.path.join('pieces', 'B_king.png'))
B_knight = pygame.image.load(os.path.join('pieces', 'B_knight.png'))
B_pawn = pygame.image.load(os.path.join('pieces', 'B_pawn.png'))
B_queen = pygame.image.load(os.path.join('pieces', 'B_queen.png'))
B_rook = pygame.image.load(os.path.join('pieces', 'B_rook.png'))

W_bishop = pygame.image.load(os.path.join('pieces', 'W_bishop.png'))
W_king = pygame.image.load(os.path.join('pieces', 'W_king.png'))
W_knight = pygame.image.load(os.path.join('pieces', 'W_knight.png'))
W_pawn = pygame.image.load(os.path.join('pieces', 'W_pawn.png'))
W_queen = pygame.image.load(os.path.join('pieces', 'W_queen.png'))
W_rook = pygame.image.load(os.path.join('pieces', 'W_rook.png'))

class ChessDisplay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ChessBot")
        os.system('cls')

    def inputKey(self, label):
        """
        Capture les entrées clavier dans Pygame pour construire un string.
        - Retourne le texte complet lorsque 'Enter' est pressée.
        - Supprime le dernier caractère avec 'Backspace'.
        """

        text = ""  # String qui contient les lettres saisies
        clock = pygame.time.Clock()

        sys.stdout.write(label)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print("")
                    if not DEBUG and UI_terminal:
                        os.system('cls')
                    print("Thanks for using ChessBot. Bye...")
                    sys.exit(0) # Quitte Pygame si l'utilisateur ferme la fenêtre

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Retourne le texte si 'Enter' est pressée
                        running = False
                    elif event.key == pygame.K_BACKSPACE:  # Supprime la dernière lettre avec 'Backspace'
                        text = text[:-1]
                    else:
                        # Ajoute une lettre si une touche correspondante est pressée
                        char = event.unicode  # Récupère le caractère tapé
                        if char.isprintable():  # Vérifie que c'est un caractère affichable
                            text += char
                    
                    if running:
                        print(end="\r")
                        sys.stdout.write(label)
                        sys.stdout.write(text)
                        sys.stdout.write(" ")
                        sys.stdout.write("\b")
                    else:
                        print("")
                    
            clock.tick(30)  # Limite à 30 FPS

        return text

    def draw_chessboard(self, screen):
        font = pygame.font.Font(None, 20)  # Police pour les numéros de cases
        text_color = (169, 169, 169)  # Gris clair pour les numéros

        for row in range(8):
            for col in range(8):
                # Alterne les couleurs entre noir et blanc
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                if DEBUG:
                    # Numéro de case
                    square_number = row * 8 + col  # Calcul du numéro de case
                    text_surface = font.render(str(square_number), True, text_color)
                    
                    # Positionne le texte en haut à droite de chaque case
                    text_x = (col + 1) * TILE_SIZE - 15  # Décale à droite
                    text_y = row * TILE_SIZE + 5        # Décale en haut
                    screen.blit(text_surface, (text_x, text_y))

        # Ajouter les lettres (a-h) en bas à droite
        for col in range(8):
            letter = chr(ord('a') + col)  # Convertit les colonnes en lettres
            text_surface = font.render(letter, True, text_color)
            text_x = (col + 1) * TILE_SIZE - 15  # Décale à droite
            text_y = HEIGHT - 15  # Bas de la fenêtre
            screen.blit(text_surface, (text_x, text_y))

        # Ajouter les chiffres (1-8) en bas à gauche
        for row in range(8):
            number = str(8 - row)  # Numérotation classique (1 en bas, 8 en haut)
            text_surface = font.render(number, True, text_color)
            text_x = 5  # Décale à gauche
            text_y = row * TILE_SIZE + TILE_SIZE - 15  # Bas de la case
            screen.blit(text_surface, (text_x, text_y))

    def draw_piece(self, board):
        self.screen.blit(W_pawn, (0,0))
        self.screen.blit(B_pawn, (180,0))

    def draw_pieces(self, board):
        for i in range(len(board)):
            x = i%8 * 60
            y = i//8 * 60

            if board[i] == 1:
                self.screen.blit(W_pawn, (x,y))
            if board[i] == 2:
                self.screen.blit(W_rook, (x,y))
            if board[i] == 3:
                self.screen.blit(W_knight, (x,y))
            if board[i] == 4:
                self.screen.blit(W_bishop, (x,y))
            if board[i] == 5:
                self.screen.blit(W_queen, (x,y))
            if board[i] == 6:
                self.screen.blit(W_king, (x,y))

            if board[i] == -1:
                self.screen.blit(B_pawn, (x,y))
            if board[i] == -2:
                self.screen.blit(B_rook, (x,y))
            if board[i] == -3:
                self.screen.blit(B_knight, (x,y))
            if board[i] == -4:
                self.screen.blit(B_bishop, (x,y))
            if board[i] == -5:
                self.screen.blit(B_queen, (x,y))
            if board[i] == -6:
                self.screen.blit(B_king, (x,y))

    def plot(self, board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                if not DEBUG and UI_terminal:
                    os.system('cls')
                print("Thanks for using ChessBot. Bye...")
                sys.exit(0) # Quitte Pygame si l'utilisateur ferme la fenêtre

        # Dessine l'échiquier
        self.draw_chessboard(self.screen)

        # Dessine les pièces
        self.draw_pieces(board)

        # Met à jour l'affichage
        pygame.display.flip()