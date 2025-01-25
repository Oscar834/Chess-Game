import os
import operator

operators = {'+': operator.add, '-': operator.sub}

class Piece:
    def __init__(self, name, colour, value, image=None, imageRect=None):
        self.name = name
        self.colour = colour
        self.image = image
        self.value = value
        self.DisplayPieceImages()
        self.imageRect = imageRect

    def DisplayPieceImages(self):
        self.image = os.path.join(f"Piece Images/{self.colour} {self.name}.png")

class Pawn(Piece):
    def __init__(self, colour):
        #Using inheritance so I don't have to write all the code in the __init__ method for each piece.
        super().__init__('Pawn', colour, 1.0)

    def GetValidMoves(self, board, row, column, type=None):
        moves = []
        #Checks the colour of the piece at the current row and column
        if board[row][column].piece.colour == 'White':
            direction = -1 # White moves up
        else:
            direction = 1 # Black moves down

        if type == 'Control':
            return self.GetControlMoves(board, row, column)

        else:
            # Checks if the pawns are on their starting rows to allow them move two squares up but checks if both squares are empty first
            if (board[row][column].piece.colour == 'White' and row == 6) or (board[row][column].piece.colour == 'Black' and row == 1):
                if board[row + direction][column].piece is None and board[row + 2 * direction][column].piece is None:
                    moves.append((row + 2 * direction, column))
            
            # Allows the pawns move one square up as normal
            if 0 <= row + direction <= 7 and board[row + direction][column].piece is None:
                moves.append((row + direction, column))

            # Responsible for diagonal captures
            for col in [-1, 1]:
                newColumn = column + col
                
                # Checks if the diagonal capture squares are within bounds of the board
                if 1 <= newColumn <= 8 and row < 7:
                    newPiece = board[row + direction][newColumn].piece
                    currentPiece = board[row][column].piece

                    # Checks to ensure an opponent piece is present for a diagonal capture to be possible
                    if newPiece != None and newPiece.colour != currentPiece.colour:
                        moves.append((row + direction, newColumn))
                
        return moves
    
    def GetControlMoves(self, board, row, column):
        moves = []

        if board[row][column].piece.colour == 'White':
            direction = -1 #White moves up
        else:
            direction = 1 #Black moves down

        for col in [-1, 1]:
            newColumn = column + col
            
            #Checks if the diagonal capture squares are within bounds of the board
            if 1 <= newColumn <= 8 and row < 7:
                square = board[row + direction][newColumn]
                piece = square.piece
                #Checks if the square is empty or another piece of same colour is there so it can defend that piece from the king.
                if piece is None or (piece.colour == board[row][column].piece.colour):
                    moves.append((row + direction, newColumn))
                
        return moves

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__('Bishop', colour, 3.0)

    def GetValidMoves(self, board, row, column, type=None):
        moves = []

        operatorPairs = [('+', '+'), ('-', '-'), ('+', '-'), ('-', '+')]

        # Responsible for diagonal moves in the bottom right direction
        for ops in operatorPairs:
            for direction in range(1, 8):
                op1 = operators[ops[0]]
                op2 = operators[ops[1]]
                newRow = op1(row, direction)
                newColumn = op2(column, direction)

                # Checks to see if the new row and column to move to is within the bounds of the board
                if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                    newPiece = board[newRow][newColumn].piece # It would be None if the square is empty
                    currentPiece = board[row][column].piece

                    if type == None:
                        #Checks if the square to move to is empty
                        if newPiece is None:
                            moves.append((newRow, newColumn))
                        # Checks if the colour of the current piece is not the same as a piece encountered
                        elif currentPiece.colour != newPiece.colour:
                            moves.append((newRow, newColumn))
                            # If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                            break
                        else:
                            # It stops if it encounters a piece of the same colour
                            break

                    elif type == 'Control':
                        #Checks if the square is empty
                        if newPiece is None:
                            moves.append((newRow, newColumn))
                        # Checks if the colour of the current piece is the same as the piece encountered so it can defend if from the king
                        elif currentPiece.colour == newPiece.colour:
                            moves.append((newRow, newColumn))
                            # If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                            break
                        # If the piece it encounters is a king, it skips that square and adds the ones behind it.
                        elif newPiece.name == 'King' and currentPiece.colour != newPiece.colour:
                            continue
                        else:
                            #If it encounters a piece of opposite colour that is not a king, it stops.
                            break

                    elif type == 'Pin':
                        # Checks if the square is empty
                        if newPiece is None:
                            moves.append((newRow, newColumn))
                        # If it encounters a piece of opposite colour that is not a king it skips it
                        elif currentPiece.colour != newPiece.colour and newPiece.name != 'King':
                            continue
                        # If it encounters a king of opposite colour, it adds it to the moves list and stops
                        elif currentPiece.colour != newPiece.colour and newPiece.name == 'King':
                            moves.append((newRow, newColumn))
                            break
                        else:
                            break
        return moves

class Knight(Piece):
    def __init__(self, colour):
        super().__init__('Knight', colour, 3.0)

    def GetValidMoves(self, board, row, column, control=None):
        moves = []

        operatorPairs = [('-', '+'), ('+', '+')]
        direction1 = 1
        direction2 = 2

        for ops in operatorPairs:
            for col in [-1, 1]:
                op1 = operators[ops[0]]
                op2 = operators[ops[1]]
                newRow = op1(row, direction2)
                newColumn = op2(column, col)

                if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                    newPiece = board[newRow][newColumn].piece
                    currentPiece = board[row][column].piece
                    # Checks if the square encountered is empty
                    if control == None:
                        if newPiece is None:
                            moves.append((newRow, newColumn))
                        #Checks if the piece in the valid square is not the same colour as the current piece
                        elif currentPiece.colour != newPiece.colour:
                            moves.append((newRow, newColumn))
                    elif control == 'Control':
                        if newPiece is None:
                            moves.append((newRow, newColumn))
                        #Checks if the piece in the valid square is not the same colour as the current piece
                        elif currentPiece.colour == newPiece.colour:
                            moves.append((newRow, newColumn))

            for col in [-2, 2]:
                newRow = op1(row, direction1)
                newColumn = op2(column, col)

                if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                    newPiece = board[newRow][newColumn].piece
                    currentPiece = board[row][column].piece
                    # Checks if the square encountered is empty
                    if control == None:
                        if newPiece is None:
                            moves.append((newRow, newColumn))
                        #Checks if the piece in the valid square is not the same colour as the current piece
                        elif currentPiece.colour != newPiece.colour:
                            moves.append((newRow, newColumn))
                    elif control == 'Control':
                        if newPiece is None:
                            moves.append((newRow, newColumn))
                        #Checks if the piece in the valid square is not the same colour as the current piece
                        elif currentPiece.colour == newPiece.colour:
                            moves.append((newRow, newColumn))
        
        return moves
   
class Rook(Piece):
    def __init__(self, colour):
        super().__init__('Rook', colour, 5.0)

    def GetValidMoves(self, board, row, column, type=None):
        moves = []

        operatorPairs = ['+', '-']

        #Responsible for vertical moves downwards
        for ops in operatorPairs:
            for direction in range(1, 8):
                op1 = operators[ops]
                newRow = op1(row, direction)

                if 0 <= newRow <= 7:
                    newPiece = board[newRow][column].piece
                    currentPiece = board[row][column].piece
                    if type == None:
                        #Checks if the square is empty
                        if newPiece is None:
                            moves.append((newRow, column))
                        #Checks if the colour of the piece at the current square is not the same as the piece
                        #in one of the valid squares.
                        elif currentPiece.colour != newPiece.colour:
                            moves.append((newRow, column))
                            #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                            break
                        else:
                            #It stops if it encounters a piece of the same colour
                            break
                    elif type == 'Control':
                        #Checks if the square is empty
                        if newPiece is None:
                            moves.append((newRow, column))
                        #Checks if piece in valid square is same colour so it can defend it.
                        elif currentPiece.colour == newPiece.colour:
                            moves.append((newRow, column))
                            #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                            break
                        #If it encounters a king, it skips and adds the squares behind it.
                        elif newPiece.name == 'King' and currentPiece.colour != newPiece.colour:
                            continue
                        else:
                            break
                    elif type == 'Pin':
                        #Checks if the square is empty
                        if newPiece is None:
                            moves.append((newRow, column))
                        #Checks if the colour of the piece at the current square is not the same as the piece
                        #in one of the valid squares.
                        elif currentPiece.colour != newPiece.colour and newPiece.name != 'King':
                            continue
                        elif currentPiece.colour != newPiece.colour and newPiece.name == 'King':
                            moves.append((newRow, column))
                            #It stops if it encounters a piece of the same colour
                            break 
                        else:
                            break

            for direction in range(1, 8):
                newColumn = op1(column, direction)

                if 1 <= newColumn <= 8:
                    newPiece = board[row][newColumn].piece
                    currentPiece = board[row][column].piece
                    if type == None:
                        if newPiece is None:
                            moves.append((row, newColumn))
                        elif currentPiece.colour != newPiece.colour:
                            moves.append((row, newColumn))
                            break
                        else:
                            break
                    elif type == 'Control':
                        #Checks if the square is empty
                        if newPiece is None:
                            moves.append((row, newColumn))
                        #Checks if piece in valid square is same colour so it can defend it.
                        elif currentPiece.colour == newPiece.colour:
                            moves.append((row, newColumn))
                            #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                            break
                        #If it encounters a king, it skips and adds the squares behind it.
                        elif newPiece.name == 'King' and currentPiece.colour != newPiece.colour:
                            continue
                        else:
                            break
                    elif type == 'Pin':
                        #Checks if the square is empty
                        if newPiece is None:
                            moves.append((row, newColumn))
                        #Checks if the colour of the piece at the current square is not the same as the piece
                        #in one of the valid squares.
                        elif currentPiece.colour != newPiece.colour and newPiece.name != 'King':
                            continue
                        elif currentPiece.colour != newPiece.colour and newPiece.name == 'King':
                            moves.append((row, newColumn))
                            #It stops if it encounters a piece of the same colour
                            break 
                        else:
                            break

        return moves

class Queen(Piece):
    def __init__(self, colour):
        super().__init__('Queen', colour, 9.0)
        self.rook = Rook(colour)
        self.bishop = Bishop(colour)

    def GetValidMoves(self, board, row, column, type=None):
        moves = []

        # The queen just has the moves of the rook and a bishop combined
        if type != None:
            moves.extend(self.rook.GetValidMoves(board, row, column, type))
            moves.extend(self.bishop.GetValidMoves(board, row, column, type))
        else:
            moves.extend(self.rook.GetValidMoves(board, row, column))
            moves.extend(self.bishop.GetValidMoves(board, row, column))
       
        return moves

class King(Piece):
    def __init__(self, colour):
        super().__init__('King', colour, 100000.0)

    def GetValidMoves(self, board, row, column, type=None):
        moves = []
        direction = 1
        
        #Responsible for movement in the top left and bottom right directions
        for dir in [-1, 1]:
            newRow = row + dir
            newColumn = column + dir
        
            #Checks if the new row and new column are within the bounds of the board
            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if type == None:
                    #Checks if the square it's moving to is empty
                    if piece is None:
                        moves.append((newRow, newColumn))
                    #Checks if the piece at the square it's moving to is of a different colour and not a king
                    elif piece2.colour != piece.colour:
                        moves.append((newRow, newColumn))
                elif type == 'Control':
                    #Checks if the square it's moving to is empty
                    if piece is None:
                        moves.append((newRow, newColumn))
                    #Checks if the piece at the square it's moving to is of a different colour and not a king
                    elif piece2.colour == piece.colour:
                        moves.append((newRow, newColumn))

        #Responsible for movement in the horizontal left and right directions
        for dir in [-1, 1]:
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if type == None:
                    if piece is None: 
                        moves.append((row, newColumn))
                    elif piece2.colour != piece.colour:
                        moves.append((row, newColumn))
                elif type == 'Control':
                    if piece is None: 
                        moves.append((row, newColumn))
                    elif piece2.colour == piece.colour:
                        moves.append((row, newColumn))

        #Responsible for movement in the vertical top and bottom directions
        for dir in [-1, 1]:
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece

                if type == None:
                    if piece is None:
                        moves.append((newRow, column))
                    elif piece2.colour != piece.colour:
                        moves.append((newRow, column))
                elif type == 'Control':
                    if piece is None:
                        moves.append((newRow, column))
                    elif piece2.colour == piece.colour:
                        moves.append((newRow, column))

        #Responsible for movement in the bottom left direction
        if 0 <= row + direction <= 7 and 1 <= column - direction <= 8:
            square = board[row + direction][column - direction]
            piece = square.piece
            piece2 = board[row][column].piece

            if type == None:
                if piece is None:
                    moves.append((row + direction, column - direction))
                elif piece2.colour != piece.colour:
                    moves.append((row + direction, column - direction))
            elif type == 'Control':
                if piece is None:
                    moves.append((row + direction, column - direction))
                elif piece2.colour == piece.colour:
                    moves.append((row + direction, column - direction))

        #Responsible for movement in the top right direction
        if 0 <= row - direction <= 7 and 1 <= column + direction <= 8:
            square = board[row - direction][column + direction]
            piece = square.piece
            piece2 = board[row][column].piece

            if type == None:
                if piece is None:
                    moves.append((row - direction, column + direction))
                elif piece2.colour != piece.colour:
                    moves.append((row - direction, column + direction))
            elif type == 'Control':
                if piece is None:
                    moves.append((row - direction, column + direction))
                elif piece2.colour == piece.colour:
                    moves.append((row - direction, column + direction))

        return moves
    
    def GetShortCastleMoves(self, board, row, column):
        moves = []
        #Checks if it's black or white by checking the row
        if (row == 7 or row == 0) and column == 5:
            #Checks if the squares between the king and the rook on the right are empty
            if board[row][column + 1].piece is None and board[row][column + 2].piece is None:
                moves.append((row, column + 2))

        return moves
    
    def GetLongCastleMoves(self, board, row, column):
        moves = []
        #Checks if it's black or white by checking the row
        if (row == 7 or row == 0) and column == 5:
            #Checks if the three squares between the king and rook on the left are empty
            if board[row][column - 1].piece is None and board[row][column - 2].piece is None and board[row][column - 3].piece is None:
                moves.append((row, column - 2))

        return moves
    
    
    




        
        

        



        

        

        



