from .Pieces import *
import math

class AIGame:
    def __init__(self):
        # All the global variables to be used are here
        self.pawn = Pawn(Piece)
        self.bishop = Bishop(Piece)
        self.knight = Knight(Piece)
        self.rook = Rook(Piece)
        self.queen = Queen(Piece)
        self.king = King(Piece)
        self.turn = 'White' # Initialised to white because white makes the first move
        self.validPieceMoves = []
        self.EnPassantMove = []
    
    def PiecePositions(self, board, piece, colour):
        pieces = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
        positions = []

        # The two for loops check all squares on the board
        for row in range(0, 8):
            for column in range(1, 9):
                # Checks if a piece of a player has been encountered
                if board.board[row][column].piece != None and board.board[row][column].piece.name == piece\
                and board.board[row][column].piece.colour == colour:
                    positions.append((row, column)) # Adds the position as a tuple to the positions list

                    # Uses the values in the positions list and adds them IN TURN to be the value of the keys in the dictionary
                    # For instance, if positions = [(1, 1), (2, 1)], then pieces would be {1: (1, 1), 2: (2, 1), 3: None} and so on
                    for key, value in zip(pieces.keys(), positions):
                        pieces[key] = value

        return pieces
    
    # This method holds the positions of all the pieces of a certain colour
    def AllPiecePositions(self, board, colour):
        positions = []

        # The two for loops ensure all squares on the board are checked
        for row in range(0, 8):
            for column in range(1, 9):
                # This adds the positions of all the pieces of the chosen player (depending on colour) to the positions list
                if board.board[row][column].piece != None and board.board[row][column].piece.colour == colour\
                and board.board[row][column].piece.name != 'King':
                    positions.append((row, column))

        return positions

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
    
    def Checkmate(self, board, colour):
        # Checks if the King is in check and whose turn it is
        if self.InCheck(board, colour) != None:
            # Checks if the list from AllPieceMoves is empty indicating checkmate as the king is in check
            if self.AllPieceMoves(board, colour) == []:
                return True
        
        return False
    
    def Stalemate(self, board, colour):
        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)
        # Checks if the King cannot move
        if self.NewKingMoves(board, kingRow, kingColumn, colour) == []:
            # Checks if the King is not in check but the AllMovesPiece list is empty indicating Stalemate
            if self.InCheck(board, colour) == None and self.AllPieceMoves(board, colour) == []:
                return True
        
        return False

    def PlayerPieces(self, board, colour):
        pieceValues = []

        # The two for loops check every single square on the board
        for row in range(0, 8):
            for column in range(1, 9):
                square = board.board[row][column]
                # Checks if the there is a piece on the square and the piece is not a king
                if square.piece != None and square.piece.colour == colour and square.piece.name != 'King':
                    # Adds the values of the white or black pieces depending on colcour to the piece values list
                    pieceValues.append(square.piece.value) 

        return pieceValues
    
    def AllPieces(self, board):
        pieceValues = []
        
        # The two for loops check every single square on the board
        for row in range(0, 8):
            for column in range(1, 9):
                square = board.board[row][column]
                # Checks if the there is a piece on the square and the piece is not a king
                if square.piece != None and square.piece.name != 'King':
                    pieceValues.append(square.piece.value) # Adds the value of the piece to the piece values list

        return pieceValues

    def InsufficientMaterial(self, board):
        whitePieces = self.PlayerPieces(board, 'White') # Stores the piece values of all white pieces
        blackPieces = self.PlayerPieces(board, 'Black') # Stores the piece values of all black pieces
        allPieces = self.AllPieces() # Stores the piece values of all pieces
        pawnValue = 1

        # Checks if only kings are left or kings and 1 bishop or knight is left
        if allPieces == [] or (len(allPieces) == 1 and 3 <= allPieces[0] <= 3.5):
            return True
        
        # Checks if two pieces aside from the king's are left and no pawns
        elif len(allPieces) == 2 and pawnValue not in allPieces:
            # Checks if a knight or bishop for both players exist
            if 6 <= sum(allPieces) <= 7 and len(whitePieces) != 0  and len(blackPieces) != 0:
                return True
            
            # Checks if only two knights are left
            elif sum(allPieces) == 6:
                return True
        
        return False
    
    def SwitchTurns(self):
        # Resets the valid moves so the previous players valid moves no longer appears on the screen
        self.validPieceMoves = []
        # This 'if else' block is responsible for switching turns
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'

    def EnPassantPossible(self, board, row, column, colour, side):
        currentSquare = board.board[row][column]

        # Uses the colour parameter to determine the row the pawn is supposed to be for enpassant to happen and its direction
        if colour == 'White':
            enPassantRow = 3
            direction = -1
        else:
            enPassantRow = 4
            direction = 1

        # Checks what side it is
        if side == 'left':
            newColumn = column - 1 
        else:
            newColumn = column + 1

        newRow = row + direction

        # validation to ensure that the new row and column are within the bounds of the board
        if 1 <= newColumn <= 8 and 0 <= newRow <= 7 and 0 <= row + direction * 2 <= 7:
            newSquare = board.board[row][newColumn]
            captureSquare = board.board[newRow][newColumn]
            checkSquare = board.board[row + direction * 2][newColumn]

            # Checks if all enPassant conditions have been met
            if row == enPassantRow and newSquare.piece != None and newSquare.piece.name == 'Pawn'\
            and newSquare.piece.colour != currentSquare.piece.colour and captureSquare.piece == None and checkSquare.piece == None:
                return True

    def NewKingMoves(self, board, row, column, colour):
        # Uses the colour parameter to determine the castling row as well as the colour of the enemy.
        if colour == 'White':
            oppColour = 'Black'
            castlingRow = 7 # White starts at the bottom
        else:
            oppColour = 'White'
            castlingRow = 0 # Black starts at the top

        kingMoves = self.king.GetValidMoves(board.board, row, column)
        shortCastleMoves = self.king.GetShortCastleMoves(board.board, row, column)
        longCastleMoves = self.king.GetLongCastleMoves(board.board, row, column)

        # Checks if kingside castle conditions are met and the King is not in check
        if board.CanCastleKingside(colour) and self.InCheck(board, colour) == None:
            kingMoves.extend(shortCastleMoves) # Adds the castle moves to the valid moves

        # Checks if queenside castle conditions are met and the King is not in check
        if board.CanCastleQueenside(colour) and self.InCheck(board, colour) == None:
            kingMoves.extend(longCastleMoves) # Adds the castle moves to the valid moves

        enemyPieceData = {'King': [], 'Queen': [], 'Rook': [], 'Bishop': [], 'Knight': [], 'Pawn': []}
        
        for number in range(1, 10):
            for piece in ['King', 'Queen', 'Rook','Bishop', 'Knight', 'Pawn']:
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
                    if board.board[row][column].piece.colour == colour and move in controlMoves:
                        kingMoves.remove(move)

                    # This prevents kingside castling through a check
                    if move == (castlingRow, 7) and move in kingMoves and (castlingRow, 6) in controlMoves\
                    and board.CanCastleKingside(colour) and board.board[row][column].piece.colour == colour:
                        kingMoves.remove((castlingRow, 7))

                    # This prevents queenside castling through a check
                    if move == (castlingRow, 3) and move in kingMoves and (castlingRow, 4) in controlMoves\
                    and board.CanCastleQueenside(colour) and board.board[row][column].piece.colour == colour:
                        kingMoves.remove((castlingRow, 3))

        return kingMoves

    def NewPieceMoves(self, board, row, column, name, colour):
        # Uses the colour parameter to determine the colour of the enemy
        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        # Dynamically gets the method to calculate valid moves for the given piece
        movesMethod = getattr(self, name.lower()).GetValidMoves
        validMoves = movesMethod(board.board, row, column)
        updatedValidMoves = []
        piecePositions = self.PiecePositions(board, name, colour) # Holds the dictionary which stores the positions of the given piece
        pieceKey = self.KeyFromPosition(piecePositions, (row, column)) # Gets the key of each piece using KeyFromPosition method
        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)

        # This holds the position of the piece giving the check
        checkingPiecePosition = self.CheckingPiecePosition(board, colour)

        # This stores the list of the different moves for blocking a check
        blockMoves = self.BlockCheckMoves(board, colour)

        if name == 'Pawn' and self.EnPassantPossible(board, row, column, colour, 'left'):
            self.EnPassantMove.extend(self.pawn.GetEnPassantMove(board.board, row, column, 'left'))
            validMoves.extend(self.pawn.GetEnPassantMove(board.board, row, column, 'left'))
        elif name == 'Pawn' and self.EnPassantPossible(board, row, column, colour, 'right'):
            self.EnPassantMove.extend(self.pawn.GetEnPassantMove(board.board, row, column, 'right'))
            validMoves.extend(self.pawn.GetEnPassantMove(board.board, row, column, 'right'))

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
            updatedValidMoves = [] # No other piece apart from the king should be allowed to move in a double check
            
        # Checks if the King is in check by a single piece
        elif self.InCheck(board, colour) == 'single':
            # This checks if the checking piece is in the valid moves of the selected piece and makes it the ONLY valid move if so
            if checkingPiecePosition in validMoves:
                updatedValidMoves = [checkingPiecePosition]

            # This loops through all the possible blocking squares and checks if they are in valid moves of the selected piece and adds them if so
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
        # Uses the colour parameter to determine the colour of the enemy
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
    
    def CheckingPiecePosition(self, board, colour):
        # Uses the colour parameter to determine the colour of the enemy
        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)

        # The two for loops ensure EVERY possible enemy piece (excluding the king) has been checked for its position and moves
        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
                oppPiecePosition = self.PiecePositions(board, piece, oppColour).get(number)

                # Checks if the piece exists
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
        
    def BlockCheckMoves(self, board, colour):
        moves = []
        enemyPiecePosition = self.CheckingPiecePosition(board, colour)
        kingRow, kingColumn = self.PiecePositions(board, 'King', colour).get(1)

        # Cheks if the position of the checking piece exists
        if enemyPiecePosition != None:
            enemyPieceRow, enemyPieceColumn = enemyPiecePosition
            pieceObject = board.PieceAtSquare(enemyPieceRow, enemyPieceColumn) # Gets the piece object from the row and column
            piece = pieceObject.name
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
                            if (row, column) in movesMethod(board.board, enemyPieceRow, enemyPieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the bottom left direction of the queen
                elif enemyPieceRow < kingRow and enemyPieceColumn > kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(enemyPieceRow + 1, kingRow):
                        for column in range(kingColumn + 1, enemyPieceColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(board.board, enemyPieceRow, enemyPieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the top right direction of the queen
                elif enemyPieceRow > kingRow and enemyPieceColumn < kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(kingRow + 1, enemyPieceRow):
                        for column in range(enemyPieceColumn + 1, kingColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(board.board, enemyPieceRow, enemyPieceColumn):
                                moves.append((row, column))

                # Checks if the king is in the top left direction of the queen
                elif enemyPieceRow > kingRow and enemyPieceColumn > kingColumn:
                    # Checks the squares between the king and the queen
                    for row in range(kingRow + 1, enemyPieceRow):
                        for column in range(kingColumn + 1, enemyPieceColumn):
                            # Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            # and if they are, they are added to moves.
                            if (row, column) in movesMethod(board.board, enemyPieceRow, enemyPieceColumn):
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
                        
    # This method gets the total material value of the given player depending on colour
    def Material(self, board, colour):
        materialValue = 0

        # Checks all squares on the board it is given
        for row in range(0, 8):
            for column in range(1, 9):
                # Checks if a piece has been encountered and its colour is the same as the colour parameter
                if board.board[row][column].piece != None and board.board[row][column].piece.colour == colour:
                    materialValue += board.board[row][column].piece.value # Adds its relative value to material value

        return materialValue
    
    # This method calculates how much more/less material black has than white
    def MaterialEvaluation(self, board):
        return self.Material(board, 'Black') - self.Material(board, 'White')

    # This method encourages the AI to have at least 2 pawns in the centre
    def CentralPresence(self, board):
        score = 0

        # Stores the central two forward squares for the black pawns
        centralSquares = [(3, 4), (3, 5)]

        # Loops through the positions of all black pawn
        for pos in self.PiecePositions(board, 'Pawn', 'Black').values():
            # Checks if their current position is in the central squares list
            if pos in centralSquares:
                score += 1 # Adds 1 to score to encourage the AI to have 2 pawns in the centre at least

        return score
    
    # This method is used to check the controlled squares of friendly pieces
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
            # Depending on the piece, it adds it control moves to the moves list accordingly
            moves.extend(movesMethod(board.board, pos[0], pos[1], 'Control'))

        return moves

    # This method is used to ensure a piece does not move to a square controlled by more enemy pieces than defended by friendly pieces
    def Defense(self, board):
        score = 0
        attackCount = 0 # Variable to store the number of enemy pieces that attack a square/friendly piece
        defenseCount = 0 # Variable to store the number of friendly piece that defend a square/friendly piece

        enemyPieceMoves = self.AllPieceMoves(board, 'White') # Holds a squares controlled by an enemy piece
        enemyPieceMoves.extend(self.SkewerMoves(board, 'White')) # Adds the skewer moves to list of enemy piece moves
        friendlyDefenseMoves = self.PieceDefenseMoves(board, 'Black') # Holds all squares controlled by a friendly piece

        # Ensure the positions all black pieces are checked
        for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
            piecePositions = self.PiecePositions(board, piece, 'Black')

            # Loops through the positions of all black pieces excluding the king
            for pos in piecePositions.values():
                # Checks if the piece is in a square controlled by an enemy piece
                if pos != None and pos in enemyPieceMoves:
                    attackCount += 1 # Increments the attack count
                    # Checks if the piece is in a square controlled by a friendly piece
                    if pos in friendlyDefenseMoves:
                        defenseCount += 1 # Increments the defense count

        # Checks if the number of pieces attacking piece is greater than the number of pieces defending it.
        if attackCount > defenseCount:
            score -= 7 * (attackCount - defenseCount) # Reduces the score by a lot to discourage moving to such positions

        return score

    # This method gets the relative value of a piece from its position
    def PieceValueData(self, board, position):
        piece = board.PieceAtSquare(position[0], position[1])

        pieceValue = piece.value
        
        return pieceValue
    
    # This method encourages the AI to move a piece with a higher value if attacked by a piece with a lower value
    def HighValueAttacked(self, board):
        score = 0
        friendlyPositions = self.AllPiecePositions(board, 'Black')
        enemyPositions = self.AllPiecePositions(board, 'White')
        lowestScore = float('inf') # I set it to +infinity because I want to keep track of the lowest score

        # Loops through the positions of all black pieces
        for friendlyPos in friendlyPositions:
            value = self.PieceValueData(board, friendlyPos) # Stores the relative value of the piece from its position
            # Loops through the positions of all enemy pieces
            for enemyPos in enemyPositions:
                enemyMove = self.PieceMovesData(board, enemyPos) # Stores the moves the enemy piece can make from its position
                enemyValue = self.PieceValueData(board, enemyPos) # Stores the relative value of the enemy piece from its position

                # Checks if any of the black pieces are in any of the white piece's moves and the black piece has more relative value
                if friendlyPos in enemyMove and value > enemyValue:
                    score -= 6 * (value - enemyValue) # Reduces the score by 6 times the value deficit to encourage moving out of danger
                    # Checks if the score is lower than the lowest score
                    if score < lowestScore:
                        lowestScore = score # Reassigns the lowest score

        # Checks if a piece with a higher value is being attacked by a piece with a lower value
        if lowestScore != float('inf'):
            return lowestScore
        else:
            return 0 # returns 0 if no high value piece is under attack by a lower value piece       
    
    # This method checks if the King is castled, manually
    def IsCastled(self, board, side):
        moved = False
        kingsRook = False # Variables to track if the kings rook is on the correct castled square
        queensRook = False # Variables to track if the queens rook is on the correct castled square
        kingRow, kingColumn = self.PiecePositions(board, 'King', 'Black').get(1)
        rookPositions = self.PiecePositions(board, 'Rook', 'Black') # Stores the positions of the two black rooks

        # Checks the positions of the rooks
        for pos in rookPositions.values():
            # Checks if the rook exists and its on the short castled square not castling square so (0, 6) and not (0, 8)
            if pos != None and pos == (0, 6):
                kingsRook = True
            
            # Checks if the rook exists and its on the long castled square not the castling square so (0, 4) and not (0, 1)
            elif pos != None and pos == (0, 4):
                queensRook = True

        # Checks if the king and rook are on the short castled squares and the king's rook original square is empty 
        if board.board[0][8].piece == None and (kingRow, kingColumn) == (0, 7) and kingsRook and side == 'kingside' and not moved:
            moved = True
            return True
        
        # Checks if the king and queens rook are on the long castled squares and the queen's rook original square is empty as well as the one next to it
        if board.board[0][1].piece == None and board.board[0][2].piece == None and (kingRow, kingColumn) == (0, 3)\
        and queensRook and side == 'queenside' and not moved:
            moved = True
            return True
        
        return False
    
    # This is where all the separate evaluations are added up to produce a final one for the medium AI
    def MediumEvaluation(self, board):
        numMoves = 0 # Variable to track the number of moves the AI has
        positionalScore = 0  # Initialises a positional score for some positional advantages
        centralControl = self.CentralPresence(board) # Stores the pawn central control score
        positiveAdvantage = 0

        materialAdvantage = self.MaterialEvaluation(board) # Stores the difference in material between black and white
    
        # Checks if white has more material value than black
        if materialAdvantage < 0:
            positionalScore += 4 * materialAdvantage # This reduces positional score by 4 times the deficit to encourage capturing back

        # Checks if black has more material value than white
        if materialAdvantage > 0:
            positiveAdvantage += 1.5 * materialAdvantage # Increases the score by a smaller amount to prevent the AI from capturing defended pieces

        # Checks if the black king is castled queenside or kingside (i.e short or long)
        if self.IsCastled(board, 'kingside') or self.IsCastled(board, 'queenside'):
            positionalScore += 5 # Increases the positional score so it encourages the AI to castle its king
        
        # Checks if the black king can castle queenside or kingside
        if board.CanCastleKingside('Black') or board.CanCastleQueenside('Black'):
            # Increases the positional score so it encourages the AI to be in a position that it can castle
            # but with by a less amount than being actually castled so the AI doesn't continue to stay in a position where it CAN castle.
            positionalScore += 2.5

        # Checks if the current game phase is the opening
        if self.GamePhases(board) == 'Opening':
            # This checks the valid moves of all pieces excluding the king and queen
            for piece in ['Rook', 'Bishop', 'Knight', 'Pawn']:
                validMoves = self.PieceMoves(board, piece, 'Black')

                # Loops through all the move lists for each piece
                for move in validMoves.values():
                    numMoves += len(move) # Adds the length of each list to numMoves so the AI can prioritise activating its pieces

        # Checks if the current game phase is not in the opening
        elif self.GamePhases(board) != 'Opening':
            # This checks the valid moves of all pieces excluding the king
            for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
                validMoves = self.PieceMoves(board, piece, 'Black')

                # Loops through all the move lists for each piece
                for move in validMoves.values():
                    numMoves += len(move) # Adds the length of each list to numMoves so the AI can prioritise activating its pieces

        # Allows the AI to find checkmate in 1 if possible
        if self.Checkmate(board, 'White'):
            positionalScore += 100000000

        # Prevents taking the log of 0 which would result in an error
        if numMoves > 0:
            # Takes a logarithm of the no. of moves so it doesn't contribute too much a factor into the evaluation
            mobilityScore = math.log(numMoves)
        else:
            mobilityScore = 0

        # Returns all the evaluations added together, some of them have been multiplied by certain amounts to reduce their influence further
        return mobilityScore * 0.6 + positionalScore + self.Defense(board) + self.HighValueAttacked(board)\
        + centralControl * 0.8 + positiveAdvantage
    
    # This method gets the current phase of the game by checking the number of pieces left on the board
    def GamePhases(self, board):
        phase = None

        # Checks if there are 25 or more pieces left
        if len(self.AllPieces(board)) >= 25:
            phase = 'Opening'

        # Checks if there are more than 15 pieces left but less than 25 pieces
        elif 15 <= len(self.AllPieces(board)) < 25:
            phase = 'Middlegame'

        # Checks if there are less than 15 pieces left
        elif len(self.AllPieces(board)) < 15:
            phase = 'Endgame'

        return phase
    
    # This method uses the position of any piece to get its moves
    def PieceMovesData(self, board, position):
        piece = board.PieceAtSquare(position[0], position[1])
        movesMethod = getattr(self, piece.name.lower()).GetValidMoves
        moves = movesMethod(board.board, position[0], position[1])

        return moves

    def SkewerMoves(self, board, colour):
        positions = []
        moves = []

        # The two for loops check all squares on the board
        for row in range(0, 8):
            for column in range(1, 9):
                # This adds the positions of all the pieces of the set player to the positions list
                if board.board[row][column].piece != None and board.board[row][column].piece.colour == colour:
                    positions.append((row, column))

        # This loops through all the values now in the positions list
        for pos in positions:
            piece = board.PieceAtSquare(pos[0], pos[1]) # Gets the piece attribute at that position
            # Checks if the piece is a queen, bishop or rook
            if piece.name == 'Queen' or piece.name == 'Bishop' or piece.name == 'Rook':
                # Dynamically gets the GetValidMoves function depending on the piece
                movesMethod = getattr(self, piece.name.lower()).GetValidMoves
                moves.extend(movesMethod(board.board, pos[0], pos[1], 'Skewer')) # Adds the skewer moves only

        return moves

    # This uses a better defense logic from the medium AI so it doesn't blunder easily
    def BetterDefense(self, board):
        score = 0
        allPieces = {}
        lowestScore = float('inf') # I set it to +infinity because I want to keep track of the lowest score
        allPositions = self.AllPiecePositions(board, 'Black') 
        enemyPieceMoves = self.AllPieceMoves(board, 'White') 
        enemyPieceMoves.extend(self.SkewerMoves(board, 'White')) # This adds the skewer moves to the enemy moves so it can be considered
        defenceMoves = self.PieceDefenseMoves(board, 'Black')

        # Loops through the positions of all friendly(black) pieces
        for pos in allPositions:
            attackCount = enemyPieceMoves.count(pos) # Gets the attack count by counting the number of times its position is in the enemy moves
            defenseCount = defenceMoves.count(pos) # Gets the defense count by counting the number of times of its position is in the defense moves

            # Updates the all pieces dictionary so it now holds the position of all pieces and how much they are defended.
            allPieces.update({pos: defenseCount - attackCount})

        # Loops through the positions and defenseScores
        for position, defenseScore in allPieces.items():
            piece = board.PieceAtSquare(position[0], position[1]) # Gets the piece attribute using the board method PieceAtSquare

            # Checks if a piece is attacked more than it is defended
            if defenseScore < 0:
                # Checks if the piece is a pawn
                if piece.value == 1:
                    score = -3 # Takes away a constant score
                else:
                    # If it's not a piece it takes away the score related to the piece's value and how much it was attacked
                    score = defenseScore * piece.value * 1.35

                # Checks if the score is lower than the lowest score
                if score < lowestScore:
                    lowestScore = score # Reassigns lowest score

        # Checks if any piece is attack more times than defended
        if lowestScore != float('inf'):
            return lowestScore
        else:
            return 0 # Returns 0 if all pieces are defended more or the same number of times than attacked

    # This method encourages the AI to attack undefended pieces but ensures they can't be captured by said undefended pieces
    def AttackUndefended(self, board):
        score = 0
        undefendedPiecePositions = []
        enemyPiecePositions = self.AllPiecePositions(board, 'White') # Stores the positions of all enemy pieces
        piecePositions = self.AllPiecePositions(board, 'Black')
        piecePositions.append(self.PiecePositions(board, 'King', 'Black').get(1)) # Adds the position of the king

        # Loops through all positions of enemy pieces
        for positions in enemyPiecePositions:
            # Checks if the piece is not defended
            if positions not in self.PieceDefenseMoves(board, 'White'):
                undefendedPiecePositions.append(positions) # Adds it to the undefended list

        # Loops through the positions of all friendly pieces
        for pos in piecePositions:
            moves = self.PieceMovesData(board, pos) # Uses their current position to get their moves
            # Loops through all undefended enemy pieces
            for enemypos in undefendedPiecePositions:
                # Checks if the enemy piece is in the valid moves of the friendly piece but the friendly piece can't be captured by enemy piece
                if enemypos in moves and pos not in self.PieceMovesData(board, enemypos):
                    score += 1.8

        return score
    
    # This method holds the moves a player can make without getting captured by an enemy piece
    def UsefulMoves(self, board, colour):
        if colour == 'White':
            oppColour = 'Black'
        else:
            oppColour = 'White'

        moves = [] # To be used to store all useful moves
        enemyMoves = self.AllPieceMoves(board, oppColour) # Holds all enemy piece moves
        friendlyMoves = self.AllPieceMoves(board, colour) # Holds all moves that can be made by friendly piece

        moves.append(friendlyMoves)

        # Loops through all the moves in the moves list
        for move in moves[:]:
            # Check if that move is in an enemy piece's move and removes it if so
            if move in enemyMoves:
                moves.remove(move)

        return moves

    # This method encourages the AI to play a pawn break if it's in a clamped position meaning it has less useful moves than white
    def PawnBreaks(self, board):
        score = 0

        # Checks if the current game phase is in the Opening or Middlegame
        if self.GamePhases(board) == 'Middlegame' or self.GamePhases(board) == 'Opening':
            # Checks if white has more useful moves than black
            if len(self.UsefulMoves(board, 'White')) - len(self.UsefulMoves(board, 'Black')) >= 5:
                enemyPawnMoves = self.PieceMoves(board, 'Pawn', 'White') # Stores the dictionary which holds the valid moves of the white pawns
                friendlyPawnPositions = self.PiecePositions(board, 'Pawn', 'Black') # Stores the positions of all the black pawns

                # Loops through all the positions of all the black pawns
                for pos in friendlyPawnPositions.values():
                    # Checks if they are in the valid move of an enemy pawn so a pawn break could occur
                    if pos in enemyPawnMoves.values():
                        score += 2

        return score

    # This is an endgame evaluation method which encourages the AI to push the furthest pawns that have no pieces in front of them
    def PromotionBonus(self, board):
        score = 0
        rows = [] # To store the rows of all the pawns

        # Checks if the current game phase in the Endgame
        if self.GamePhases(board) == 'Endgame':
            pawnPositions = self.PiecePositions(board, 'Pawn', 'Black') # Holds the dictionary which stores the positions of all black pawns

            # Loops through 1 to 8 to get the individual positions of each pawn
            for number in range(1, 9):
                position = pawnPositions.get(number)
                # Checks if the pawn exists
                if position != None:
                    rows.append(position[0]) # It adds its row to the rows list

            # Loops through all the pawn positions individually
            for pos in pawnPositions.values():
                squaresEmpty = True
                # Checks if the pawn exists
                if pos != None:
                    # Checks all the squares in front of the pawn till the last row
                    for row in range(pos[0] + 1, 8):
                        # Checks if a piece is there
                        if board.board[row][pos[1]].piece != None:
                            squaresEmpty = False # Sets to False to indicate not all squares in front of it are empty
                            break
                
                # This checks if all squares in front of the pawn are empty
                if pos != None and squaresEmpty:
                    # Checks if the pawn is the closest to the promotion square
                    if pos[0] == max(rows):
                        score += 7 + pos[0] # Gives it a higher score
                    else:
                        score += 5 + pos[0] # Still gives a score so it can push the pawn but a lower one

        return score

    # This method encourages the AI to give checks if the number of moves white has while their king is in check is below a certain amount
    def CheckBonus(self, board):
        totalMoves = 0
        score = 0

        # Checks if the white king is in check
        if self.InCheck(board, 'White') != None:
            totalMoves = len(self.AllPieceMoves(board, 'White')) # Stores all the moves white can make while the king is in check
            kingMoves = len(self.PieceMoves(board, 'King', 'White').get(1)) # Stores all the king moves white can make while in check
            pieceMoves = totalMoves - kingMoves # Stores the number of moves pieces other than a king can make while in check
            checkingPiecePosition = self.CheckingPiecePosition(board, 'White') # Holds the position of the black piece giving the check

            # Checks if the black piece giving the check is not in positions to be captured by a white piece
            if checkingPiecePosition not in self.AllPieceMoves(board, 'White'):
                # Checks if total moves > 0 to prevent a math error and it can make 2 moves with pieces other than a king
                if totalMoves > 0 and pieceMoves < 3 :
                    score += 1.8/totalMoves # Used division so the smaller total moves is, the higher the score

        return score
    
    # The main evaluation where all the separate evaluations are added for the hard AI
    def HardEvaluation(self, board):
        mediumEval = self.MediumEvaluation(board) - self.Defense(board) + self.BetterDefense(board)
        score = 0

        # Checks if the current game phase is in the opening
        if self.GamePhases(board) == 'Opening':
            queenPosition = self.PiecePositions(board, 'Queen', 'Black').get(1)
            # Checks if black has less or equal material
            if self.MaterialEvaluation(board) <= 0:
                 # Checks if the queen exists and the queen is in white's side of the board
                if queenPosition != None and queenPosition[0] > 3:
                        score -= 4 # Reduces to score to discourage bringing out the queen too early in the game

        # Checks if the current game phase is in the endgame
        if self.GamePhases(board) == 'Endgame':
            # Checks if the king is castled on either side
            if self.IsCastled(board, 'kingside') or self.IsCastled(board, 'queenside'):
                score -= 6 # Reduces score to penalise being castled in the endgame

            return self.PromotionBonus(board) + self.CheckBonus(board) + mediumEval + self.AttackUndefended(board) + score

        else:
            return mediumEval + self.CheckBonus(board) + self.PawnBreaks(board) + self.AttackUndefended(board) + score
    
                