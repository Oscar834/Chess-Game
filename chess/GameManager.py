import pygame
from .Constants import SQUARE_HEIGHT, SQUARE_WIDTH, LGREY
from .Board import Board
from .Pieces import *

class Game:
    def __init__(self, screen):
        self.board = Board()
        self.pawn = Pawn(Piece)
        self.bishop = Bishop(Piece)
        self.knight = Knight(Piece)
        self.rook = Rook(Piece)
        self.queen = Queen(Piece)
        self.king = King(Piece)
        self.squareSelected = None
        self.turn = 'White'
        self.ValidPieceMoves = []
        self.screen = screen

    def UpdateScreen(self, colour):
        self.board.DrawBoard(self.screen, colour)
        self.board.DisplayPieces(self.screen)
        #Promotion is called here for white and for black for visual display
        self.board.Promotion('White', self.screen)
        self.board.Promotion('Black', self.screen)
        self.DrawValidMoves(self.ValidPieceMoves)

    def FriendlyPiecePosition(self, piece):
        # Dictionary which stores the row and column of the piece as the value and the piece number as the key
        friendlyPieces = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
        positions = []

        for row in range(0, 8):
            for column in range(1, 9):
                # Row and column for friendly piece added to positions list. 
                if self.board.board[row][column].piece != None and self.board.board[row][column].piece.name == piece\
                and self.board.board[row][column].piece.colour == self.turn:
                    positions.append((row, column))

                    # Uses the values in the positions list and adds them in turn to be the value of the keys in the dictionary
                    for key, value in zip(friendlyPieces.keys(), positions):
                        friendlyPieces[key] = value

        return friendlyPieces
    
    def EnemyPiecePosition(self, piece):
        enemyPieces = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
        positions = []

        for row in range(0, 8):
            for column in range(1, 9):
                # Row and column for enemy piece added to positions list
                if self.board.board[row][column].piece != None and self.board.board[row][column].piece.name == piece\
                and self.board.board[row][column].piece.colour != self.turn:
                    positions.append((row, column))

                    for key, value in zip(enemyPieces.keys(), positions):
                        enemyPieces[key] = value

        return enemyPieces

    def PieceMoves(self, piece, colour):
        moves = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        squares = []

        if piece == 'King' and colour == 'Black':
            kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)
            squares.append(self.NewKingMoves(kingRow, kingColumn))

            for key, value in zip(moves.keys(), squares):
                moves[key] = value

        elif piece != 'King' and colour == 'Black':
            for num in range(1, 10):
                piecePosition = self.FriendlyPiecePosition(piece).get(num)
                if piecePosition != None:
                    pieceRow, pieceColumn = piecePosition
                    squares.append(self.NewPieceMoves(pieceRow, pieceColumn, piece))

                    for key, value in zip(moves.keys(), squares):
                        moves[key] = value

        return moves

    def KeyFromPosition(self, dict, position):
        for key, value in dict.items():
            if value == position:
                return key
            
        return None

    def CheckingPiecePosition(self):
        positions = []
        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
                positions.append(self.PieceCheck(piece, number))

        return positions
    
    def BlockMoves(self):
        moves = []
        for number in range(1, 10):
            for piece in ['Queen', 'Rook', 'Bishop']:
                moves.extend(self.BlockPieceCheck(piece, number))

        return moves
    
    def AllPieceMoves(self):
        positions = []
        moves = []
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece != None and self.board.board[row][column].piece.colour == self.turn:
                    positions.append((row, column))

        for pos in positions:
            piece = self.board.PieceAtSquare(pos[0], pos[1])
            if piece.name != 'King':
                moves.extend(self.NewPieceMoves(pos[0], pos[1], piece.name))
            else:
                moves.extend(self.NewKingMoves(pos[0], pos[1]))

        return moves
    
    def Checkmate(self, colour):
        if self.InCheck() != None and colour == self.turn:
            if self.AllPieceMoves() == []:
                return True
        
        return False
    
    def Stalemate(self):
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)
        if self.NewKingMoves(kingRow, kingColumn) == []:
            if self.InCheck() == None and self.AllPieceMoves() == []:
                return True
        
        return False
    
    def PlayerPieces(self, colour):
        playerPieces = []
        
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece != None and self.board.board[row][column].piece.colour == colour:
                    playerPieces.append(self.board.board[row][column].piece.name)

        return playerPieces
    
    def AllPieces(self):
        allPieces = []
        
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece != None:
                    allPieces.append(self.board.board[row][column].piece.name)

        return allPieces

    def InsufficientMaterial(self):
        whitePieces = self.PlayerPieces('White')
        blackPieces = self.PlayerPieces('Black')
        allPieces = self.AllPieces()

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
        return self.board
    
    def AIMovement(self, board):
        self.board = board
        self.SwitchTurns()
    
    def SelectSquare(self, row, column):
        #checks if a square is selected
        if self.squareSelected:
            finalSquare = self.Move(row, column)
            if not finalSquare:
                #If the square they tried to move to is not valid, reset the valid moves, and allow them to select a piece again
                self.ValidPieceMoves= []
                self.squareSelected = None
                self.SelectSquare(row, column)

        piece = self.board.PieceAtSquare(row, column)
        pieceSquare = self.board.PieceBoardIndex(row, column)
        
        if piece != None and piece.name == 'King' and piece.colour == self.turn:
            self.squareSelected = pieceSquare
            #Set this variable to the new method (NewKingMoves) so it accounts for the removal of moves.
            self.ValidPieceMoves = self.NewKingMoves(row, column)

        #Checks is the selected square != empty and if it's a pawn
        elif piece != None and piece.colour == self.turn:
            self.squareSelected = pieceSquare
            self.ValidPieceMoves = self.NewPieceMoves(row, column, piece.name)

    def Move(self, row, column):
        if self.squareSelected.piece != None and self.squareSelected.piece.name == 'King' and (row == 7 or row == 0)\
        and column == 7 and self.board.CanCastleKingside(self.turn):
            self.board.CastleKingside(self.turn)
            self.SwitchTurns()

        elif self.squareSelected.piece != None and self.squareSelected.piece.name == 'King' and (row == 7 or row == 0)\
        and column == 3 and self.board.CanCastleQueenside(self.turn):
            self.board.CastleQueenside(self.turn)
            self.SwitchTurns()

        #This is the if block responsible for every other move
        elif self.squareSelected and (row, column) in self.ValidPieceMoves:
            self.board.MovePiece(self.squareSelected, row, column)
            self.SwitchTurns()
            return True
        
        return False
        
    def DrawValidMoves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.screen, LGREY, (column * SQUARE_WIDTH + SQUARE_HEIGHT//2, row * SQUARE_HEIGHT + SQUARE_WIDTH//2), 14)
    
    def SwitchTurns(self):
        #resets the valid moves so the previous players valid moves
        #no longer appears on the screen
        self.ValidPieceMoves = []
        #This 'if else' block is responsible for switching turns
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'
    
    def NewKingMoves(self, row, column):
        kingMoves = self.king.GetValidMoves(self.board.board, row, column)
        shortCastleMoves = self.king.GetShortCastleMoves(self.board.board, row, column)
        longCastleMoves = self.king.GetLongCastleMoves(self.board.board, row, column)
        oppKingPosition = self.EnemyPiecePosition('King').get(1)
        oppKingRow, oppKingColumn = oppKingPosition
        kingControlMoves = self.king.GetControlMoves(self.board.board, oppKingRow, oppKingColumn)

        if self.board.CanCastleKingside(self.turn) and self.InCheck() == None:
            kingMoves.extend(shortCastleMoves)

        if self.board.CanCastleQueenside(self.turn) and self.InCheck() == None:
            kingMoves.extend(longCastleMoves)

        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': [], 'Knight': [], 'Pawn': []}
        
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop', 'Knight', 'Pawn']:
                position = self.EnemyPiecePosition(piece).get(number)
                if position != None:
                    pieceRow, pieceColumn = position
                    controlMovesMethod = getattr(self, piece.lower()).GetControlMoves
                    enemyPieceData[piece].append({
                        'controlMoves': controlMovesMethod(self.board.board, pieceRow, pieceColumn)
                    })

        for pieceData in enemyPieceData.values():
            for enemyData in pieceData:
                controlMoves = enemyData['controlMoves']

                for move in kingMoves[:]:
                    if self.board.board[row][column].piece.colour == self.turn and (move in controlMoves or move in kingControlMoves):
                        kingMoves.remove(move)

        return kingMoves

    def NewPieceMoves(self, row, column, name):
        movesMethod = getattr(self, name.lower()).GetValidMoves
        validMoves = movesMethod(self.board.board, row, column)
        updatedValidMoves = []
        piecePositions = self.FriendlyPiecePosition(name)
        pieceKey = self.KeyFromPosition(piecePositions, (row, column))
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)

        #This holds the positions of the pieces giving the check
        positions = self.CheckingPiecePosition()

        #This stores the list of the different moves for blocking a queen, rook or bishop check
        blockMoves = self.BlockMoves()

        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': []}
        
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop']:
                position = self.EnemyPiecePosition(piece).get(number)
                if position != None:
                    pieceRow, pieceColumn = position
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    pinMovesMethod = getattr(self, piece.lower()).GetPinMoves
                    enemyPieceData[piece].append({
                        'position': position,
                        'validMoves': validMovesMethod(self.board.board, pieceRow, pieceColumn),
                        'pinMoves': pinMovesMethod(self.board.board, pieceRow, pieceColumn)
                    })

        if self.PiecePinned(name, pieceKey) and self.InCheck() != None:
            updatedValidMoves = []

        elif self.InCheck() == 'double':
            updatedValidMoves = []
            
        elif self.InCheck() == 'single':
            for position in positions:
                if position in validMoves:
                    updatedValidMoves = [position]

            for move in blockMoves:
                if move in validMoves:
                    updatedValidMoves.append(move)

        elif self.InCheck() == None and self.PiecePinned(name, pieceKey) != True:
            updatedValidMoves = validMoves

        else:
            for enemyPiece, pieceData in enemyPieceData.items():
                for enemyData in pieceData:
                    pieceRow, pieceColumn = enemyData['position']
                    pieceMoves = enemyData['validMoves']
                    pinMoves = enemyData['pinMoves']

                    if name == 'Queen' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                            if row == pieceRow:
                                for move in pinMoves:
                                    if move in validMoves and move[0] == row:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))
                            elif column == pieceColumn:
                                for move in pinMoves:
                                    if move in validMoves and move[1] == column:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))

                        if enemyPiece == 'Bishop' or enemyPiece == 'Queen':
                            if (kingRow < pieceRow and kingColumn > pieceColumn) or (kingRow > pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] + move[1] == row + column:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))
                            elif (kingRow > pieceRow and kingColumn > pieceColumn) or (kingRow < pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] != pieceRow and move[1] != pieceColumn:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))

                    if name == 'Rook' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                            if row == pieceRow:
                                for move in pinMoves:
                                    if move in validMoves and move[0] == row:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))
                            elif column == pieceColumn:
                                for move in pinMoves:
                                    if move in validMoves and move[1] == column:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))
                        
                        if (enemyPiece == 'Queen' or enemyPiece == 'Bishop') and row != pieceRow and column != pieceColumn:
                            updatedValidMoves = []

                    if name == 'Knight' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        updatedValidMoves = []

                    if name == 'Bishop' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        if (enemyPiece == 'Bishop' or enemyPiece == 'Queen'):
                            if (kingRow < pieceRow and kingColumn > pieceColumn) or (kingRow > pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] + move[1] == row + column:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))
                            elif (kingRow > pieceRow and kingColumn > pieceColumn) or (kingRow < pieceRow and kingColumn < pieceColumn):
                                for move in pinMoves:
                                    if move in validMoves and move[0] != pieceRow and move[1] != pieceColumn:
                                        updatedValidMoves.append(move)
                                updatedValidMoves.append((pieceRow, pieceColumn))
                        if (enemyPiece == 'Queen' or enemyPiece == 'Rook') and (row == pieceRow or column == pieceColumn):
                            updatedValidMoves = []

                    if name == 'Pawn' and (row, column) in pieceMoves and (kingRow, kingColumn) in pinMoves:
                        if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                            if column == pieceColumn:
                                for move in pinMoves:
                                    if move in validMoves and move[1] == column:
                                        updatedValidMoves.append(move)
                            elif row == pieceRow:
                                updatedValidMoves = []
                        if (enemyPiece == 'Bishop' or enemyPiece == 'Queen') and (row != pieceRow and column != pieceColumn):
                            if (pieceRow, pieceColumn) in validMoves:
                                updatedValidMoves = [(pieceRow, pieceColumn)]
                            else:
                                updatedValidMoves = []

        return updatedValidMoves
    
    def InCheck(self):
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)
        count = 0

        enemyPieceData = {'Queen': [], 'Rook': [], 'Bishop': [], 'Knight': [], 'Pawn': []}
        
        for number in range(1, 10):
            for piece in ['Queen', 'Rook','Bishop', 'Knight', 'Pawn']:
                position = self.EnemyPiecePosition(piece).get(number)
                if position != None:
                    pieceRow, pieceColumn = position
                    validMovesMethod = getattr(self, piece.lower()).GetValidMoves
                    enemyPieceData[piece].append({
                        'validMoves': validMovesMethod(self.board.board, pieceRow, pieceColumn)
                    })

        for pieceData in enemyPieceData.values():
            for enemyData in pieceData:
                validMoves = enemyData['validMoves']

                if (kingRow, kingColumn) in validMoves:
                    count += 1

        if count == 2:
            return 'double'
        elif count == 1:
            return 'single'
        
        return None

    def PieceCheck(self, piece, number):
        oppPiecePosition = self.EnemyPiecePosition(piece).get(number)
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)

        if oppPiecePosition != None:
            oppPieceRow, oppPieceColumn = oppPiecePosition
            movesMethod = getattr(self, piece.lower()).GetValidMoves
            oppPieceMoves = movesMethod(self.board.board, oppPieceRow, oppPieceColumn)
        else:
            oppPieceMoves = []

        if (kingRow, kingColumn) in oppPieceMoves:
            return oppPieceRow, oppPieceColumn
        
    def BlockPieceCheck(self, piece, number):
        moves = []
        piecePosition = self.PieceCheck(piece, number)
        kingRow, kingColumn = self.FriendlyPiecePosition('King').get(1)
        movesMethod = getattr(self, piece.lower()).GetValidMoves

        if piecePosition != None:
            pieceRow, pieceColumn = piecePosition

            if (piece == 'Queen' or piece == 'Bishop') and (pieceRow != kingRow and pieceColumn != kingColumn):
                #Checks if the king is in the bottom right direction of the queen
                if pieceRow < kingRow and pieceColumn < kingColumn:
                    #Checks the squares between the king and the queen
                    for row in range(pieceRow + 1, kingRow):
                        for column in range(pieceColumn + 1, kingColumn):
                            #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            #and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

                #Checks if the king is in the bottom left direction of the queen
                elif pieceRow < kingRow and pieceColumn > kingColumn:
                    #Checks the squares between the king and the queen
                    for row in range(pieceRow + 1, kingRow):
                        for column in range(kingColumn + 1, pieceColumn):
                            #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            #and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

                #Checks if the king is in the top right direction of the queen
                elif pieceRow > kingRow and pieceColumn < kingColumn:
                    #Checks the squares between the king and the queen
                    for row in range(kingRow + 1, pieceRow):
                        for column in range(pieceColumn + 1, kingColumn):
                            #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            #and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

                #Checks if the king is in the top left direction of the queen
                elif pieceRow > kingRow and pieceColumn > kingColumn:
                    #Checks the squares between the king and the queen
                    for row in range(kingRow + 1, pieceRow):
                        for column in range(kingColumn + 1, pieceColumn):
                            #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                            #and if they are, they are added to moves.
                            if (row, column) in movesMethod(self.board.board, pieceRow, pieceColumn):
                                moves.append((row, column))

            if (piece == 'Queen' or piece == 'Rook') and (pieceRow == kingRow or pieceColumn == kingColumn):
                #Checks if the king is below the rook and they are both on the same column
                if pieceRow < kingRow and pieceColumn == kingColumn:
                    #This for loop is then used to check all the squares between the king and the rook and then adds them to moves
                    for row in range(pieceRow + 1, kingRow):
                        moves.append((row, pieceColumn))

                #Checks if the king is above the rook and they're on the same column
                elif pieceRow > kingRow and pieceColumn == kingColumn:
                    #This also checks all the squares between the king and rook and adds them to moves
                    for row in range(kingRow + 1, pieceRow):
                        moves.append((row, pieceColumn))

                #Checks if the king and rook are on the same row and the king is to the right of the rook
                elif pieceRow == kingRow and pieceColumn < kingColumn:
                    #Adds all the squares between the king and rook in this scenario to moves
                    for column in range(pieceColumn + 1, kingColumn):
                        moves.append((pieceRow, column))

                #Checks if the king and rook are on the same row and the king is to the left of the rook
                elif pieceRow == kingRow and pieceColumn > kingColumn:
                    #Adds all the squares between the king and rook to moves
                    for column in range(kingColumn + 1, pieceColumn):
                        moves.append((pieceRow, column))

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
                    movesMethod = getattr(self, piece.lower()).GetValidMoves
                    pinMovesMethod = getattr(self, piece.lower()).GetPinMoves
                    enemyPieceData[piece].append({
                        'position': position,
                        'pieceMoves': movesMethod(self.board.board, enemyPieceRow, enemyPieceColumn),
                        'pinMoves': pinMovesMethod(self.board.board, enemyPieceRow, enemyPieceColumn)
                    })

        for enemyPiece, pieceData in enemyPieceData.items():
            for enemydata in pieceData:
                enemyPieceRow, enemyPieceColumn = enemydata['position']
                enemyPieceMoves = enemydata['pieceMoves']
                enemyPinMoves = enemydata['pinMoves']

                if enemyPiece == 'Queen' or enemyPiece == 'Rook':
                    #Checks if the piece is on the same vertical file as the king and rook and the king is below the rook
                    if (pieceColumn == enemyPieceColumn == kingColumn) and (enemyPieceRow < pieceRow < kingRow)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for row in range(pieceRow + 1, kingRow):
                            #Checks if the squares between the piece and king are not empty or the king is directly behind the piece
                            if self.board.board[row][enemyPieceColumn].piece != None or pieceRow + 1 == kingRow:
                                squaresEmpty = False
                                break
                        
                        #This then checks if both condtions have been satisfied for the piece to be considered pinned
                        if kingInSight == True and squaresEmpty == True:
                            return True
                        
                    #Checks if the piece is on the same row as the king and rook and the king is to the left of the rook
                    elif (pieceRow == enemyPieceRow == kingRow) and (kingColumn < pieceColumn < enemyPieceColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for column in range(kingColumn + 1, pieceColumn):
                            #Checks if the squares between the piece and king are not empty or the king is directly to the left of the piece
                            if self.board.board[enemyPieceRow][column].piece != None:
                                squaresEmpty = False
                                break
                            
                        if kingInSight == True and squaresEmpty == True:
                            return True
                        
                    #This is similar to the if block but just checks if the king is above instead of below 
                    elif (pieceColumn == enemyPieceColumn == kingColumn) and (kingRow < pieceRow < enemyPieceRow)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for row in range(kingRow + 1, pieceRow):
                            if self.board.board[row][enemyPieceColumn].piece != None:
                                squaresEmpty = False
                                break
                                
                        if kingInSight == True and squaresEmpty == True:
                            return True
                        
                    #This is similar to the previous elif block but just checks if the king is to the right instead of the left of the rook 
                    elif (pieceRow == enemyPieceRow == kingRow) and (enemyPieceColumn < pieceColumn < kingColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves:
                        kingInSight = True

                        squaresEmpty = True
                        for column in range(pieceColumn + 1, kingColumn):
                            if self.board.board[enemyPieceRow][column].piece != None:
                                squaresEmpty = False
                                break
                            
                        if kingInSight == True and squaresEmpty == True:
                            return True

                if enemyPiece == 'Queen' or enemyPiece == 'Bishop':
                    #This checks if the piece is between the bishop and king in the top-left to bottom-right diagonal
                    if (enemyPieceRow < pieceRow < kingRow) and (enemyPieceColumn < pieceColumn < kingColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = kingRow - pieceRow

                        for i in range(1, squares): 
                            #This makes it so that the row and column increment by the same amount so that way only diagonals are considered. 
                            row  = pieceRow + i 
                            column = pieceColumn + i
                            #This checks if the squares between the piece and king are occupied 
                            if self.board.board[row][column].piece != None: 
                                squaresEmpty = False 
                                break 
                        
                        if kingInSight == True and squaresEmpty == True: 
                            return True

                    #This checks if the piece is between the bishop and king in the top-right to bottom-left diagonal
                    elif (enemyPieceRow < pieceRow < kingRow) and (kingColumn < pieceColumn < enemyPieceColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = kingRow - pieceRow

                        #Uses same logic as previous elif block
                        for i in range(1, squares):
                            #This ensures the only the diagonals are checked.
                            row  = pieceRow + i
                            column = pieceColumn - i

                            #This checks if the squares between the piece and king are occupied
                            if self.board.board[row][column].piece != None:
                                squaresEmpty = False
                                break

                        if kingInSight == True and squaresEmpty == True:
                            return True
                    
                    #This checks if the piece is between the bishop and king in the bottom-left to top-right diagonal
                    elif (kingRow < pieceRow < enemyPieceRow) and (enemyPieceColumn < pieceColumn < kingColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = pieceRow - kingRow

                        #Uses same logic as previous elif block
                        for i in range(1, squares):
                            #This ensures the only the diagonals are checked.
                            row  = pieceRow - i
                            column = pieceColumn + i

                            #This checks if the squares between the piece and king are occupied
                            if self.board.board[row][column].piece != None:
                                squaresEmpty = False
                                break

                        if kingInSight == True and squaresEmpty == True:
                            return True
                        
                    #This checks if the piece is between the bishop and king in the bottom-right to top-left diagonal
                    elif (kingRow < pieceRow < enemyPieceRow) and (kingColumn < pieceColumn < enemyPieceColumn)\
                    and (pieceRow, pieceColumn) in enemyPieceMoves and (kingRow, kingColumn) in enemyPinMoves:
                        kingInSight = True

                        squaresEmpty = True
                        squares = pieceRow - kingRow

                        #Uses same logic as previous elif block
                        for i in range(1, squares):
                            #This ensures the only the diagonals are checked.
                            row  = pieceRow - i
                            column = pieceColumn - i

                            #This checks if the squares between the piece and king are occupied
                            if self.board.board[row][column].piece != None:
                                squaresEmpty = False
                                break

                        if kingInSight == True and squaresEmpty == True:
                            return True
                