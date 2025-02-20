import os
import operator

# This dictionary is used to map a string to its correct operator using the in-buit operator module.
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
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Pawn', colour, 1) # The number indicates the pawn's relative value

    def GetValidMoves(self, board, row, column, condition=None):
        moves = []
        currentSquare = board[row][column]

        # Checks the colour of the piece at the current row and column
        if currentSquare.piece.colour == 'White':
            direction = -1 # White moves up
        else:
            direction = 1 # Black moves down

        # Checks if the pawns are on their starting rows to allow them move two squares up but checks if both squares are empty first
        if (currentSquare.piece.colour == 'White' and row == 6) or (currentSquare.piece.colour == 'Black' and row == 1):
            if board[row + direction][column].piece == None and board[row + 2 * direction][column].piece == None:
                moves.append((row + 2 * direction, column))
        
        # Allows the pawns move one square up as normal
        if 0 <= row + direction <= 7 and board[row + direction][column].piece == None:
            moves.append((row + direction, column))

        # Responsible for diagonal captures
        for col in [-1, 1]:
            newColumn = column + col
            
            # Checks if the diagonal capture squares are within bounds of the board
            # But doesn't consider the last row because row + direction (7 + 1) would go out of bounds
            if 1 <= newColumn <= 8 and row < 7:
                newSquare = board[row + direction][newColumn]

                # Checks to ensure an opponent piece is present for a diagonal capture to be possible
                if newSquare.piece != None and newSquare.piece.colour != currentSquare.piece.colour:
                    moves.append((row + direction, newColumn))

        if condition == 'Control':
            return self.GetControlMoves(board, row, column)
                
        return moves
    
    def GetControlMoves(self, board, row, column):
        moves = []
        currentSquare = board[row][column]

        if currentSquare.piece.colour == 'White':
            direction = -1 # White moves up
        else:
            direction = 1 # Black moves down

        for col in [-1, 1]:
            newColumn = column + col
            
            # Checks if the diagonal capture squares are within bounds of the board
            # But doesn't consider the last row because row + direction (7 + 1) would go out of bounds
            if 1 <= newColumn <= 8 and row < 7:
                newSquare = board[row + direction][newColumn]

                #Checks if the square is empty or contains a friendly piece so it can defend that piece from the king.
                if newSquare.piece == None or (newSquare.piece.colour == currentSquare.piece.colour):
                    moves.append((row + direction, newColumn))
                
        return moves
    
    def EnPassant(self, board, row, column):
        move = []
        currentSquare = board[row][column]

        if currentSquare.piece.colour == 'White':
            correctRow = 3
            direction = -1 # White moves up
        else:
            correctRow = 4
            direction = 1 # Black moves down

        for col in [-1, 1]:
            newColumn = column + col

            if 1 <= newColumn <= 8 and 0 <= row + direction <= 7:
                newSquare = board[row][newColumn]
                captureSquare = board[row + direction][newColumn]

                if row == correctRow and newSquare.piece != None and newSquare.piece.name == 'Pawn'\
                and newSquare.piece.colour != currentSquare.piece.colour and captureSquare.piece == None:
                    move.append((row + direction, newColumn))

        return move

class Bishop(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Bishop', colour, 3.5) # The number indicates the bishop's relative value

    def GetValidMoves(self, board, row, column, condition=None):
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
                    newSquare = board[newRow][newColumn]
                    currentSquare = board[row][column]

                    if condition == None:
                        # Checks if the square to move to is empty
                        if newSquare.piece == None:
                            moves.append((newRow, newColumn))
                        # Checks if the colour of the current piece is not the same as a piece encountered
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, newColumn))
                            # If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                            break
                        else:
                            # It stops if it encounters a piece of the same colour
                            break

                    elif condition == 'Control':
                        #Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, newColumn))
                        # Checks if the colour of the current piece is the same as the piece encountered so it can defend if from the king
                        elif currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((newRow, newColumn))
                            # If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                            break
                        # If the piece it encounters is a king, it skips that square and adds the ones behind it.
                        elif newSquare.piece.name == 'King' and currentSquare.piece.colour != newSquare.piece.colour:
                            continue
                        else:
                            #If it encounters a piece of opposite colour that is not a king, it stops.
                            break

                    elif condition == 'Pin':
                        # Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, newColumn))
                        # If it encounters a piece of opposite colour that is not a king it skips it
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name != 'King':
                            continue
                        # If it encounters a king of opposite colour, it adds it to the moves list and stops
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name == 'King':
                            moves.append((newRow, newColumn))
                            break
                        else:
                            # If it encounters a friendly piece it stops
                            break
        return moves

class Knight(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Knight', colour, 3) # The number indicates the knight's relative value

    def GetValidMoves(self, board, row, column, condition=None):
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
                    newSquare = board[newRow][newColumn]
                    currentSquare = board[row][column]

                    if condition == None:
                        # Checks if the square encountered is empty or contains an enemy piece
                        if newSquare.piece == None or currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, newColumn))

                    elif condition == 'Control':
                        # Checks if the square encountered is empty or contains a friendly piece so it can defend it from the king
                        if newSquare.piece == None or currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((newRow, newColumn))

            for col in [-2, 2]:
                newRow = op1(row, direction1)
                newColumn = op2(column, col)

                if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                    newSquare = board[newRow][newColumn]
                    currentSquare = board[row][column]

                    if condition == None:
                        # Checks if the square encountered is empty or contains an enemy piece
                        if newSquare.piece == None or currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, newColumn))

                    elif condition == 'Control':
                        # Checks if the square encountered is empty or contains a friendly piece so it can defend it from the king
                        if newSquare.piece == None or currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((newRow, newColumn))

        return moves
   
class Rook(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Rook', colour, 5) # The number indicates the rook's relative value

    def GetValidMoves(self, board, row, column, condition=None):
        moves = []

        operatorPairs = ['+', '-']

        # Responsible for vertical moves 
        for ops in operatorPairs:
            for direction in range(1, 8):
                op1 = operators[ops]
                newRow = op1(row, direction)

                if 0 <= newRow <= 7:
                    newSquare = board[newRow][column]
                    currentSquare = board[row][column]
                    if condition == None:
                        #Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, column))
                        #Checks if the colour of the piece at the current square is not the same as the piece
                        #in one of the valid squares.
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, column))
                            #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                            break
                        else:
                            #It stops if it encounters a piece of the same colour
                            break

                    elif condition == 'Control':
                        #Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, column))
                        #Checks if piece in valid square is same colour so it can defend it.
                        elif currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((newRow, column))
                            #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                            break
                        #If it encounters a king, it skips and adds the squares behind it.
                        elif newSquare.piece.name == 'King' and currentSquare.piece.colour != newSquare.piece.colour:
                            continue
                        else:
                            break

                    elif condition == 'Pin':
                        #Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, column))
                        #Checks if the colour of the piece at the current square is not the same as the piece
                        #in one of the valid squares.
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name != 'King':
                            continue
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name == 'King':
                            moves.append((newRow, column))
                            #It stops if it encounters a piece of the same colour
                            break 
                        else:
                            break

            # Responsible for horizontal moves
            for direction in range(1, 8):
                newColumn = op1(column, direction)

                if 1 <= newColumn <= 8:
                    newSquare = board[row][newColumn]
                    currentSquare = board[row][column]
                    if condition == None:
                        if newSquare.piece == None:
                            moves.append((row, newColumn))
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((row, newColumn))
                            break
                        else:
                            break

                    elif condition == 'Control':
                        #Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((row, newColumn))
                        #Checks if piece in valid square is same colour so it can defend it.
                        elif currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((row, newColumn))
                            #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                            break
                        #If it encounters a king, it skips and adds the squares behind it.
                        elif newSquare.piece.name == 'King' and currentSquare.piece.colour != newSquare.piece.colour:
                            continue
                        else:
                            break

                    elif condition == 'Pin':
                        #Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((row, newColumn))
                        #Checks if the colour of the piece at the current square is not the same as the piece
                        #in one of the valid squares.
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name != 'King':
                            continue
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name == 'King':
                            moves.append((row, newColumn))
                            #It stops if it encounters a piece of the same colour
                            break 
                        else:
                            # It stops if it encounters a friendly piece
                            break

        return moves

class Queen(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Queen', colour, 9) # The number indicates the queens's relative value

        self.rook = Rook(colour)
        self.bishop = Bishop(colour)

    def GetValidMoves(self, board, row, column, condition=None):
        moves = []

        # The queen just has the moves of the rook and a bishop combined
        if condition != None:
            moves.extend(self.rook.GetValidMoves(board, row, column, condition))
            moves.extend(self.bishop.GetValidMoves(board, row, column, condition))
        else:
            moves.extend(self.rook.GetValidMoves(board, row, column))
            moves.extend(self.bishop.GetValidMoves(board, row, column))
       
        return moves

class King(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('King', colour, 100000) # The king doesn't need a value but I just gave it the largest one anyways

    def GetValidMoves(self, board, row, column, condition=None):
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

                if condition == None:
                    #Checks if the square it's moving to is empty
                    if piece == None:
                        moves.append((newRow, newColumn))
                    #Checks if the piece at the square it's moving to is of a different colour and not a king
                    elif piece2.colour != piece.colour:
                        moves.append((newRow, newColumn))

                elif condition == 'Control':
                    #Checks if the square it's moving to is empty
                    if piece == None:
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

                if condition == None:
                    if piece == None: 
                        moves.append((row, newColumn))
                    elif piece2.colour != piece.colour:
                        moves.append((row, newColumn))

                elif condition == 'Control':
                    if piece == None: 
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

                if condition == None:
                    if piece == None:
                        moves.append((newRow, column))
                    elif piece2.colour != piece.colour:
                        moves.append((newRow, column))

                elif condition == 'Control':
                    if piece == None:
                        moves.append((newRow, column))
                    elif piece2.colour == piece.colour:
                        moves.append((newRow, column))

        #Responsible for movement in the bottom left direction
        if 0 <= row + direction <= 7 and 1 <= column - direction <= 8:
            square = board[row + direction][column - direction]
            piece = square.piece
            piece2 = board[row][column].piece

            if condition == None:
                if piece == None:
                    moves.append((row + direction, column - direction))
                elif piece2.colour != piece.colour:
                    moves.append((row + direction, column - direction))

            elif condition == 'Control':
                if piece == None:
                    moves.append((row + direction, column - direction))
                elif piece2.colour == piece.colour:
                    moves.append((row + direction, column - direction))

        #Responsible for movement in the top right direction
        if 0 <= row - direction <= 7 and 1 <= column + direction <= 8:
            square = board[row - direction][column + direction]
            piece = square.piece
            piece2 = board[row][column].piece

            if condition == None:
                if piece == None:
                    moves.append((row - direction, column + direction))
                elif piece2.colour != piece.colour:
                    moves.append((row - direction, column + direction))

            elif condition == 'Control':
                if piece == None:
                    moves.append((row - direction, column + direction))
                elif piece2.colour == piece.colour:
                    moves.append((row - direction, column + direction))

        return moves
    
    def GetShortCastleMoves(self, board, row, column):
        moves = []
        # Checks if it's black or white by checking the row. row 7 for white, row 0 for black
        if (row == 7 or row == 0) and column == 5:
            # Checks if the squares between the king and the king's rook are empty
            if board[row][column + 1].piece == None and board[row][column + 2].piece == None:
                moves.append((row, column + 2))

        return moves
    
    def GetLongCastleMoves(self, board, row, column):
        moves = []
        # Checks if it's black or white by checking the row
        if (row == 7 or row == 0) and column == 5:
            # Checks if the three squares between the king and the queen's rook are empty
            if board[row][column - 1].piece == None and board[row][column - 2].piece == None and board[row][column - 3].piece == None:
                moves.append((row, column - 2))

        return moves
    
    
    




        
        

        



        

        

        



