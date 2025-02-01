import pygame
from .Constants import SQUARE_HEIGHT, SQUARE_WIDTH, LGREY
from .Board import Board
from .Pieces import *

class Game:
    def __init__(self, screen):
        # All the global variables to be used are declared here and some are instances of classes from Piece
        self.board = Board()
        self.pawn = Pawn(Piece)
        self.bishop = Bishop(Piece)
        self.knight = Knight(Piece)
        self.rook = Rook(Piece)
        self.queen = Queen(Piece)
        self.king = King(Piece)
        self.squareSelected = None
        self.turn = 'White' # Initalised to white because white makes the first move
        self.validPieceMoves = []
        self.screen = screen

    # This method is responsible for rendering all the visual displays onto the screen in the internal state
    # It is then called in the main game file to render the visuals on the actual screen
    def UpdateScreen(self):
        self.board.DrawBoard(self.screen)
        self.board.DisplayPieces(self.screen)
        self.DrawValidMoves(self.validPieceMoves)
        pygame.display.update()

    def SelectSquare(self, row, column):
        # checks if a square is selected
        if self.squareSelected:
            finalSquare = self.Move(row, column)
            # Checks if an invalid move has been performed
            if not finalSquare:
                self.squareSelected = None # resets the selected piece
                self.SelectSquare(row, column) # Allow to select again

        piece = self.board.PieceAtSquare(row, column) # Gets the piece attribute from the current row and column
        pieceSquare = self.board.GetPieceSquare(row, column)
        # Dynamically gets the valid moves depending on the piece selected
        # For instance, if piece.name = Queen, it gets self.queen.GetValidMoves and if piece.name = Rook it gets self.rook.GetValidMoves and on
        movesMethod = getattr(self, piece.name.lower()).GetValidMoves
        
        # Checks if the square selected is not an empty square and if the piece selected to move is a piece of the current player 
        if piece != None and piece.colour == self.turn:
            self.squareSelected = pieceSquare
            # Set this variable to store the moves depending on the selected piece
            self.validPieceMoves = movesMethod(self.board.board, row, column)

    def Move(self, row, column):
        # This checks if a piece has been selected and a valid square from its moves has been selected to move to
        if self.squareSelected and (row, column) in self.validPieceMoves:
            self.board.MovePiece(self.squareSelected, row, column) # Performs the piece movement
            self.SwitchTurns()
            return True
        
        return False # If move is invalid it returns false so SelectSquare method can allow re-selection
        
    def DrawValidMoves(self, moves):
        # Loops through all the given moves
        for move in moves:
            row, column = move
            # This is responsible for drawing a light grey circle in the centre of the square
            pygame.draw.circle(self.screen, LGREY, (column * SQUARE_WIDTH + SQUARE_HEIGHT//2, row * SQUARE_HEIGHT + SQUARE_WIDTH//2), 14)
    
    def SwitchTurns(self):
        # Resets the valid moves so the previous players valid moves no longer appears on the screen
        self.validPieceMoves = []
        # This 'if else' block is responsible for switching turns
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'