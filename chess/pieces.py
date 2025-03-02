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
            if 1 <= newColumn <= 8:
                newSquare = board[row + direction][newColumn]

                # Checks to ensure an opponent piece is present for a diagonal capture to be possible
                if newSquare.piece != None and newSquare.piece.colour != currentSquare.piece.colour:
                    moves.append((row + direction, newColumn))

        # Checks if the condition was control and return the control moves instea
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
            if 1 <= newColumn <= 8:
                newSquare = board[row + direction][newColumn]

                # Checks if the square is empty or contains a friendly piece so it can defend that piece from the king.
                if newSquare.piece == None or (newSquare.piece.colour == currentSquare.piece.colour):
                    moves.append((row + direction, newColumn))
                
        return moves
    
    def GetEnPassantMove(self, board, row, column, side):
        move = []
        currentSquare = board[row][column]

        if currentSquare.piece.colour == 'White':
            enPassantRow = 3 # The row the white pawn has to be in for enPassant to occur
            direction = -1 # White moves up
        else:
            enPassantRow = 4 # The row the black pawn has to be in for enPassant to occur
            direction = 1 # Black moves down

        newRow = row + direction # This gets the row the pawn would move to perform the enPassant movement

        # Checks if enPassant is possible to the left of the pawn
        if side == 'left':
            newColumn = column - 1
        # Checks if enPassant is possible to the right of the pawn
        else:
            newColumn = column + 1
        
        # Checks if the new row and new column are within bounds of the board 
        if 1 <= newColumn <= 8 and 0 <= newRow <= 7 and 0 <= row + direction * 2 <= 7:
            newSquare = board[row][newColumn] # This holds the square of the pawn to be removed once the enPassant movement is perfomed
            checkSquare = board[row + direction * 2][newColumn] # This holds the starting square of the pawn to be removed
            captureSquare = board[newRow][newColumn] # This holds the square the pawn would move to perform the enPassant movement

            # Checks if the pawn is on the correct row for enPassant to occur and check if all the basic enPassant conditions are met
            if row == enPassantRow and newSquare.piece != None and newSquare.piece.name == 'Pawn'\
            and newSquare.piece.colour != currentSquare.piece.colour and captureSquare.piece == None\
            and checkSquare.piece == None:
                move.append((newRow, newColumn))

        return move

class Bishop(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Bishop', colour, 3.5) # The number indicates the bishop's relative value
        self.pawn = Pawn(colour)

    def GetValidMoves(self, board, row, column, condition=None):
        moves = []
        currentSquare = board[row][column]

        # The pair (+, +) is responsible for getting the moves for the bishop in the top-left to bottom-right diagonal
        # The pair(-, -) is responsible for getting the moves for the bishop in the bottom-right to top-left diagonal
        # The pair (+, -) is responsible foe getting the moves for the bishop in the top-right to bottom-left diagonal
        # The pair (-, +) is responsible for getting the moves for the bishop in the bottom-left to top-right diagonal
        operatorPairs = [('+', '+'), ('-', '-'), ('+', '-'), ('-', '+')]

        for ops in operatorPairs:
            for direction in range(1, 8): # This for loop with the help of the first loops checks the squares in all directions
                op1 = operators[ops[0]] # Gets the first element of the tuple
                op2 = operators[ops[1]] # Gets the second element of the tuple
                newRow = op1(row, direction) # Same as newRow = row + direction (operator depends on first element of each tuple iterated)
                newColumn = op2(column, direction) # Same as newColumn  = row + direction (operator depends on second element of each tuple iterated)

                # Checks to see if the new row and column to move to is within the bounds of the board
                if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                    newSquare = board[newRow][newColumn] # It would be None if the square is empty

                    # This if block is responsible for normal valid moves
                    if condition == None:
                        # Checks if the square to move to is empty
                        if newSquare.piece == None:
                            moves.append((newRow, newColumn))
                        # Checks if an enemy piece has been encountered
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, newColumn))
                            # If it encounters an enemy piece, it stops so no more moves are added along that direction
                            break
                        else:
                            # It stops if it encounters a friendly piece
                            break

                    # This elif block is responsible for the moves that are used to control king movement
                    elif condition == 'Control':
                        # Checks if the square to move to is empty
                        if newSquare.piece == None:
                            moves.append((newRow, newColumn))
                        # Checks if a friendly piece has been encountered and adds it so it can defend it from the king
                        elif currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((newRow, newColumn))
                            # If it encounters a friendly piece, it stops so no more moves are added along that direction
                            break
                        # If the piece it encounters is an enemy king, it skips that square and adds the ones behind it.
                        elif newSquare.piece.name == 'King' and currentSquare.piece.colour != newSquare.piece.colour:
                            continue
                        else:
                            # If it encounters an enemy piece that is not a king, it stops.
                            break

                    # This is responsible for pin moves
                    elif condition == 'Pin':
                        # Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, newColumn))
                        # If it encounters an enemy piece that is not a king it skips it
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name != 'King':
                            continue
                        # If it encounters an enemy king, it adds it to the moves list and stops
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name == 'King':
                            moves.append((newRow, newColumn))
                            break
                        else:
                            # If it encounters a friendly piece it stops
                            break

                    # This is responsible for skewer moves
                    elif condition == 'Skewer':
                        # Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, newColumn))
                        # Checks if a friendly queen or bishop has been encountered and skips it if so
                        elif currentSquare.piece.colour == newSquare.piece.colour\
                        and newSquare.piece.name == 'Queen' or newSquare.piece.name == 'Bishop':
                            continue
                        # Checks if an enemy piece has been encountered
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, newColumn))
                            break # Stops once an enemy piece has been encountered
                        else:
                            break # It stops if a friendly rook, knight, pawn or king is encountered
                
        return moves

class Knight(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Knight', colour, 3) # The number indicates the knight's relative value

    def GetValidMoves(self, board, row, column, condition=None):
        moves = []
        currentSquare = board[row][column]

        operatorPairs = [('-', '+'), ('+', '+')]
        direction1 = 1
        direction2 = 2

        for ops in operatorPairs:
            # This is responsible for the L-Movement that is 2 squares up/down and then 1 square left/right
            for col in [-1, 1]:
                op1 = operators[ops[0]]
                op2 = operators[ops[1]]
                newRow = op1(row, direction2) # Gets the row 2 squares up (op1 = -) or 2 squares down (op1 = +)
                newColumn = op2(column, col) # Gets the column 1 to the left if col = - or 1 to the right if col = 1

                if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                    newSquare = board[newRow][newColumn]
                    
                    # Responsible for normal moves
                    if condition == None:
                        # Checks if the square encountered is empty or contains an enemy piece
                        if newSquare.piece == None or currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, newColumn))

                    # Responsible for control moves to control king movement
                    elif condition == 'Control':
                        # Checks if the square encountered is empty or contains a friendly piece so it can defend it from the king
                        if newSquare.piece == None or currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((newRow, newColumn))

            # This is responsible for the L-Movement that is 1 square up/down and then 2 squares left/right
            for col in [-2, 2]:
                newRow = op1(row, direction1) # Gets the row 1 squares up (op1 = -) or 1 squares down (op1 = +)
                newColumn = op2(column, col) # Gets the column 2 to the left if col = - or 2 to the right if col = 1

                if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                    newSquare = board[newRow][newColumn]

                    # This if block is responsible for normal valid moves
                    if condition == None:
                        # Checks if the square encountered is empty or contains an enemy piece
                        if newSquare.piece == None or currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, newColumn))
                    
                    # This elif block is responsible for the moves that are used to control king movement
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
        currentSquare = board[row][column]

        operatorPairs = ['+', '-'] # + is for down/right, - is for up/left

        for ops in operatorPairs:
            # Responsible for vertical moves
            for direction in range(1, 8):
                op1 = operators[ops] # Maps the string in operator pairs to the correct operator in the operators dictionary
                newRow = op1(row, direction) # Performs the correct operation

                # Checks if the new row is within the bounds of the board
                if 0 <= newRow <= 7:
                    newSquare = board[newRow][column]
                    
                    # This if block is responsible for the normal valid moves
                    if condition == None:
                        # Checks if the encountered square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, column))
                        # Checks if the new square contains an enemy piece
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, column))
                            # If it encounters an enemy piece, it stops so no more moves are added along that direction
                            break
                        else:
                            # It stops if it encounters a friendly piece
                            break
                    
                    # This elif block is responsible for the moves that are used to control king movement
                    elif condition == 'Control':
                        # Checks if the encountered square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, column))
                        # Checks if the new square contains a friendly piece so it can defend it from the king
                        elif currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((newRow, column))
                            # If it encounters a friendly piece, it stops so no more moves are added along that direction
                            break
                        # If the piece it encounters is an enemy king, it skips that square and adds the ones behind it.
                        elif newSquare.piece.name == 'King' and currentSquare.piece.colour != newSquare.piece.colour:
                            continue
                        else:
                            # If it encounters an enemy piece that is not a king, it stops.
                            break

                    # Responsible for pin moves so it can check if a king is in sight
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

                    # Responsible for skewer moves
                    elif condition == 'Skewer':
                        # Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((newRow, column))
                        # Checks if a friendly rook or queen has been encountered and skips it if so
                        elif currentSquare.piece.colour == newSquare.piece.colour\
                        and (newSquare.piece.name == 'Queen' or newSquare.piece.name == 'Rook'):
                            continue
                        # Checks if an enemy piece has been encountered
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((newRow, column))
                            break # Stops once an enemy piece has been encountered
                        else:
                            break # It stops if it encounters a friendly piece that is not a rook or queen

            # Responsible for horizontal moves
            for direction in range(1, 8):
                newColumn = op1(column, direction) # Perform the correct operation on column and direction

                if 1 <= newColumn <= 8:
                    newSquare = board[row][newColumn]
                    # This if block is responsible for the normal valid moves
                    if condition == None:
                        # Checks if the new square is empty
                        if newSquare.piece == None:
                            moves.append((row, newColumn))
                        # Checks if an enemy piece has been encountered
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((row, newColumn))
                            # If it encounters an enemy piece, it stops so no more moves are added along that direction
                            break
                        else:
                            # It stops if it encounters a friendly piece
                            break

                    # This elif block is responsible for the moves that are used to control king movement
                    elif condition == 'Control':
                        # Checks if the new square is empty
                        if newSquare.piece == None:
                            moves.append((row, newColumn))
                        # Checks if a friendly piece has been encountered so it can defend it from the king
                        elif currentSquare.piece.colour == newSquare.piece.colour:
                            moves.append((row, newColumn))
                            # If it encounters a friendly piece, it stops so no more moves are added along that direction
                            break
                        # If the piece it encounters is an enemy king, it skips that square and adds the ones behind it.
                        elif newSquare.piece.name == 'King' and currentSquare.piece.colour != newSquare.piece.colour:
                            continue
                        else:
                            # If it encounters an enemy piece that is not a king, it stops.
                            break

                    # Responsible for pin moves in the horizontal direction
                    elif condition == 'Pin':
                        #Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((row, newColumn))
                        # Checks if a non-king enemy piece has been encountered and skips it if so
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name != 'King':
                            continue
                        # Checks if an enemy king has been encountered
                        elif currentSquare.piece.colour != newSquare.piece.colour and newSquare.piece.name == 'King':
                            moves.append((row, newColumn))
                            # It stops once it encounters an enemy king
                            break 
                        else:
                            # It stops if it encounters a friendly piece
                            break

                    # Responsible for skewer moves in the horizontal direction
                    elif condition == 'Skewer':
                        # Checks if the square is empty
                        if newSquare.piece == None:
                            moves.append((row, newColumn))
                        # Checks if a friendly rook or queen has been encountered and skips it if so
                        elif currentSquare.piece.colour == newSquare.piece.colour\
                        and (newSquare.piece.name == 'Queen' or newSquare.piece.name == 'Rook'):
                            continue
                        # Checks if an enemy piece has been encountered
                        elif currentSquare.piece.colour != newSquare.piece.colour:
                            moves.append((row, newColumn))
                            break # Stops once an enemy piece has been encountered
                        else:
                            break # It stops if it encounters a friendly piece that is not a rook or queen

        return moves

class Queen(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('Queen', colour, 9) # The number indicates the queens's relative value

        self.rook = Rook(colour)
        self.bishop = Bishop(colour)

    def GetValidMoves(self, board, row, column, condition=None):
        moves = []

        # It adjusts appropriately depending on the condition
        if condition != None:
            moves.extend(self.rook.GetValidMoves(board, row, column, condition))
            moves.extend(self.bishop.GetValidMoves(board, row, column, condition))
        else:
            # The queen just has the moves of the rook and a bishop combined
            moves.extend(self.rook.GetValidMoves(board, row, column))
            moves.extend(self.bishop.GetValidMoves(board, row, column))
       
        return moves

class King(Piece):
    def __init__(self, colour):
        # Using inheritance so I don't have to write all the code in the Piece class constructor for each piece.
        super().__init__('King', colour, 100000) # The king doesn't need a value but I just gave it the largest one anyways

    def GetValidMoves(self, board, row, column, condition=None):
        moves = []
        currentSquare = board[row][column]

        # Loops through each row and column one square from the king in all directions
        for rows in range(row - 1, row + 2):
            for cols in range(column - 1, column + 2):
                # Ensures it within the bounds of the boards
                if 0 <= rows <= 7 and 1 <= cols <= 8 and (rows, cols) != (row, column):
                    newSquare = board[rows][cols]

                    # Responsible for normal moves
                    if condition == None:
                        # Checks if an empty square or an enemy piece has been encountered
                        if newSquare.piece == None or newSquare.piece.colour != currentSquare.piece.colour:
                            moves.append((rows, cols))

                    # Responsible for storing control moves so it can controls squares and defend pieces from the enemy king
                    elif condition == 'Control':
                        # Checks if an emepty square or a friendly piece has been encountered so it can defend it agains the enemy king
                        if newSquare.piece == None or newSquare.piece.colour == currentSquare.piece.colour:
                            moves.append((rows, cols))
                        
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
    
    
    




        
        

        



        

        

        



