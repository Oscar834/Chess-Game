from .Pieces import *
import math
from. Board import Board

class AIGame:
    def __init__(self):
        self.board = Board()
        self.pawn = Pawn(Piece)
        self.bishop = Bishop(Piece)
        self.knight = Knight(Piece)
        self.rook = Rook(Piece)
        self.queen = Queen(Piece)
        self.king = King(Piece)
        self.squareSelected = None
        self.turn = 'White'
        self.validPieceMoves = []
    
    def PiecePositions(self, board, piece, colour):
        pieces = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
        positions = []

        for row in range(0, 8):
            for column in range(1, 9):
                # Row and column for enemy piece added to positions list
                if board.board[row][column].piece != None and board.board[row][column].piece.name == piece\
                and board.board[row][column].piece.colour == colour:
                    positions.append((row, column))

                    for key, value in zip(pieces.keys(), positions):
                        pieces[key] = value

        return pieces

    def PieceMoves(self, board, piece, colour):
        moves = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        squares = []

        if piece == 'King':
            kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)
            # Adds the King moves to the squares list including cases where his movement is restricted
            squares.append(self.NewKingMoves(board, kingRow, kingColumn, colour)) 

            # Assigns the value in the squares list to the key '1' because there can only be one king
            for key, value in zip(moves.keys(), squares):
                moves[key] = value

        else:
            for num in range(1, 10):
                piecePosition = self.PiecePositions(board, piece, colour).get(num)
                if piecePosition != None:
                    pieceRow, pieceColumn = piecePosition
                    # Adds the updated moves for the piece to the squares list
                    squares.append(self.NewPieceMoves(board, pieceRow, pieceColumn, piece, colour))

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

    def CheckingPiecePosition(self, board, colour):
        positions = []
        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
                # Adds the position of any piece giving the check to the positions list
                positions.append(self.PieceCheck(board, piece, number, colour))

        return positions
    
    def BlockMoves(self, board, colour):
        moves = []
        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop']:
                # Adds the appropriate blocking moves to the moves list depending on the piece giving the check
                moves.extend(self.BlockPieceCheck(board, piece, number, colour))

        return moves
    
    def AllPieceMoves(self, board, colour):
        positions = []
        moves = []
        for row in range(0, 8):
            for column in range(1, 9):
                # This adds the positions of all the pieces of the current player to the positions list
                if board.board[row][column].piece != None and board.board[row][column].piece.colour == colour:
                    positions.append((row, column))

        # This loops through all the values now in the positions list and gets the piece using the row and column
        for pos in positions:
            piece = board.PieceAtSquare(pos[0], pos[1])
            # Depending on the piece, it adds it moves to the moves list accordingly
            if piece.name != 'King':
                moves.extend(self.NewPieceMoves(board, pos[0], pos[1], piece.name, colour))
            else:
                moves.extend(self.NewKingMoves(board, pos[0], pos[1], colour))

        return moves
    
    def PieceDefenseMoves(self, board, colour):
        positions = []
        moves = []
        for row in range(0, 8):
            for column in range(1, 9):
                # This adds the positions of all the pieces of the current player to the positions list
                if board.board[row][column].piece != None and board.board[row][column].piece.colour == colour:
                    positions.append((row, column))

        # This loops through all the values now in the positions list and gets the piece using the row and column
        for pos in positions:
            piece = board.PieceAtSquare(pos[0], pos[1])
            movesMethod = getattr(self, piece.name.lower()).GetValidMoves
            # Depending on the piece, it adds it moves to the moves list accordingly
            moves.extend(movesMethod(board.board, pos[0], pos[1], 'Control'))

        return moves
    
    def Checkmate(self, board, colour):
        # Checks if the King is in check and whose turn it is
        if self.InCheck(board, colour) != None and colour == self.turn:
            # Checks if the list from AllPieceMoves is empty indicating checkmate as the king is in check
            if self.AllPieceMoves(board, colour) == []:
                return True
        
        return False
    
    def Stalemate(self, board):
        kingRow, kingColumn = self.PiecePositions(board, 'King', self.turn).get(1)
        # Checks if the King cannot move
        if self.NewKingMoves(board, kingRow, kingColumn, self.turn) == []:
            # Checks if the King is not in check but the AllMovesPiece list is empty indicating Stalemate
            if self.InCheck(board, self.turn) == None and self.AllPieceMoves(board, self.turn) == []:
                return True
        
        return False

    def PlayerPieces(self, board, colour):
        playerPieces = []

        for row in range(0, 8):
            for column in range(1, 9):
                # Adds the names of all the pieces of the white or black player (depending on colour) to the playerPieces list
                if board.board[row][column].piece != None and board.board[row][column].piece.colour == colour:
                    playerPieces.append(board.board[row][column].piece.name)

        return playerPieces
    
    def AllPieces(self, board):
        allPieces = []
        
        for row in range(0, 8):
            for column in range(1, 9):
                # Adds the name of all the pieces of every single piece on the board
                if board.board[row][column].piece != None:
                    allPieces.append(board.board[row][column].piece.name)

        return allPieces

    def InsufficientMaterial(self, board):
        whitePieces = self.PlayerPieces(board, 'White')
        blackPieces = self.PlayerPieces(board, 'Black')
        allPieces = self.AllPieces(board)

        if allPieces.count('King') == 2 and allPieces.count('Pawn') == 0 and allPieces.count('Knight') == 0\
        and allPieces.count('Bishop') == 0 and allPieces.count('Rook') == 0 and allPieces.count('Queen') == 0:
            return True
        
        elif allPieces.count('King') == 2 and allPieces.count('Pawn') == 0 and allPieces.count('Knight') == 1\
        and allPieces.count('Bishop') == 0 and allPieces.count('Rook') == 0 and allPieces.count('Queen') == 0:
            return True
        
        elif allPieces.count('King') == 2 and allPieces.count('Pawn') == 0 and allPieces.count('Knight') == 0\
        and allPieces.count('Bishop') == 1 and allPieces.count('Rook') == 0 and allPieces.count('Queen') == 0:
            return True
        
        elif allPieces.count('King') == 2 and allPieces.count('Pawn') == 0 and whitePieces.count('Knight') == 1\
        and whitePieces.count('Bishop') == 0 and blackPieces.count('Bishop') == 1 and blackPieces.count('Knight') == 0\
        and allPieces.count('Rook') == 0 and allPieces.count('Queen') == 0:
            return True
        
        elif allPieces.count('King') == 2 and allPieces.count('Pawn') == 0 and whitePieces.count('Knight') == 0\
        and whitePieces.count('Bishop') == 1 and blackPieces.count('Bishop') == 0 and blackPieces.count('Knight') == 1\
        and allPieces.count('Rook') == 0 and allPieces.count('Queen') == 0:
            return True
        
        elif allPieces.count('King') == 2 and allPieces.count('Pawn') == 0 and whitePieces.count('Knight') == 0\
        and whitePieces.count('Bishop') == 1 and blackPieces.count('Bishop') == 1 and blackPieces.count('Knight') == 0\
        and allPieces.count('Rook') == 0 and allPieces.count('Queen') == 0:
            return True
        
        elif allPieces.count('King') == 2 and allPieces.count('Pawn') == 0 and allPieces.count('Knight') == 2\
        and allPieces.count('Bishop') == 0 and allPieces.count('Rook') == 0 and allPieces.count('Queen') == 0:
            return True
        
        return False
    
    def GetBoard(self):
        return self.board # Returns the board object so it can be used with the AI

    def AIBoard(self, board):
        self.board = board
    
    def SwitchTurns(self):
        # Resets the valid moves so the previous players valid moves no longer appears on the screen
        self.validPieceMoves = []
        # This 'if else' block is responsible for switching turns
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'

    def NewKingMoves(self, board, row, column, colour):
        if colour == 'White':
            oppColour = 'Black'
            rows = 7
        else:
            oppColour = 'White'
            rows = 0
        kingMoves = self.king.GetValidMoves(board.board, row, column)
        shortCastleMoves = self.king.GetShortCastleMoves(board.board, row, column)
        longCastleMoves = self.king.GetLongCastleMoves(board.board, row, column)
        oppKingRow, oppKingColumn = self.PiecePositions(board, 'King', oppColour).get(1)
        kingControlMoves = self.king.GetValidMoves(board.board, oppKingRow, oppKingColumn, 'Control')
        
        # Checks if kingside castle conditions are met and the King is not in check
        if board.CanCastleKingside(colour) and self.InCheck(board, colour) == None:
            kingMoves.extend(shortCastleMoves) # Adds the castle moves to the valid moves

        # Checks if queenside castle conditions are met and the King is not in check
        if board.CanCastleQueenside(colour) and self.InCheck(board, colour) == None:
            kingMoves.extend(longCastleMoves) # Adds the castle moves to the valid moves

        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': [], 'Knight': [], 'Pawn': []}
        
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop', 'Knight', 'Pawn']:
                position = self.PiecePositions(board, piece, oppColour).get(number) # Gets the position of each piece from the key in the dictionary
                if position != None:
                    pieceRow, pieceColumn = position
                    # Dynamically gets the method to calculate control moves for the given piece
                    controlMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds a dictionary which hold the control to the list of each piece in the enemyPieceData dictionary
                    enemyPieceData[piece].append({
                        'controlMoves': controlMovesMethod(board.board, pieceRow, pieceColumn, 'Control')
                    })

        # Loops through all the values in the enemy piece data dictionary
        for pieceData in enemyPieceData.values():
            for enemyData in pieceData:
                controlMoves = enemyData['controlMoves']

                # Loops through all the initial valid King moves and removes any that are in the control moves of an enemy piece
                for move in kingMoves[:]:
                    if board.board[row][column].piece.colour == colour and (move in controlMoves or move in kingControlMoves):
                        kingMoves.remove(move)

                    # This prevents kingside castling through a check
                    if move == (rows, 7) and move in kingMoves and ((rows, 6) in controlMoves or (rows, 6) in kingControlMoves)\
                    and board.CanCastleKingside(colour) and board.board[row][column].piece.colour == colour:
                        kingMoves.remove((rows, 7))

                    # This prevents queenside castling through a check
                    if move == (rows, 3) and move in kingMoves and ((rows, 4) in controlMoves or (rows, 4) in kingControlMoves)\
                    and board.CanCastleQueenside(colour) and board.board[row][column].piece.colour == colour:
                        kingMoves.remove((rows, 3))
        return kingMoves

    def NewPieceMoves(self, board, row, column, name, colour):
        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        # Dynamically gets the method to calculate control moves for the given piece
        movesMethod = getattr(self, name.lower()).GetValidMoves
        validMoves = movesMethod(board.board, row, column)
        updatedValidMoves = []
        piecePositions = self.PiecePositions(board, name, colour) # Holds the dictionary which stores the positions of the given piece
        pieceKey = self.KeyFromPosition(piecePositions, (row, column)) # Gets the key of each piece using KeyFromPosition method
        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)

        #This holds the positions of the pieces giving the check
        positions = self.CheckingPiecePosition(board, colour)

        #This stores the list of the different moves for blocking a queen, rook or bishop check
        blockMoves = self.BlockMoves(board, colour)

        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': []}
        
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop']:
                position = self.PiecePositions(board, piece, oppColour).get(number)
                if position != None:
                    pieceRow, pieceColumn = position
                    # Dynamically gets the method to calculate moves for each piece
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds to each list for each piece (key) in the enemyPieceData dict another dictionary which holds the position,
                    # the validMoves and the pinMoves of that piece
                    enemyPieceData[piece].append({
                        'position': position,
                        'validMoves': validMovesMethod(board.board, pieceRow, pieceColumn),
                        'pinMoves': validMovesMethod(board.board, pieceRow, pieceColumn, 'Pin')
                    })

        # Checks if the piece is pinned and the king is in check
        if self.PiecePinned(board, name, pieceKey, colour) and self.InCheck(board, colour) != None:
            updatedValidMoves = []

        # Checks if the King is in double check
        elif self.InCheck(board, colour) == 'double':
            updatedValidMoves = []
            
        # Checks if the King is in check by a single piece
        elif self.InCheck(board, colour) == 'single':
            # This checks if the checking piece is in the valid moves of the selected piece and adds it to the updatedValidMoves list
            for position in positions:
                if position in validMoves:
                    updatedValidMoves = [position]

            # This loops through all the possible blocking squares and adds them to the updatedValidMoves list
            for move in blockMoves:
                if move in validMoves:
                    updatedValidMoves.append(move)

        # This checks if the King is not in check and the selected piece is not pinned
        elif self.InCheck(board, colour) == None and self.PiecePinned(board, name, pieceKey, colour) != True:
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
    
    def InCheck(self, board, colour):
        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)
        count = 0 # Variable to track the number of enemy pieces that the King's position is in

        # Dictionary which holds data of all pieces that can give a check
        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': [], 'Knight': [], 'Pawn': []}
        
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop', 'Knight', 'Pawn']:
                position = self.PiecePositions(board, piece, oppColour).get(number) # Gets the piece position from the key in the EnemyPiecePositon dict.
                if position != None:
                    pieceRow, pieceColumn = position
                    # Dynamically gets the method to calculate valid moves for each piece
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds to the list for each piece in the enemyPieceData dict its valid moves
                    enemyPieceData[piece].append({
                        'validMoves': validMovesMethod(board.board, pieceRow, pieceColumn)
                    })

        # Loops through all the values (lists) in the enemyPieceData dictionary
        for pieceData in enemyPieceData.values():
            # Loops through all the dictionaries in each list
            for enemyData in pieceData:
                validMoves = enemyData['validMoves']

                # Checks if the King's position is in the valid moves of any enemy piece
                if (kingRow, kingColumn) in validMoves:
                    count += 1 # Increments the count by 1

        # Checks if the King's position is in the valid moves of two enemy pieces
        if count == 2:
            return 'double'
        # Checks if the King's position is in the valid move of a single enemy piece
        elif count == 1:
            return 'single'
        
        return None # Else it returns None

    def PieceCheck(self, board, piece, number, colour):
        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        oppPiecePosition = self.PiecePositions(board, piece, oppColour).get(number)
        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)

        if oppPiecePosition != None:
            oppPieceRow, oppPieceColumn = oppPiecePosition
            # Dynamically gets the method to calculate valid moves for each enemy piece
            movesMethod = getattr(self, piece.lower()).GetValidMoves
            oppPieceMoves = movesMethod(board.board, oppPieceRow, oppPieceColumn)
        else:
            oppPieceMoves = []

        # This checks if the King is in the enemy piece's moves and returns the position of the checking piece
        if (kingRow, kingColumn) in oppPieceMoves:
            return oppPieceRow, oppPieceColumn
        
    def BlockPieceCheck(self, board, piece, number, colour):
        moves = []
        piecePosition = self.PieceCheck(board, piece, number, colour)
        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)
        movesMethod = getattr(self, piece.lower()).GetValidMoves

        if piecePosition != None:
            pieceRow, pieceColumn = piecePosition

            # Checks if the checking piece is a queen or a bishop and the 'check' is done diagonally
            if (piece == 'Queen' or piece == 'Bishop') and (pieceRow != kingRow and pieceColumn != kingColumn):
                # Checks if the king is in the bottom right direction of the queen
                if pieceRow < kingRow and pieceColumn < kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(pieceRow + 1, kingRow):
                        for column in range(pieceColumn + 1, kingColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the bottom left direction of the queen
                elif pieceRow < kingRow and pieceColumn > kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(pieceRow + 1, kingRow):
                        for column in range(kingColumn + 1, pieceColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the top right direction of the queen
                elif pieceRow > kingRow and pieceColumn < kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(kingRow + 1, pieceRow):
                        for column in range(pieceColumn + 1, kingColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the top left direction of the queen
                elif pieceRow > kingRow and pieceColumn > kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(kingRow + 1, pieceRow):
                        for column in range(kingColumn + 1, pieceColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

            # Checks if the checking piece is a queen or a rook and the 'check' is done rectilinearly
            if (piece == 'Queen' or piece == 'Rook') and (pieceRow == kingRow or pieceColumn == kingColumn):
                # Checks if the king is below the rook and they are both on the same column
                if pieceRow < kingRow and pieceColumn == kingColumn:
                    # This for loop is then used to check all the squares between the king and the rook and then adds them to moves
                    for row in range(pieceRow + 1, kingRow):
                        moves.append((row, pieceColumn))

                # Checks if the king is above the rook and they're on the same column
                elif pieceRow > kingRow and pieceColumn == kingColumn:
                    # This also checks all the squares between the king and rook and adds them to moves
                    for row in range(kingRow + 1, pieceRow):
                        moves.append((row, pieceColumn))

                # Checks if the king and rook are on the same row and the king is to the right of the rook
                elif pieceRow == kingRow and pieceColumn < kingColumn:
                    # Adds all the squares between the king and rook in this scenario to moves
                    for column in range(pieceColumn + 1, kingColumn):
                        moves.append((pieceRow, column))

                # Checks if the king and rook are on the same row and the king is to the left of the rook
                elif pieceRow == kingRow and pieceColumn > kingColumn:
                    # Adds all the squares between the king and rook to moves
                    for column in range(kingColumn + 1, pieceColumn):
                        moves.append((pieceRow, column))

        return moves
    
    def PiecePinned(self, board, name, key, colour):
        kingInSight = False

        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        piecePosition = self.PiecePositions(board, name, colour).get(key)
        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': []}

        if piecePosition != None:
            pieceRow, pieceColumn = piecePosition

        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)

        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop']:
                position = self.PiecePositions(board, piece, oppColour).get(number)
                if position != None:
                    enemyPieceRow, enemyPieceColumn = position
                    # Dynamically gets the method for calculating the moves of each enemy piece
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    # Adds to each list for each piece (key) in the enemyPieceData dict another dictionary which holds the position,
                    # the validMoves and the pinMoves of that piece
                    enemyPieceData[piece].append({
                        'position': position,
                        'validMoves': validMovesMethod(board.board, enemyPieceRow, enemyPieceColumn),
                        'pinMoves': validMovesMethod(board.board, enemyPieceRow, enemyPieceColumn, 'Pin')
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
                            if board.board[row][enemyPieceColumn].piece != None:
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
                            if board.board[enemyPieceRow][column].piece != None:
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
                            if board.board[row][enemyPieceColumn].piece != None:
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
                            if board.board[enemyPieceRow][column].piece != None:
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
                            if board.board[row][column].piece != None: 
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
                            if board.board[row][column].piece != None:
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
                            if board.board[row][column].piece != None:
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
                            if board.board[row][column].piece != None:
                                squaresEmpty = False
                                break
                        # This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight and squaresEmpty:
                            return True
                        
    def Material(self, board, colour):
        materialValue = 0

        for row in range(0, 8):
            for column in range(1, 9):
                if board.board[row][column].piece != None and board.board[row][column].piece.colour == colour:
                    materialValue += board.board[row][column].piece.value

        return materialValue

    def CentralPresence(self, board):
        value = 0

        centralSquares = [(3, 4), (3, 5)]

        for val in centralSquares:
            for values in self.PiecePositions(board, 'Pawn', 'Black').values():
                if values == val:
                    value += 2

        return value
    
    def MaterialEvaluation(self, board):
        materialCount = self.Material(board, 'White') - self.Material(board, 'Black')
        return materialCount
    
    def GamePhases(self, board):
        opening, middlegame, endgame = False, False, False
        if len(self.AllPieces(board)) >= 28:
            opening = True
        elif 16 <= len(self.AllPieces(board)) < 28:
            opening, middlegame = False, True
        elif len(self.AllPieces(board)) < 16 and abs(len(self.PlayerPieces(board, 'White')) - len(self.PlayerPieces(board, 'Black'))) <= 4:
            opening, middlegame, endgame = False, False, True

        if opening:
            pass

        if middlegame:
            pass

        if endgame:
            pass

    def Defense(self, board):
        score = 0
        attackCount = 0
        defenseCount = 0

        enemyPieceMoves = self.AllPieceMoves(board, 'White')
        friendlyDefenseMoves = self.PieceDefenseMoves(board, 'Black')

        for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
            piecePositions = self.PiecePositions(board, piece, 'Black')

            for pos in piecePositions.values():
                if pos != None and pos in enemyPieceMoves:
                    attackCount += 1
                    if pos in friendlyDefenseMoves:
                        defenseCount += 1

        if attackCount > defenseCount:
            score -= 6 * (attackCount - defenseCount)

        return score
    
    def HighValueAttacked(self, board):
        score = 0
        pieceMappings = {'Queen': 9, 'Rook': 5, 'Bishop': 3, 'Knight': 3, 'Pawn': 1}
        for enemyPiece in ['Pawn', 'Bishop', 'Knight', 'Rook']:
            enemyPieceMoves = self.PieceMoves(board, enemyPiece, 'White')
    
            for friendlyPiece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
                piecePositions = self.PiecePositions(board, friendlyPiece, 'Black')
                for pos in piecePositions.values():
                    for i in enemyPieceMoves.values():
                        if pos != None and pos in i and pieceMappings[enemyPiece] < pieceMappings[friendlyPiece]:
                            score -= 6 * (pieceMappings[friendlyPiece] - pieceMappings[enemyPiece])
                            
        return score
    
    def IsCastled(self, board, side=None):
        moved = False
        kingsRook = False
        queensRook = False
        kingRow, kingColumn = self.PiecePositions(board, 'King', 'Black').get(1)
        rookPositions = self.PiecePositions(board, 'Rook', 'Black')

        for pos in rookPositions.values():
            if pos != None and pos == (0, 6):
                kingsRook = True
            elif pos != None and pos == (0, 4):
                queensRook = True

        if board.board[0][8].piece == None and (kingRow, kingColumn) == (0, 7) and kingsRook and side == 'kingside' and not moved:
            moved = True
            return True
        
        if board.board[0][1].piece == None and board.board[0][2].piece == None and (kingRow, kingColumn) == (0, 3)\
        and queensRook and side == 'queenside' and not moved:
            moved = True
            return True
        
        return False
    
    def MediumEvaluation(self, board):
        numMoves = 0
        positionalScore = 0
        centralControl = self.CentralPresence(board)

        materialAdvantage = self.Material(board, 'Black') - self.Material(board, 'White')

        if materialAdvantage < 0:
            positionalScore += 9 * materialAdvantage

        if self.IsCastled(board, 'kingside') or self.IsCastled(board, 'queenside'):
            positionalScore += 5
        
        if board.CanCastleKingside('Black') or board.CanCastleQueenside('Black'):
            positionalScore += 2.5     

        for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
            validMoves = self.PieceMoves(board, piece, 'Black')

            for move in validMoves.values():
                numMoves += len(move)

        if self.Checkmate(board, 'White'):
            positionalScore += 100000000

        mobilityScore = math.log(numMoves)
        #kingRow, kingColumn = self.PiecePositions(board, 'King', 'Black').get(1)
        #queenMoves = self.queen.GetValidMoves(board.board, kingRow, kingColumn)
        #mobilityScore -= 0.5 * len(queenMoves)

        return mobilityScore * 0.6 + positionalScore + self.Defense(board) + self.HighValueAttacked(board)\
        + centralControl * 0.9
    
                