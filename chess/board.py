import pygame
from .Constants import WHITE, SQUARE_WIDTH, SQUARE_HEIGHT, DGREY
from .Pieces import *
import math

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

    def Display(self, board):
        board_str = ""
        for row in board.board:
            board_str += " ".join(
                square.piece.name[0] if square and square.piece else "." for square in row[1:]
            ) + "\n"
        print(board_str)

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
            # Creates the alternating pattern of white and green
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
                    #Checks if a piece occupies the current row and column
                    if square.PiecePresent():
                        piece = square.piece
                        image = pygame.image.load(piece.image) # Loads the piece image using the piece class
                        imageCentre = column * SQUARE_WIDTH + SQUARE_HEIGHT // 2, row * SQUARE_HEIGHT + SQUARE_WIDTH // 2
                        piece.imageRect = image.get_rect(center=imageCentre)
                        screen.blit(image, piece.imageRect) # Displays the piece onto the screen

    def GetPiece(self, row, column):
        # Ensures it stays within the bounds of the board to prevent errors
        if 0 <= row <= 7 and 1 <= column <= 8:
            return self.board[row][column]

    def MovePiece(self, pieceSquare, newRow, newColumn):
        piece = pieceSquare.piece
        # Changes the internal state of the previous square to None so no piece appears on it
        pieceSquare.piece = None
        # Assigns the piece to the new square that it just moved to
        self.board[newRow][newColumn].piece = piece

    def PieceAtSquare(self, row, column):
        if 0 <= row <= 7 and 1 <= column <= 8:
            # Assigns the variable square as an instance of the BoardSquares class
            square = self.board[row][column]
            # Return the piece attribute of the BoardSquares class
            return square.piece
        
        return None

    def CanCastleKingside(self, colour):
        if colour == 'White':
            row = 7
        else:
            row = 0

        # Checks if the the King and kingside rook are on their starting squares and there are no pieces between them
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

        # Checks if the the King and queenside rook are on their starting squares and there are no pieces between them
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
        kingSquare = self.board[row][5] # Stores the piece object on the king's starting square
        rookSquare = self.board[row][8] # Stores the piece object on the kingisde rook's starting square

        # Checks if kingside castling is possible
        if self.CanCastleKingside(colour):
            if kingSquare.piece.colour == 'White' and rookSquare.piece.colour == 'White':
                # Uses the MovePiece method to simultaneously move both the king and rook to specific squares
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
        kingSquare = self.board[row][5] # Stores the piece object on the king's starting square
        rookSquare = self.board[row][1] # Stores the piece object on the queenside rook's starting square

        # Checks if kingside castling is possible
        if self.CanCastleQueenside(colour):
            if kingSquare.piece.colour == 'White' and rookSquare.piece.colour == 'White':
                # Uses the MovePiece method to simultaneously move both the king and rook to specific squares
                self.MovePiece(kingSquare, row, 3)
                self.MovePiece(rookSquare, row, 4)
            elif kingSquare.piece.colour == 'Black' and rookSquare.piece.colour == 'Black':
                self.MovePiece(kingSquare, row, 3)
                self.MovePiece(rookSquare, row, 4)

    def Promotion(self, colour, screen):
        # This checks if a pawn has reached the opponents first row (the end of the board)
        if colour == 'White':
            row = 0
        elif colour == 'Black':
            row = 7

        for column in range(1, 9):
            # Stores the board object of the squares of each opponents starting row
            square = self.board[row][column]
            # Stores a queen piece object
            queen = BoardSquares(row, column, Queen(colour))

            #This checks if the piece on the square of the opponents first row is a pawn
            if square.piece != None and square.piece.name == 'Pawn' and square.piece.colour == colour:
                square.piece = queen.piece # Replaces the pawn object with the queen object

                # These next lines are then responsible for displaying the queen on that square
                piece = square.piece
                image = pygame.image.load(piece.image)
                imageCentre = column * SQUARE_WIDTH + SQUARE_HEIGHT // 2, row * SQUARE_HEIGHT + SQUARE_WIDTH // 2
                piece.imageRect = image.get_rect(center=imageCentre)
                screen.blit(image, piece.imageRect)

    def Remove(self, row, column):
        square = self.board[row][column]
        square.piece = None
    
    def Material(self, colour):
        materialValue = 0

        for row in range(0, 8):
            for column in range(1, 9):
                if self.board[row][column].piece != None and self.board[row][column].piece.colour == colour:
                    materialValue += self.board[row][column].piece.value

        return materialValue
    
    def PiecePositions(self, piece, colour):
        pieces = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
        positions = []

        for row in range(0, 8):
            for column in range(1, 9):
                # Row and column for enemy piece added to positions list
                if self.board[row][column].piece != None and self.board[row][column].piece.name == piece\
                and self.board[row][column].piece.colour == colour:
                    positions.append((row, column))

                    for key, value in zip(pieces.keys(), positions):
                        pieces[key] = value

        return pieces

    def Positional(self, colour):
        value = 0
        if colour == 'White':
            row = 4
        else:
            row = 3
        centralSquares = [(row, 3), (row, 4), (row, 5)]

        for val in centralSquares:
            for values in self.PiecePositions('Pawn', colour).values():
                if values == val:
                    value += 2
            #if self.board[val[0]][val[1]].piece != None and self.board[val[0]][val[1]].piece.name == 'Pawn'\
            #and self.board[val[0]][val[1]].piece.colour == colour:
                #value += 2

        return value
    
    def Evaluate(self):
        materialCount = self.Material('White') - self.Material('Black')
        return materialCount + (self.Positional('White') - self.Positional('Black'))
    
    def HardEvaluation(self, game):
        numMoves = 0
        centralSquares = [(4, 3), (4, 4), (4, 5), (4, 6)]
        positionalScore = 0

        for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
            validMoves = game.PieceMoves(piece, 'Black')

            for move in validMoves.values():
                numMoves += len(move)

        pawnMoves = game.PieceMoves('Pawn', 'Black')

        for moves in pawnMoves.values():
            for move in moves:
                if move in centralSquares:
                    positionalScore += 3

        mobilityScore = math.log(numMoves)
        kingRow, kingColumn = game.PiecePositions('King', 'Black').get(1)
        queenMoves = game.queen.GetValidMoves(game.board.board, kingRow, kingColumn)
        mobilityScore -= 0.5 * len(queenMoves)

        return mobilityScore + self.Material('Black') + positionalScore
