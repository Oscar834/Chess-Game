import pygame
from .Constants import SQUARE_HEIGHT, SQUARE_WIDTH, LGREY
from .Board import Board
from .Pieces import *

class Game:
    def __init__(self, screen):
        # All the global variables to be used are declared here and some are instances of piece classes
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
    def UpdateScreen(self, colour):
        self.board.DrawBoard(self.screen, colour)
        self.board.DisplayPieces(self.screen)
        #Promotion is called here for white and for black for visual display
        self.board.Promotion('White', self.screen)
        self.board.Promotion('Black', self.screen)
        self.DrawValidMoves(self.validPieceMoves)
    
    def PiecePositions(self, piece, colour):
        # Dictionary which stores the row and column of the piece as the value and the piece number as the key
        pieces = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
        positions = []

        # The two for loops check all squares on the board
        for row in range(0, 8):
            for column in range(1, 9):
                # Checks if a piece with name as the piece parameter has been encountered and checks
                # if the piece colour is the same as the colour parameter.
                if self.board.board[row][column].piece != None and self.board.board[row][column].piece.name == piece\
                and self.board.board[row][column].piece.colour == colour:
                    positions.append((row, column)) # Adds the row and column as a tuple to the positions list

                    # Uses the values in the positions list and adds them IN TURN to be the value of the keys in the dictionary
                    # For instance, if positions = [(1, 1), (2, 1)], then pieces would be {1: (1, 1), 2: (2, 1), 3: None} and so on
                    for key, value in zip(pieces.keys(), positions):
                        pieces[key] = value

        return pieces
    
    def PieceMoves(self, piece, colour):
        moves = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        squares = []

        # Checks if the piece is a king
        if piece == 'King':
            kingRow, kingColumn = self.PiecePositions('King', colour).get(1)
            # Adds the King moves to the squares list including cases where his movement is restricted
            squares.append(self.NewKingMoves(kingRow, kingColumn, colour)) 

            # Assigns the value in the squares list to the key '1' because there can only be one king
            for key, value in zip(moves.keys(), squares):
                moves[key] = value

        # This is responsible for adding the moves of every other piece
        else:
            # This for loop ensures every possible piece is checked
            for num in range(1, 10):
                piecePosition = self.PiecePositions(piece, colour).get(num)
                # Checks if the piece exists
                if piecePosition != None:
                    pieceRow, pieceColumn = piecePosition
                    # Adds the updated moves for the piece to the squares list
                    squares.append(self.NewPieceMoves(pieceRow, pieceColumn, piece, colour))

                    # Assigns the value at each position in the squares to become the value of the corresponding key in the dictionary
                    for key, value in zip(moves.keys(), squares):
                        moves[key] = value

        return moves
    
    def KeyFromPosition(self, dict, position):
        # Loops through all key value pairs in the dictionary passed
        for key, value in dict.items():
            if value == position:
                return key # Returns the key from the value
            
        return None
    
    def AllPieceMoves(self):
        positions = []
        moves = []
        for row in range(0, 8):
            for column in range(1, 9):
                # This adds the positions of all the pieces of the current player to the positions list
                if self.board.board[row][column].piece != None and self.board.board[row][column].piece.colour == self.turn:
                    positions.append((row, column))

        # This loops through all the values in the positions list and gets the piece attribute using the row and column
        for pos in positions:
            piece = self.board.PieceAtSquare(pos[0], pos[1])
            # Depending on the piece, it adds it moves to the moves list accordingly
            if piece.name != 'King':
                moves.extend(self.NewPieceMoves(pos[0], pos[1], piece.name))
            else:
                moves.extend(self.NewKingMoves(pos[0], pos[1]))

        return moves
    
    def Checkmate(self, colour): # The colour parameter is used so I can identify the colour of the king that got checkmated
        # Checks if the King is in check
        if self.InCheck() != None and colour == self.turn:
            # Checks if the player has no moves indicating checkmate as the king is in check
            if self.AllPieceMoves() == []:
                return True
        
        return False
    
    def Stalemate(self):
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)
        # Checks if the King cannot move
        if self.NewKingMoves(kingRow, kingColumn) == []:
            # Checks if the King is not in check but the player has no moves indicating Stalemate
            if self.InCheck() == None and self.AllPieceMoves() == []:
                return True
        
        return False

    def PlayerPieces(self, colour):
        pieceValues = []

        # The two for loops check every single square on the board
        for row in range(0, 8):
            for column in range(1, 9):
                square = self.board.board[row][column]
                # Checks if the there is a piece on the square and the piece is not a king
                if square.piece != None and square.piece.colour == colour and square.piece.name != 'King':
                    # Adds the values of the white or black pieces depending on colcour to the piece values list
                    pieceValues.append(square.piece.value) 

        return pieceValues

    def AllPieces(self):
        pieceValues = []
        
        # The two for loops check every single square on the board
        for row in range(0, 8):
            for column in range(1, 9):
                square = self.board.board[row][column]
                # Checks if the there is a piece on the square and the piece is not a king
                if square.piece != None and square.piece.name != 'King':
                    pieceValues.append(square.piece.value) # Adds the value of the piece to the piece values list

        return pieceValues

    def InsufficientMaterial(self):
        whitePieces = self.PlayerPieces('White') # Stores the piece values of all white pieces excluding the king
        blackPieces = self.PlayerPieces('Black') # Stores the piece values of all black pieces excluding the king
        allPieces = self.AllPieces() # Stores the piece values of all pieces excluding the king
        pawnValue = 1

        # Checks if only kings are left or kings and 1 bishop or knight is left
        if allPieces == [] or (len(allPieces) == 1 and 3 <= allPieces[0] <= 3.5):
            return True
        
        # Checks if two pieces aside from the king's are left and no pawns
        elif len(allPieces) == 2 and pawnValue not in allPieces:
            # Checks if a knight or bishop for both players exist
            if 6 <= sum(allPieces) <= 7 and len(whitePieces) != 0  and len(blackPieces) != 0:
                return True
            
            # Checks if only two knights are left for a single player 
            elif sum(allPieces) == 6:
                return True
        
        return False
    
    def TerminalCondition(self):
        if self.Checkmate('White') or self.Checkmate('Black') or self.Stalemate() or self.InsufficientMaterial():
            return True
        
        return False
    
    def GetBoard(self):
        return self.board # Returns the board object so it can be used with the AI
    
    def AIBoard(self, board):
        self.board = board # Reassigns self.board so it now holds the new board object passed to the method

    def SelectSquare(self, row, column):
        # Checks if a square is selected
        if self.squareSelected:
            finalSquare = self.Move(row, column)
            # Checks if an invalid move has been performed
            if not finalSquare:
                self.validPieceMoves = [] # Clear the valid moves if an invalid square has been selected so they are not displayed
                self.squareSelected = None # resets the selected piece
                self.SelectSquare(row, column) # Allow to select again

        piece = self.board.PieceAtSquare(row, column) # Gets the piece attribute from the current row and column
        pieceSquare = self.board.GetPieceSquare(row, column)

        # Checks if the selected square contains a king that is the colour of the current player
        if piece != None and piece.name == 'King' and piece.colour == self.turn:
            self.squareSelected = pieceSquare
            # Set this variable to the new method (NewKingMoves) so it accounts for the removal of moves.
            self.validPieceMoves = self.NewKingMoves(row, column, piece.colour)

        # Checks if a square containing any other piece of the current player has been selected
        elif piece != None and piece.colour == self.turn:
            self.squareSelected = pieceSquare
            # Sets this variable so it now accounts for restriction of piece movement depending on the piece selected
            self.validPieceMoves = self.NewPieceMoves(row, column, piece.name, piece.colour)

    def Move(self, row, column):
        # Checks if the selected piece to move is a King and the kingside castle square is selected to move to
        if self.squareSelected.piece != None and self.squareSelected.piece.name == 'King' and (row == 7 or row == 0)\
        and column == 7 and self.board.CanCastleKingside(self.turn) and (row, column) in self.validPieceMoves:
            self.board.CastleKingside(self.turn) # Performs kingside castling
            self.SwitchTurns() # After a move has been made, it switches turns so the other player can make a move

        # Checks if the selected piece to move is a King and the queenside castle square is selected to move to
        elif self.squareSelected.piece != None and self.squareSelected.piece.name == 'King' and (row == 7 or row == 0)\
        and column == 3 and self.board.CanCastleQueenside(self.turn) and (row, column) in self.validPieceMoves:
            self.board.CastleQueenside(self.turn) # Performs queenside castling
            self.SwitchTurns()

        # This is the block responsible for every other move and checking if a piece has been selected
        elif self.squareSelected and (row, column) in self.validPieceMoves:
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

    def NewKingMoves(self, row, column, colour):
        if colour == 'White':
            oppColour = 'Black'
            castlingRow = 7 # White starts the bottom 
        else:
            oppColour = 'White'
            castlingRow = 0 # Black starts at the top

        kingMoves = self.king.GetValidMoves(self.board.board, row, column)
        shortCastleMoves = self.king.GetShortCastleMoves(self.board.board, row, column)
        longCastleMoves = self.king.GetLongCastleMoves(self.board.board, row, column)
        
        # Checks if kingside castle conditions are met and the King is not in check
        if self.board.CanCastleKingside(self.turn):
            kingMoves.extend(shortCastleMoves) # Adds the castle move to the valid moves

        # Checks if queenside castle conditions are met and the King is not in check
        if self.board.CanCastleQueenside(self.turn):
            kingMoves.extend(longCastleMoves) # Adds the castle move to the valid moves

        # This is to store the control moves of every piece
        enemyPieceData = {'King': [], 'Queen': [], 'Rook': [], 'Bishop': [], 'Knight': [], 'Pawn': []} 
        
        for number in range(1, 10):
            for piece in ['King', 'Queen', 'Rook','Bishop', 'Knight', 'Pawn']: 
                position = self.PiecePositions(piece, oppColour).get(number) # Gets the position of each enemy piece from the key in the dictionary
                # Checks if the piece exists
                if position != None:
                    pieceRow, pieceColumn = position
                    # Dynamically gets the method to calculate control moves for the given piece
                    controlMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds a dictionary to the list for each piece in the enemy piece data dictionary which holds the control moves
                    # of each piece in the enemyPieceData dictionary
                    enemyPieceData[piece].append({'controlMoves': controlMovesMethod(self.board.board, pieceRow, pieceColumn, 'Control')})

        # Loops through all the values (the lists) in the enemy piece data dictionary
        for pieceData in enemyPieceData.values():
            # Loops through the dictionaries in the lists
            for enemyData in pieceData:
                controlMoves = enemyData['controlMoves']

                # Loops through all the initial valid King moves and removes any that are in the control moves of an enemy piece
                for move in kingMoves[:]:
                    if self.board.board[row][column].piece.colour == colour and move in controlMoves: 
                        kingMoves.remove(move)

                    # This prevents kingside castling through a controlled square
                    if move == (castlingRow, 7) and move in kingMoves and (castlingRow, 6) in controlMoves\
                    and self.board.CanCastleKingside(self.turn) and self.board.board[row][column].piece.colour == colour:
                        kingMoves.remove(move)

                    # This prevents queenside castling through a controlled square
                    if move == (castlingRow, 3) and move in kingMoves and (castlingRow, 4) in controlMoves\
                    and self.board.CanCastleQueenside(colour) and self.board.board[row][column].piece.colour == colour:
                        kingMoves.remove(move)

        return kingMoves
    
    def NewPieceMoves(self, row, column, name, colour):
        # Allows to easily get friendly or enemy pieces by passing the colour/oppColour to PiecePositions
        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        # Dynamically gets the method to calculate valid moves for the given piece
        movesMethod = getattr(self, name.lower()).GetValidMoves
        validMoves = movesMethod(self.board.board, row, column)
        updatedValidMoves = []
        checkingPiecePosition = self.CheckingPiecePosition(colour) # This holds the position of the piece giving the check
        blockMoves = self.BlockCheckMoves(colour) # This stores the different moves for blocking a check
        piecePositions = self.PiecePositions(name, colour) # Holds the dictionary which stores the positions of the given piece
        kingRow, kingColumn = self.PiecePositions('King', colour).get(1)

        # Gets the key of each piece using KeyFromPosition method and with their current row and column
        pieceKey = self.KeyFromPosition(piecePositions, (row, column)) 

        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': []}
        
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop']:
                position = self.PiecePositions(piece, oppColour).get(number) # Gets the position of the enemy bishop, rook or queen
                if position != None:
                    pieceRow, pieceColumn = position
                    # Dynamically gets the method to calculate moves for each piece
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds to each list for each piece (key) in the enemyPieceData dict another dictionary which holds the position,
                    # the validMoves and the pinMoves of that piece
                    enemyPieceData[piece].append({
                        'position': position,
                        'validMoves': validMovesMethod(self.board.board, pieceRow, pieceColumn),
                        'pinMoves': validMovesMethod(self.board.board, pieceRow, pieceColumn, 'Pin')
                    })

        # Checks if the piece is pinned and the king is in check
        if self.PiecePinned(name, pieceKey) and self.InCheck() != None:
            updatedValidMoves = []

        # Checks if the King is in double check
        elif self.InCheck() == 'double':
            updatedValidMoves = [] # No other piece apart from the king should be allowed to move in a double check
            
        # Checks if the King is in check by a single piece
        elif self.InCheck() == 'single':
            # This checks if the checking piece is in the valid moves of the selected piece and makes it the ONLY valid move if so
            if checkingPiecePosition in validMoves:
                updatedValidMoves = [checkingPiecePosition]

            # This loops through all the possible blocking squares and checks if they are in valid moves of the selected piece and adds them if so
            for move in blockMoves:
                if move in validMoves:
                    updatedValidMoves.append(move)

        # This checks if the King is not in check and the selected piece is not pinned
        elif self.InCheck() == None and self.PiecePinned(name, pieceKey) != True:
            updatedValidMoves = validMoves

        # This else block is responsible for handling piece movement restriction when pinned depending on how the pin is and what piece is pinned
        else:
            # Loops through key, value pairs in the enemyPieceData dictionary
            for enemyPiece, pieceData in enemyPieceData.items():
                # Loops through each dictionary in each value (list)
                for enemyData in pieceData:
                    # Assigns to variables the values stored in the embedded dictionary for each piece depending on the key
                    pieceRow, pieceColumn = enemyData['position']
                    pieceMoves = enemyData['validMoves']
                    pinMoves = enemyData['pinMoves']

                    # This handles queen movement restriction when pinned
                    if name == 'Queen' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        # Checks if the pinning piece is a queen or rook 
                        if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                            # Checks if the queen is pinned horizontally
                            if row == pieceRow:
                                for move in pinMoves:
                                    if move in validMoves and move[0] == row:
                                        updatedValidMoves.append(move) # Adds only moves on the row and none else
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves

                            # Checks if the queen is pinned vertically
                            elif column == pieceColumn:
                                for move in pinMoves:
                                    if move in validMoves and move[1] == column:
                                        updatedValidMoves.append(move) # Adds only moves on the column and none else
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves

                        # Checks if the pinning piece is a bishop or queen
                        if enemyPiece == 'Bishop' or enemyPiece == 'Queen':
                            # Checks if the queen is pinend in the bottom left to top right diagonal or vice versa
                            if (kingRow < pieceRow and kingColumn > pieceColumn) or (kingRow > pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] + move[1] == row + column:
                                        updatedValidMoves.append(move) # Adds only moves on the diagonal
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves

                            # Checks if the queen is pinned in the bottom right to top left diagonal or vice versa
                            elif (kingRow > pieceRow and kingColumn > pieceColumn) or (kingRow < pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] != pieceRow and move[1] != pieceColumn and move[0] != row and move[1] != column:
                                        updatedValidMoves.append(move) # Adds only moves on the diagonal
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves
    
                    # This handles rook movement restriction when pinned
                    if name == 'Rook' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        # Checks if the rook is pinned by a queen or rook
                        if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                            # Checks if the rook is pinned horizontally
                            if row == pieceRow:
                                for move in pinMoves:
                                    if move in validMoves and move[0] == row:
                                        updatedValidMoves.append(move) # Adds only moves on the row and none else
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves

                            # Checks if the rook is pinned vertically
                            elif column == pieceColumn:
                                for move in pinMoves:
                                    if move in validMoves and move[1] == column:
                                        updatedValidMoves.append(move) # Adds only moves on the column and none else
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves
                        
                        # Checks if the rook is pinned by a queen or bishop diagonally
                        if (enemyPiece == 'Queen' or enemyPiece == 'Bishop') and row != pieceRow and column != pieceColumn:
                            updatedValidMoves = []

                    # This handles knight movement restriction when pinned
                    if name == 'Knight' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        updatedValidMoves = []

                    # This handles bishop movement restriction when pinned
                    if name == 'Bishop' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        # Checks if the bishop is pinned by a queen or bishop 
                        if (enemyPiece == 'Bishop' or enemyPiece == 'Queen'):
                            # Checks if the bishop is pinned in the bottom left to top right diagonal or vice versa
                            if (kingRow < pieceRow and kingColumn > pieceColumn) or (kingRow > pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] + move[1] == row + column:
                                        updatedValidMoves.append(move) # Adds only moves on the diagonal
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves

                            # Checks if the bishop is pinned in the bottom right to top left diagonal or vice versa
                            elif (kingRow > pieceRow and kingColumn > pieceColumn) or (kingRow < pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] != pieceRow and move[1] != pieceColumn:
                                        updatedValidMoves.append(move) # Adds only moves on the diagonal
                                updatedValidMoves.append((pieceRow, pieceColumn)) # Adds the pinning piece to the updatedValidMoves

                        # Checks if the bishop is pinned by a rook or queen horizontally or vertically
                        if (enemyPiece == 'Queen' or enemyPiece == 'Rook') and (row == pieceRow or column == pieceColumn):
                            updatedValidMoves = []

                    # This handles pawn movement restriction when pinned
                    if name == 'Pawn' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        # Checks if the pawn is pinned by a queen or rook
                        if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                            # Checks if the pawn is pinned vertically
                            if column == pieceColumn:
                                for move in pinMoves:
                                    if move in validMoves and move[1] == column:
                                        updatedValidMoves.append(move) # Adds only moves on the column and none else so no diagonal captures

                            # Checks if the pawn is pinned horizontally
                            elif row == pieceRow:
                                updatedValidMoves = []

                        # Checks if the pawn is pinned by a bishop or queen diagonally
                        if (enemyPiece == 'Bishop' or enemyPiece == 'Queen') and (row != pieceRow and column != pieceColumn):
                            if (pieceRow, pieceColumn) in validMoves:
                                updatedValidMoves = [(pieceRow, pieceColumn)] # Pawn can only capture pinning piece if in valid moves
                            else:
                                updatedValidMoves = [] # Otherwise it cannot move
        return updatedValidMoves
    
    def InCheck(self):
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)
        count = 0 # Variable to track the number of pieces 'checking' the king

        # Dictionary which holds data of all pieces that can give a check
        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': [], 'Knight': [], 'Pawn': []}
        
        # Loops through 1 to 9 so all key and values in the EnemyPiecePosition dictionary can be accessed
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop', 'Knight', 'Pawn']:
                position = self.EnemyPiecePosition(piece).get(number) # Gets the piece position from the key in the piece positions dict.
                if position != None:
                    pieceRow, pieceColumn = position
                    # Dynamically gets the method to calculate valid moves for each piece
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds to the list for each piece in the enemyPieceData dict its valid moves
                    enemyPieceData[piece].append({'validMoves': validMovesMethod(self.board.board, pieceRow, pieceColumn)})

        # Loops through all the values (lists) in the enemyPieceData dictionary
        for pieceData in enemyPieceData.values():
            # Loops through all the dictionaries in each list so it can access the valid moves of all enemy pieces
            for enemyData in pieceData:
                validMoves = enemyData['validMoves']

                # Checks if the King's position is in the valid moves of any enemy piece
                if (kingRow, kingColumn) in validMoves:
                    count += 1 # Increments the count by 1

        # Checks if the king is checked by two pieces (i.e through a discovered check)
        if count == 2:
            return 'double'
        # Checks if the king is checked by a single piece
        elif count == 1:
            return 'single'
        
        return None # Returns None if not in check
    
    def CheckingPiecePosition(self):
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)

        # The two for loops ensure every single enemy piece is checked (excluding the king) so its current position and moves can be accessed
        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
                oppPiecePosition = self.EnemyPiecePosition(piece).get(number)

                # Checks if the piece exists
                if oppPiecePosition != None:
                    oppPieceRow, oppPieceColumn = oppPiecePosition
                    # Dynamically gets the method to calculate valid moves for each enemy piece
                    movesMethod = getattr(self, piece.lower()).GetValidMoves
                    oppPieceMoves = movesMethod(self.board.board, oppPieceRow, oppPieceColumn)
                else:
                    oppPieceMoves = []

                # This checks if the King is in the enemy piece's moves and returns the position of the checking piece
                if (kingRow, kingColumn) in oppPieceMoves:
                    return oppPieceRow, oppPieceColumn
                
    def BlockCheckMoves(self):
        moves = []
        enemyPiecePosition = self.CheckingPiecePosition() # Gets the position of the enemy piece giving the check
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)

        # Checks if the king is in check indirectly by checking if a checking piece exists
        if enemyPiecePosition != None:
            enemyPieceRow, enemyPieceColumn = enemyPiecePosition
            pieceObject = self.board.PieceAtSquare(enemyPieceRow, enemyPieceColumn) # Gets the piece object from the row and column
            piece = pieceObject.name
            # Dynamically gets the method for calculating the valid moves of the piece
            movesMethod = getattr(self, piece.lower()).GetValidMoves

            # Checks if the checking piece is a queen or a bishop and the 'check' is done diagonally
            if (piece == 'Queen' or piece == 'Bishop') and (enemyPieceRow != kingRow and enemyPieceColumn != kingColumn):
                # Checks if the king is in the bottom right direction of the queen
                if enemyPieceRow < kingRow and enemyPieceColumn < kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(enemyPieceRow + 1, kingRow):
                        for column in range(enemyPieceColumn + 1, kingColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, enemyPieceRow, enemyPieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the bottom left direction of the queen
                elif enemyPieceRow < kingRow and enemyPieceColumn > kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(enemyPieceRow + 1, kingRow):
                        for column in range(kingColumn + 1, enemyPieceColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, enemyPieceRow, enemyPieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the top right direction of the queen
                elif enemyPieceRow > kingRow and enemyPieceColumn < kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(kingRow + 1, enemyPieceRow):
                        for column in range(enemyPieceColumn + 1, kingColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, enemyPieceRow, enemyPieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the top left direction of the queen
                elif enemyPieceRow > kingRow and enemyPieceColumn > kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(kingRow + 1, enemyPieceRow):
                        for column in range(kingColumn + 1, enemyPieceColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, enemyPieceRow, enemyPieceColumn):
                                moves.append((row, column))

            # Checks if the checking piece is a queen or a rook and the 'check' is done rectilinearly
            if (piece == 'Queen' or piece == 'Rook') and (enemyPieceRow == kingRow or enemyPieceColumn == kingColumn):
                # Checks if the king is below the rook and they are both on the same column
                if enemyPieceRow < kingRow and enemyPieceColumn == kingColumn:
                    # This for loop is then used to check all the squares between the king and the rook and then adds them to moves
                    for row in range(enemyPieceRow + 1, kingRow):
                        moves.append((row, enemyPieceColumn))

                # Checks if the king is above the rook and they're on the same column
                elif enemyPieceRow > kingRow and enemyPieceColumn == kingColumn:
                    # This also checks all the squares between the king and rook and adds them to moves
                    for row in range(kingRow + 1, enemyPieceRow):
                        moves.append((row, enemyPieceColumn))

                # Checks if the king and rook are on the same row and the king is to the right of the rook
                elif enemyPieceRow == kingRow and enemyPieceColumn < kingColumn:
                    # Adds all the squares between the king and rook in this scenario to moves
                    for column in range(enemyPieceColumn + 1, kingColumn):
                        moves.append((enemyPieceRow, column))

                # Checks if the king and rook are on the same row and the king is to the left of the rook
                elif enemyPieceRow == kingRow and enemyPieceColumn > kingColumn:
                    # Adds all the squares between the king and rook to moves
                    for column in range(kingColumn + 1, enemyPieceColumn):
                        moves.append((enemyPieceRow, column))

        return moves
    
    def PiecePinned(self, name, key):
        kingInSight = False

        piecePosition = self.FriendlyPiecePosition(name).get(key)
        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': []}

        if piecePosition != None:
            pieceRow, pieceColumn = piecePosition

        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)

        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop']:
                position = self.EnemyPiecePosition(piece).get(number)
                if position != None:
                    enemyPieceRow, enemyPieceColumn = position
                    # Dynamically gets the method for calculating the moves of each enemy piece
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds to each list for each piece (key) in the enemyPieceData dict another dictionary which holds the position,
                    # the validMoves and the pinMoves of that piece
                    enemyPieceData[piece].append({
                        'position': position,
                        'validMoves': validMovesMethod(self.board.board, enemyPieceRow, enemyPieceColumn),
                        'pinMoves': validMovesMethod(self.board.board, enemyPieceRow, enemyPieceColumn, 'Pin')
                    })

        # Loops through all the key, value pairs of the enemyPieceData dictionary
        for enemyPiece, pieceData in enemyPieceData.items():
            # Loops through all the dictionaries in each value (list)
            for enemydata in pieceData:
                enemyPieceRow, enemyPieceColumn = enemydata['position']
                enemyPieceMoves = enemydata['validMoves']
                enemyPinMoves = enemydata['pinMoves']

                # Handles conditions for checking if a piece is pinned by a queen or rook rectilinearly
                if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                    # Checks if the piece is on the same vertical file as the king and rook and the king is below the rook
                    if (pieceColumn == enemyPieceColumn == kingColumn) and (enemyPieceRow < pieceRow < kingRow)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for row in range(pieceRow + 1, kingRow):
                            # Checks if the squares between the piece and king are not empty or the king is directly below the piece
                            if self.board.board[row][enemyPieceColumn].piece != None:
                                squaresEmpty = False
                                break
                        
                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty:
                            return True
                        
                    # Checks if the piece is on the same row as the king and rook and the king is to the left of the rook
                    elif (pieceRow == enemyPieceRow == kingRow) and (kingColumn < pieceColumn < enemyPieceColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for column in range(kingColumn + 1, pieceColumn):
                            # Checks if the squares between the piece and king are not empty or the king is directly to the left of the piece
                            if self.board.board[enemyPieceRow][column].piece != None:
                                squaresEmpty = False
                                break
                            
                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty:
                            return True
                        
                    # This is similar to the if block but just checks if the king is above instead of below 
                    elif (pieceColumn == enemyPieceColumn == kingColumn) and (kingRow < pieceRow < enemyPieceRow)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for row in range(kingRow + 1, pieceRow):
                            # Checks if the squares between the piece and the king are not empty or the king is directly above the piece
                            if self.board.board[row][enemyPieceColumn].piece != None:
                                squaresEmpty = False
                                break

                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty:
                            return True
                        
                    # This is similar to the previous elif block but just checks if the king is to the right instead of the left of the rook or queen
                    elif (pieceRow == enemyPieceRow == kingRow) and (enemyPieceColumn < pieceColumn < kingColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for column in range(pieceColumn + 1, kingColumn):
                            # This checks if the squares between the king and the piece are not empty or the king is directly to the right of the piece
                            if self.board.board[enemyPieceRow][column].piece != None:
                                squaresEmpty = False
                                break

                        # This then checks if both condtions have been satisfied for the piece to be considered pinned 
                        if kingInSight and squaresEmpty:
                            return True

                # Handles conditions for checking if a piece is pinned by a queen or bishop diagonally
                if enemyPiece == 'Queen' or enemyPiece == 'Bishop':
                    # This checks if the piece is between the bishop and king in the top-left to bottom-right diagonal
                    if (enemyPieceRow < pieceRow < kingRow) and (enemyPieceColumn < pieceColumn < kingColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = kingRow - pieceRow

                        for i in range(1, squares): 
                            # This ensures that only diagonals are considered
                            row  = pieceRow + i 
                            column = pieceColumn + i
                            # This checks if the squares between the piece and king are occupied 
                            if self.board.board[row][column].piece != None: 
                                squaresEmpty = False 
                                break 

                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty: 
                            return True

                    # This checks if the piece is between the bishop and king in the top-right to bottom-left diagonal
                    elif (enemyPieceRow < pieceRow < kingRow) and (kingColumn < pieceColumn < enemyPieceColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = kingRow - pieceRow

                        # Uses same logic as previous elif block
                        for i in range(1, squares):
                            # This ensures the only the diagonals are checked
                            row  = pieceRow + i
                            column = pieceColumn - i

                            # This checks if the squares between the piece and king are occupied
                            if self.board.board[row][column].piece != None:
                                squaresEmpty = False
                                break
                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty:
                            return True
                    
                    # This checks if the piece is between the bishop and king in the bottom-left to top-right diagonal
                    elif (kingRow < pieceRow < enemyPieceRow) and (enemyPieceColumn < pieceColumn < kingColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = pieceRow - kingRow

                        # Uses same logic as previous elif block
                        for i in range(1, squares):
                            # This ensures the only the diagonals are checked.
                            row  = pieceRow - i
                            column = pieceColumn + i

                            # This checks if the squares between the piece and king are occupied
                            if self.board.board[row][column].piece != None:
                                squaresEmpty = False
                                break
                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty:
                            return True
                        
                    # This checks if the piece is between the bishop and king in the bottom-right to top-left diagonal
                    elif (kingRow < pieceRow < enemyPieceRow) and (kingColumn < pieceColumn < enemyPieceColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = pieceRow - kingRow

                        # Uses same logic as previous elif block
                        for i in range(1, squares):
                            #This ensures the only the diagonals are checked.
                            row  = pieceRow - i
                            column = pieceColumn - i

                            # This checks if the squares between the piece and king are occupied
                            if self.board.board[row][column].piece != None:
                                squaresEmpty = False
                                break
                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty:
                            return True
                
