import pygame
from .constants import WHITE, GREEN, SQUARE_WIDTH, SQUARE_HEIGHT, DGREY
from .pieces import *

class Board_Squares:
    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece

    def piece_present(self):
        #Checks if there is a piece at the current square
        if self.piece != None:
            return True
        else:
            return False

class Board:
    def __init__(self):
        #Initialises the board as an 8x9 grid of squares to allow the pieces to shift one column
        #to the right to stay away from the left-side grey panel and avoid indexing errors later on.
        self.board = [[None for _ in range(9)] for _ in range(8)]

        self.create_board()
        #This method displays all the white pieces
        self.place_Pieces('White')
        #This method displays all the black pieces
        self.place_Pieces('Black')

    def draw_board(self, screen):
        #Completely covers the screen in green
        screen.fill(GREEN)
        for i in range(10):
            #Covers the first column in dark grey
            pygame.draw.rect(screen, (DGREY), (0, i * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
        for j in range(10):
            #Covers the last column in dark grey
            pygame.draw.rect(screen, DGREY, (900, j * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
        for rows in range(8):
            #Creates the alternating pattern of white and green
            for columns in range((rows % 2) + 1, 9, 2):
                pygame.draw.rect(screen, WHITE, (columns * SQUARE_WIDTH, rows * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))

    def create_board(self):
        for row in range(8):
            #Required to start from column 1 otherwise some of the pieces would be on the grey panels on the left-side.
            for column in range(1, 9):
                self.board[row][column] = Board_Squares(row, column - 1)

    def place_Pieces(self, colour):
        if colour == 'White':
            #The white pieces occupy the last two rows
            pawn_Row = 6
            piece_Row = 7
        else:
            #The black pieces occupy the first two rows
            pawn_Row = 1
            piece_Row = 0

        #Places the pawns at their required rows.
        for column in range(1, 9):
            self.board[pawn_Row][column] = Board_Squares(pawn_Row, column - 1, Pawn(colour))

        #Places the bishops at their designated starting squares
        self.board[piece_Row][3] = Board_Squares(piece_Row, 3, Bishop(colour))
        self.board[piece_Row][6] = Board_Squares(piece_Row, 6, Bishop(colour))

        #Places the knights at their starting squares
        self.board[piece_Row][2] = Board_Squares(piece_Row, 2, Knight(colour))
        self.board[piece_Row][7] = Board_Squares(piece_Row, 7, Knight(colour))

        #Places the Rooks at their starting positions
        self.board[piece_Row][1] = Board_Squares(piece_Row, 1, Rook(colour))
        self.board[piece_Row][8] = Board_Squares(piece_Row, 8, Rook(colour))

        #Places the Queen at its starting square
        self.board[piece_Row][4] = Board_Squares(piece_Row, 4, Queen(colour))

        #Places the King at its starting square
        self.board[piece_Row][5] = Board_Squares(piece_Row, 5, King(colour))

    def display_BoardnPieces(self, screen):
        for row in range(8):
            for column in range(1, 9):
                    square = self.board[row][column]
                    #Checks if a piece occupies the current row and column
                    if square.piece_present():
                        piece = square.piece
                        image = pygame.image.load(piece.image)
                        imageCentre = column * SQUARE_WIDTH + SQUARE_HEIGHT // 2, row * SQUARE_HEIGHT + SQUARE_WIDTH // 2
                        piece.image_rect = image.get_rect(center=imageCentre)
                        screen.blit(image, piece.image_rect)

    def get_piece_position(self, row, column):
        if 0 <= row <= 7 and 1 <= column <= 8:
            return self.board[row][column]

    def move_piece(self, piece_square, new_row, new_column):
        piece = piece_square.piece
        #changes the internal state of the previous square to None so no piece appears on it
        piece_square.piece = None
        #Assigns the piece to the new square that it just moved to
        self.board[new_row][new_column].piece = piece

    def get_piece_at_square(self, row, column):
        if 0 <= row < 8 and 1 <= column <= 8:
            #assigns the variable square as an instance of the Board_Squares class
            square = self.board[row][column]
            #return the piece attribute of the Board_Squares class
            return square.piece
        else:
            return None

    def can_castle_kingside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0
        #Starts by checking if the king and rook squares are not empty
        if self.board[row][5].piece != None and self.board[row][8].piece != None:
            #Initial conditions for kingside castling for white
            if self.board[row][5].piece.name == 'King'\
            and self.board[row][8].piece.name == 'Rook'\
            and self.board[row][5].piece.colour == self.board[row][8].piece.colour\
            and self.board[row][6].piece is None\
            and self.board[row][7].piece is None:
                return True
            else:
                return False
            
    def can_castle_queenside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0
        #Starts by checking if the squares of the king and the rook on the left are not empty
        if self.board[row][5].piece != None and self.board[row][1].piece != None:
            #Initial conditions for queenside castling for white
            if self.board[row][5].piece.name == 'King'\
            and self.board[row][1].piece.name == 'Rook'\
            and self.board[row][5].piece.colour == self.board[row][1].piece.colour\
            and self.board[row][4].piece is None\
            and self.board[row][3].piece is None\
            and self.board[row][2].piece is None:
                return True
            else:
                return False
            
    def castle_kingside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0
        king_square = self.board[row][5]
        rook_square = self.board[row][8]

        #Checks if kingside castling is possible
        if self.can_castle_kingside(colour):
            if king_square.piece.colour == 'White' and rook_square.piece.colour == 'White':
                #Uses the move_piece method to simultaneously move both the king and rook to specific squares
                self.move_piece(king_square, row, 7)
                self.move_piece(rook_square, row, 6)
            elif king_square.piece.colour == 'Black' and rook_square.piece.colour == 'Black':
                self.move_piece(king_square, row, 7)
                self.move_piece(rook_square, row, 6)
        
    def castle_queenside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0
        king_square = self.board[row][5]
        rook_square = self.board[row][1]

        #Checks if kingside castling is possible
        if self.can_castle_queenside(colour):
            if king_square.piece.colour == 'White' and rook_square.piece.colour == 'White':
                #Uses the move_piece method to simultaneously move both the king and rook to specific squares
                self.move_piece(king_square, row, 3)
                self.move_piece(rook_square, row, 4)
            elif king_square.piece.colour == 'Black' and rook_square.piece.colour == 'Black':
                self.move_piece(king_square, row, 3)
                self.move_piece(rook_square, row, 4)

    def promotion(self, colour, screen):
        #This makes it so that it promotes if the pawn reaches the opponents end of the board
        if colour == 'White':
            row = 0
        elif colour == 'Black':
            row = 7

        for column in range(1, 9):
            #Stores the board object of the squares of each opponents starting row
            square = self.board[row][column]
            #Stores a queen piece object
            queen = Board_Squares(row, column, Queen(colour))

            #This checks if the piece on the square of the opponents starting row is a pawn
            if square.piece is not None and square.piece.name == 'Pawn' and square.piece.colour == colour:
                square.piece = queen.piece #Replaces the pawn object with the queen object
                #These next lines are then responsible for displaying the queen on that square
                piece = square.piece
                image = pygame.image.load(piece.image)
                imageCentre = column * SQUARE_WIDTH + SQUARE_HEIGHT // 2, row * SQUARE_HEIGHT + SQUARE_WIDTH // 2
                piece.image_rect = image.get_rect(center=imageCentre)
                screen.blit(image, piece.image_rect)

    def get_king_position(self, colour):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'King'\
                and self.board[row][column].piece.colour == colour:
                    return row, column

    def get_first_pawn_position(self, colour):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_second_pawn_position(self, colour):
        first_pawn = self.get_first_pawn_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                #Skips the first pawn
                if (row, column) == first_pawn:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_third_pawn_position(self, colour):
        first_pawn = self.get_first_pawn_position(colour)
        second_pawn = self.get_second_pawn_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                #Skips the first and second pawn
                if (row, column) == first_pawn or (row, column) == second_pawn:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_fourth_pawn_position(self, colour):
        first_pawn = self.get_first_pawn_position(colour)
        second_pawn = self.get_second_pawn_position(colour)
        third_pawn = self.get_third_pawn_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                #Skips the first, second and third pawn and so on.. for the remaining methods
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_fifth_pawn_position(self, colour):
        first_pawn = self.get_first_pawn_position(colour)
        second_pawn = self.get_second_pawn_position(colour)
        third_pawn = self.get_third_pawn_position(colour)
        fourth_pawn = self.get_fourth_pawn_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_sixth_pawn_position(self, colour):
        first_pawn = self.get_first_pawn_position(colour)
        second_pawn = self.get_second_pawn_position(colour)
        third_pawn = self.get_third_pawn_position(colour)
        fourth_pawn = self.get_fourth_pawn_position(colour)
        fifth_pawn = self.get_fifth_pawn_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn\
                or (row, column) == fifth_pawn:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_seventh_pawn_position(self, colour):
        first_pawn = self.get_first_pawn_position(colour)
        second_pawn = self.get_second_pawn_position(colour)
        third_pawn = self.get_third_pawn_position(colour)
        fourth_pawn = self.get_fourth_pawn_position(colour)
        fifth_pawn = self.get_fifth_pawn_position(colour)
        sixth_pawn = self.get_sixth_pawn_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn\
                or (row, column) == fifth_pawn\
                or (row, column) == sixth_pawn:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_eighth_pawn_position(self, colour):
        first_pawn = self.get_first_pawn_position(colour)
        second_pawn = self.get_second_pawn_position(colour)
        third_pawn = self.get_third_pawn_position(colour)
        fourth_pawn = self.get_fourth_pawn_position(colour)
        fifth_pawn = self.get_fifth_pawn_position(colour)
        sixth_pawn = self.get_sixth_pawn_position(colour)
        seventh_pawn = self.get_seventh_pawn_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn\
                or (row, column) == fifth_pawn\
                or (row, column) == sixth_pawn\
                or (row, column) == seventh_pawn:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Pawn'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                    
    def get_light_bishop_position(self, colour):
        for row in range(0, 8):
            for column in range(1, 9):
                #Checks if the square is not empty and the colour is not the turn of whoever is playing
                #because you only want to the check the position of the enemy pieces for the king.
                if self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Bishop'\
                and self.board[row][column].piece.colour == colour\
                and (row + column) % 2 == 1:#This checks if the the bishop is a light squared bishop
                    return row, column
                 
    def get_dark_bishop_position(self, colour):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Bishop'\
                and self.board[row][column].piece.colour == colour\
                and (row + column) % 2 == 0:#Checks if the bishop is a dark squared bishop
                    return row, column
                
    def get_first_knight_position(self, colour):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Knight'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_second_knight_position(self, colour):
        result = self.get_first_knight_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                #This check is necessary because you will always encounter the first knight first so the for loop just skips
                #this row and column when checking to ensure it gets the second knight
                if (row, column) == result:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Knight'\
                and self.board[row][column].piece.colour == colour:
                    return row, column  

    def get_first_rook_position(self, colour):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Rook'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_second_rook_position(self, colour):
        result = self.get_first_rook_position(colour)
        for row in range(0, 8):
            for column in range(1, 9):
                #Similar thought process for the knights
                if (row, column) == result:
                    continue
                elif self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Rook'\
                and self.board[row][column].piece.colour == colour:
                    return row, column
                
    def get_queen_position(self, colour):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece is not None\
                and self.board[row][column].piece.name == 'Queen'\
                and self.board[row][column].piece.colour == colour:
                    return row, column

    
                
                
    

    







    
       
        
        
            

    
    

    







                

                    


        