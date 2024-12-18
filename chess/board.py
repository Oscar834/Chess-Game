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
        else:
            return False

class Board:
    def __init__(self):
        #Initialises the board as an 8x9 grid of squares to allow the pieces to shift one column
        #to the right to stay away from the left-side grey panel and avoid indexing errors later on.
        self.board = [[None for _ in range(9)] for _ in range(8)]

        self.CreateBoard()
        #This method displays all the white pieces
        self.PlacePieces('White')
        #This method displays all the black pieces
        self.PlacePieces('Black')

    def DrawBoard(self, screen, colour):
        #Completely covers the screen in green
        screen.fill(colour)
        for i in range(10):
            #Covers the first column in dark grey
            pygame.draw.rect(screen, DGREY, (0, i * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
        for j in range(10):
            #Covers the last column in dark grey
            pygame.draw.rect(screen, DGREY, (900, j * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
        for rows in range(8):
            #Creates the alternating pattern of white and green
            for columns in range((rows % 2) + 1, 9, 2):
                pygame.draw.rect(screen, WHITE, (columns * SQUARE_WIDTH, rows * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))

    def CreateBoard(self):
        for row in range(8):
            #Required to start from column 1 otherwise some of the pieces would be on the grey panels on the left-side.
            for column in range(1, 9):
                self.board[row][column] = BoardSquares(row, column - 1)

    def PlacePieces(self, colour):
        if colour == 'White':
            #The white pieces occupy the last two rows
            pawnRow = 6
            pieceRow = 7
        else:
            #The black pieces occupy the first two rows
            pawnRow = 1
            pieceRow = 0

        #Places the pawns at their required rows.
        for column in range(1, 9):
            self.board[pawnRow][column] = BoardSquares(pawnRow, column - 1, Pawn(colour))

        #Places the bishops at their designated starting squares
        self.board[pieceRow][3] = BoardSquares(pieceRow, 3, Bishop(colour))
        self.board[pieceRow][6] = BoardSquares(pieceRow, 6, Bishop(colour))

        #Places the knights at their starting squares
        self.board[pieceRow][2] = BoardSquares(pieceRow, 2, Knight(colour))
        self.board[pieceRow][7] = BoardSquares(pieceRow, 7, Knight(colour))

        #Places the Rooks at their starting positions
        self.board[pieceRow][1] = BoardSquares(pieceRow, 1, Rook(colour))
        self.board[pieceRow][8] = BoardSquares(pieceRow, 8, Rook(colour))

        #Places the Queen at its starting square
        self.board[pieceRow][4] = BoardSquares(pieceRow, 4, Queen(colour))

        #Places the King at its starting square
        self.board[pieceRow][5] = BoardSquares(pieceRow, 5, King(colour))

    def DisplayPieces(self, screen):
        for row in range(8):
            for column in range(1, 9):
                    square = self.board[row][column]
                    #Checks if a piece occupies the current row and column
                    if square.PiecePresent():
                        piece = square.piece
                        image = pygame.image.load(piece.image)
                        imageCentre = column * SQUARE_WIDTH + SQUARE_HEIGHT // 2, row * SQUARE_HEIGHT + SQUARE_WIDTH // 2
                        piece.imageRect = image.get_rect(center=imageCentre)
                        screen.blit(image, piece.imageRect)

    def PieceBoardIndex(self, row, column):
        if 0 <= row <= 7 and 1 <= column <= 8:
            return self.board[row][column]

    def MovePiece(self, pieceSquare, newRow, newColumn):
        piece = pieceSquare.piece
        #changes the internal state of the previous square to None so no piece appears on it
        pieceSquare.piece = None
        #Assigns the piece to the new square that it just moved to
        self.board[newRow][newColumn].piece = piece

    def PieceAtSquare(self, row, column):
        if 0 <= row <= 7 and 1 <= column <= 8:
            #assigns the variable square as an instance of the BoardSquares class
            square = self.board[row][column]
            #return the piece attribute of the BoardSquares class
            return square.piece
        
        return None

    def CanCastleKingside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0

        #Starts by checking if the king and rook squares are not empty
        if self.board[row][5].piece != None and self.board[row][8].piece != None and self.board[row][5].piece.name == 'King'\
        and self.board[row][8].piece.name == 'Rook' and self.board[row][5].piece.colour == self.board[row][8].piece.colour\
        and self.board[row][6].piece is None and self.board[row][7].piece is None:
            return True
        
        return False
            
    def CanCastleQueenside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0

        #Starts by checking if the squares of the king and the rook on the left are not empty
        if self.board[row][5].piece != None and self.board[row][1].piece != None and self.board[row][5].piece.name == 'King'\
        and self.board[row][1].piece.name == 'Rook' and self.board[row][5].piece.colour == self.board[row][1].piece.colour\
        and self.board[row][4].piece is None and self.board[row][3].piece is None and self.board[row][2].piece is None:
            return True
        
        return False
            
    def CastleKingside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0
        kingSquare = self.board[row][5]
        rookSquare = self.board[row][8]

        #Checks if kingside castling is possible
        if self.CanCastleKingside(colour):
            if kingSquare.piece.colour == 'White' and rookSquare.piece.colour == 'White':
                #Uses the MovePiece method to simultaneously move both the king and rook to specific squares
                self.MovePiece(kingSquare, row, 7)
                self.MovePiece(rookSquare, row, 6)
            elif kingSquare.piece.colour == 'Black' and rookSquare.piece.colour == 'Black':
                self.MovePiece(kingSquare, row, 7)
                self.MovePiece(rookSquare, row, 6)
        
    def CastleQueenside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0
        kingSquare = self.board[row][5]
        rookSquare = self.board[row][1]

        #Checks if kingside castling is possible
        if self.CanCastleQueenside(colour):
            if kingSquare.piece.colour == 'White' and rookSquare.piece.colour == 'White':
                #Uses the MovePiece method to simultaneously move both the king and rook to specific squares
                self.MovePiece(kingSquare, row, 3)
                self.MovePiece(rookSquare, row, 4)
            elif kingSquare.piece.colour == 'Black' and rookSquare.piece.colour == 'Black':
                self.MovePiece(kingSquare, row, 3)
                self.MovePiece(rookSquare, row, 4)

    def Promotion(self, colour, screen):
        #This makes it so that it promotes if the pawn reaches the opponents end of the board
        if colour == 'White':
            row = 0
        elif colour == 'Black':
            row = 7

        for column in range(1, 9):
            #Stores the board object of the squares of each opponents starting row
            square = self.board[row][column]
            #Stores a queen piece object
            queen = BoardSquares(row, column, Queen(colour))

            #This checks if the piece on the square of the opponents starting row is a pawn
            if square.piece is not None and square.piece.name == 'Pawn' and square.piece.colour == colour:
                square.piece = queen.piece #Replaces the pawn object with the queen object
                #These next lines are then responsible for displaying the queen on that square
                piece = square.piece
                image = pygame.image.load(piece.image)
                imageCentre = column * SQUARE_WIDTH + SQUARE_HEIGHT // 2, row * SQUARE_HEIGHT + SQUARE_WIDTH // 2
                piece.imageRect = image.get_rect(center=imageCentre)
                screen.blit(image, piece.imageRect)

    def WhiteValue(self):
        materialValue = 0

        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece != None and self.board[row][column].piece.colour == 'White':
                    materialValue += self.board[row][column].piece.value

        return materialValue
    
    def BlackValue(self):
        materialValue = 0

        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece != None and self.board[row][column].piece.colour == 'White':
                    materialValue += self.board[row][column].piece.value

        return materialValue

    def evaluate(self):
        return self.WhiteValue() - self.BlackValue()
   