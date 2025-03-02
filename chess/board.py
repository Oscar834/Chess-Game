import pygame
from .Constants import WHITE, SQUARE_WIDTH, SQUARE_HEIGHT, DGREY
from .Pieces import *

class BoardSquares:
    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece

    def PiecePresent(self):
        #Checks if there is a piece at the current square
        if self.piece != None:
            return True
        
        return False

class Board:
    def __init__(self):
        #Initialises the board as an 8x9 2D array to allow the pieces to shift one column
        #to the right to stay away from the left-side grey panel and avoid indexing errors later on.
        self.board = [[None for _ in range(9)] for _ in range(8)]

        self.CreateBoard() # Calls the method responsible for assigning a piece object to each square on the board
        # This method places all the white pieces on their starting squares internally
        self.PlacePieces('White')
        # This method places all the black pieces on their starting squares internally
        self.PlacePieces('Black')

    def DrawBoard(self, screen, colour): 
        # Completely covers the screen in the chosen colour 
        screen.fill(colour) 
        for i in range(10):
            # Covers the first column in dark grey
            pygame.draw.rect(screen, DGREY, (0, i * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
        for j in range(10):
            # Covers the last column in dark grey
            pygame.draw.rect(screen, DGREY, (900, j * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
        for rows in range(8):
            # Creates the alternating pattern of white and the chosen colour
            for columns in range((rows % 2) + 1, 9, 2):
                pygame.draw.rect(screen, WHITE, (columns * SQUARE_WIDTH, rows * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))

    def CreateBoard(self):
        for row in range(8):
            # Required to start from column 1 otherwise some of the pieces would be on the grey panels on the left-side.
            for column in range(1, 9):
                # Assigns a piece object on each square of the board
                self.board[row][column] = BoardSquares(row, column - 1)

    def PlacePieces(self, colour):
        if colour == 'White':
            # The white pieces occupy the last two rows
            pawnRow = 6
            pieceRow = 7
        else:
            # The black pieces occupy the first two rows
            pawnRow = 1
            pieceRow = 0

        # Places the pawns at their required rows.
        for column in range(1, 9):
            self.board[pawnRow][column] = BoardSquares(pawnRow, column - 1, Pawn(colour))

        # Places the bishops at their designated starting squares
        self.board[pieceRow][3] = BoardSquares(pieceRow, 3, Bishop(colour))
        self.board[pieceRow][6] = BoardSquares(pieceRow, 6, Bishop(colour))

        # Places the knights at their starting squares
        self.board[pieceRow][2] = BoardSquares(pieceRow, 2, Knight(colour))
        self.board[pieceRow][7] = BoardSquares(pieceRow, 7, Knight(colour))

        # Places the Rooks at their starting positions
        self.board[pieceRow][1] = BoardSquares(pieceRow, 1, Rook(colour))
        self.board[pieceRow][8] = BoardSquares(pieceRow, 8, Rook(colour))

        # Places the Queen at its starting square
        self.board[pieceRow][4] = BoardSquares(pieceRow, 4, Queen(colour))

        # Places the King at its starting square
        self.board[pieceRow][5] = BoardSquares(pieceRow, 5, King(colour))

    def DisplayPieces(self, screen):
        for row in range(8):
            for column in range(1, 9):
                    square = self.board[row][column]
                    # Checks if a piece occupies the current row and column
                    if square.PiecePresent():
                        piece = square.piece
                        image = pygame.image.load(piece.image) # Loads the piece image using the piece class
                        imageCentre = (column * SQUARE_WIDTH + SQUARE_HEIGHT // 2, row * SQUARE_HEIGHT + SQUARE_WIDTH // 2)
                        piece.imageRect = image.get_rect(center=imageCentre)
                        screen.blit(image, piece.imageRect) # Displays the piece onto the screen

    def GetPieceSquare(self, row, column):
        # Ensures it stays within the bounds of the board to prevent errors
        if 0 <= row <= 7 and 1 <= column <= 8:
            return self.board[row][column] # Returns the square of the board at the given row and column. (N.B each square has a piece attribute)

    def MovePiece(self, pieceSquare, newRow, newColumn):
        piece = pieceSquare.piece
        # Changes the internal state of the previous square to None so no piece appears on it
        pieceSquare.piece = None
        # Assigns the piece to the new square that it just moved to
        self.board[newRow][newColumn].piece = piece

    def PieceAtSquare(self, row, column):
        if 0 <= row <= 7 and 1 <= column <= 8:
            # Assigns the variable square as the value return from the GetPieceSquare method
            square = self.GetPieceSquare(row, column)
            return square.piece # Return the piece attribute stored at the current square
        
        return None
    
    def CanCastleKingside(self, colour):
        # Checks the colour to determine the row correctly
        if colour == 'White':
            row = 7
        else:
            row = 0

        # Checks if the the King and kingside rook are on their starting squares and there are no pieces between them
        # and also checks that they are the same colour of the current player to prevent a player from castling on is opponent's side
        if self.board[row][5].piece != None and self.board[row][8].piece != None and self.board[row][5].piece.name == 'King'\
        and self.board[row][8].piece.name == 'Rook' and self.board[row][5].piece.colour == colour\
        and self.board[row][8].piece.colour == colour and self.board[row][6].piece == None and self.board[row][7].piece == None:
            return True
        
        return False
            
    def CanCastleQueenside(self, colour):
        # Checks the colour to determine the row correctly
        if colour == 'White':
            row = 7
        else:
            row = 0

        # Checks if the the King and queenside rook are on their starting squares and there are no pieces between them
        # and also checks that they are the same colour of the current player to prevent a player from castling on is opponent's side
        if self.board[row][5].piece != None and self.board[row][1].piece != None and self.board[row][5].piece.name == 'King'\
        and self.board[row][1].piece.name == 'Rook' and self.board[row][5].piece.colour == colour and self.board[row][1].piece.colour == colour\
        and self.board[row][4].piece == None and self.board[row][3].piece == None and self.board[row][2].piece == None:
            return True
        
        return False
            
    def CastleKingside(self, colour):
        # Checks the colour to determine the row correctly
        if colour == 'White':
            row = 7
        else:
            row = 0

        kingSquare = self.board[row][5] # Stores the starting square of the king so it can move the piece stored there
        rookSquare = self.board[row][8] # Stores the starting square of the king's rook so it can move the piece stored there

        # Checks if kingside castling is possible
        if self.CanCastleKingside(colour):
            # Uses the MovePiece method to simultaneously move both the king and rook to the kingside castle position
            self.MovePiece(kingSquare, row, 7)
            self.MovePiece(rookSquare, row, 6)

    def CastleQueenside(self, colour):
        # Checks the colour to determine the row correctly
        if colour == 'White':
            row = 7
        else:
            row = 0

        kingSquare = self.board[row][5] # Stores the starting square of the king so it can move the piece stored there
        rookSquare = self.board[row][1] # Stores the starting square of the queen's rook so it can move the piece stored there

        # Checks if queenside castling is possible
        if self.CanCastleQueenside(colour):
            # Uses the MovePiece method to simultaneously move both the king and rook to the queenside castle position
            self.MovePiece(kingSquare, row, 3)
            self.MovePiece(rookSquare, row, 4)

    def Promote(self, row, column, colour):
        # Checks if a player has reached the end of the board (the starting row of their opponent)
        if (colour == 'White' and row == 0) or (colour == 'Black' and row == 7):
            self.board[row][column] = BoardSquares(row, column, Queen(colour)) # Places a queen on the square

    def EnPassant(self, square, row, column, colour):
        # Uses the piece colour to determine what row the removed pawn should be on
        if colour == 'White':
            dir = 1
        else:
            dir = -1

        self.MovePiece(square, row, column) # Moves the pawn normally to that square
        self.Remove(row + dir, column) # Removes the opponent pawn to complete the enPassant movement

    # This method removes the piece on the row and column passed to it
    def Remove(self, row, column):
        square = self.board[row][column]
        square.piece = None # By setting the piece attribute to None, the piece is removed