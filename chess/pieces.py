import os

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

    def GetValidMoves(self, board, row, column):
        moves = []
        #Checks the colour of the piece at the current row and column
        if board[row][column].piece.colour == 'White':
            direction = -1 #White moves up
        else:
            direction = 1 #Black moves down

        #Checks if the pawns are on their starting rows to allow them move two squares up but checks if both squares are empty first
        if (board[row][column].piece.colour == 'White' and row == 6) or (board[row][column].piece.colour == 'Black' and row == 1):
            if board[row + direction][column].piece is None and board[row + 2 * direction][column].piece is None:
                moves.append((row + 2 * direction, column))
        
        #Allows the pawns move one square up as normal
        if 0 <= row + direction <= 7 and board[row + direction][column].piece is None:
            moves.append((row + direction, column))

        #Responsible for diagonal captures
        for col in [-1, 1]:
            newColumn = column + col
            
            #Checks if the diagonal capture squares are within bounds of the board
            if 1 <= newColumn <= 8 and row < 7:
                square = board[row + direction][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                #Only makes it a valid move if there is a piece at the potential diagonal capture square and the piece there is not
                # the same colour as the pawn 
                if piece is not None and piece.colour != piece2.colour:
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

    def GetValidMoves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                else:
                    #It stops if it encounters a piece of the same colour
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    break
                else:
                    break  

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column + dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    break
                else:
                    break

        return moves
    
    def GetControlMoves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square the same as the piece
                #in one of the valid squares so it can defend it from the king.
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                    break
                #If the piece it encounters is a king, it skips that square and adds the ones behind it.
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    #If it encounters a piece of opposite colour that is not a king, it stops.
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column + dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        return moves
    
    def GetPinMoves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, newColumn))
                #If it encounters a piece of opposite colour that is not a king it skips it
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                #If it encounters a king of opposite colour, it adds it to the moves list and stops
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    break
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break 

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column + dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        return moves

class Knight(Piece):
    def __init__(self, colour):
        super().__init__('Knight', colour, 3.0)

    def GetValidMoves(self, board, row, column):
        moves = []
        direction1 = 1
        direction2 = 2

        for col in [-1, 1]:
            newColumn = column + col
            newRow = row - direction2

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None :
                    moves.append((newRow, newColumn))
                #Checks if the piece in the valid square is not the same colour as the current piece
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
            
        for col in [-1, 1]:
            newColumn = column + col
            newRow = row + direction2

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))

        for col in [-2, 2]:
            newColumn = column + col
            newRow = row - direction1

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))

        for col in [-2, 2]:
            newColumn = column + col
            newRow = row + direction1

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
        
        return moves
    
    def GetControlMoves(self, board, row, column):
        moves = []
        direction1 = 1
        direction2 = 2

        for col in [-1, 1]:
            newColumn = column + col
            newRow = row - direction2

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None :
                    moves.append((newRow, newColumn))
                #Defending its own piece so king cant capture
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
            
        for col in [-1, 1]:
            newColumn = column + col
            newRow = row + direction2

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))

        for col in [-2, 2]:
            newColumn = column + col
            newRow = row - direction1

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))

        for col in [-2, 2]:
            newColumn = column + col
            newRow = row + direction1

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
        
        return moves
   
class Rook(Piece):
    def __init__(self, colour):
        super().__init__('Rook', colour, 5.0)

    def GetValidMoves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour:
                    moves.append((newRow, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                else:
                    #It stops if it encounters a piece of the same colour
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            newRow = row - dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, column))
                    break
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((row, newColumn))
                    break
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            newColumn = column - dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((row, newColumn))
                    break
                else:
                    break

        return moves
    
    def GetControlMoves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, column))
                #Checks if piece in valid square is same colour so it can defend it.
                elif piece2.colour == piece.colour:
                    moves.append((newRow, column))
                    #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                    break
                #If it encounters a king, it skips and adds the squares behind it.
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            newRow = row - dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((row, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            newColumn = column - dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((row, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        return moves
    
    def GetPinMoves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            newRow = row - dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break 

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            newColumn = column - dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        return moves

class Queen(Piece):
    def __init__(self, colour):
        super().__init__('Queen', colour, 9.0)

    def GetValidMoves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, column))
                    break
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            newRow = row - dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, column))
                    break
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((row, newColumn))
                    break
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            newColumn = column - dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((row, newColumn))
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                #Checks if the square is not occupied or the piece at that square is of a different colour to allow captures
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    break
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    break
                else:
                    break  

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column + dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))
                    break
                else:
                    break
       
        return moves
    
    def GetControlMoves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square the same as the piece
                #in one of the valid squares to defend it.
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                    break
                #If it encounters a king, it skips it and adds the squares behind it
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column + dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((newRow, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, column))
                #Checks if piece in valid square is same colour so it can defend it.
                elif piece2.colour == piece.colour:
                    moves.append((newRow, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            newRow = row - dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((row, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            newColumn = column - dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour == piece.colour:
                    moves.append((row, newColumn))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        return moves
    
    def GetPinMoves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            newRow = row + dir
            newColumn = column - dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            newRow = row - dir
            newColumn = column + dir

            if 0 <= newRow <= 7 and 1 <= newColumn <= 8:
                square = board[newRow][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((newRow, column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            newRow = row - dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((newRow, column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break 

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            newColumn = column - dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, newColumn))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        return moves

class King(Piece):
    def __init__(self, colour):
        super().__init__('King', colour, 100000)

    def GetValidMoves(self, board, row, column):
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

                #Checks if the square it's moving to is empty
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the piece at the square it's moving to is of a different colour and not a king
                elif piece2.colour != piece.colour:
                    moves.append((newRow, newColumn))

        #Responsible for movement in the horizontal left and right directions
        for dir in [-1, 1]:
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None: 
                    moves.append((row, newColumn))
                elif piece2.colour != piece.colour:
                    moves.append((row, newColumn))

        #Responsible for movement in the vertical top and bottom directions
        for dir in [-1, 1]:
            newRow = row + dir

            if 0 <= newRow <= 7:
                square = board[newRow][column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour != piece.colour:
                    moves.append((newRow, column))

        #Responsible for movement in the bottom left direction
        if 0 <= row + direction <= 7 and 1 <= column - direction <= 8:
            square = board[row + direction][column - direction]
            piece = square.piece
            piece2 = board[row][column].piece

            if piece is None:
                moves.append((row + direction, column - direction))
            elif piece2.colour != piece.colour:
                moves.append((row + direction, column - direction))

        #Responsible for movement in the top right direction
        if 0 <= row - direction <= 7 and 1 <= column + direction <= 8:
            square = board[row - direction][column + direction]
            piece = square.piece
            piece2 = board[row][column].piece

            if piece is None:
                moves.append((row - direction, column + direction))
            elif piece2.colour != piece.colour:
                moves.append((row - direction, column + direction))

        return moves
    
    def GetControlMoves(self, board, row, column):
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

                #Checks if the square it's moving to is empty
                if piece is None:
                    moves.append((newRow, newColumn))
                #Checks if the piece at the square is the same colour so it can defend it.
                elif piece2.colour == piece.colour:
                    moves.append((newRow, newColumn))

        #Responsible for movement in the horizontal left and right directions
        for dir in [-1, 1]:
            newColumn = column + dir

            if 1 <= newColumn <= 8:
                square = board[row][newColumn]
                piece = square.piece
                piece2 = board[row][column].piece

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

                if piece is None:
                    moves.append((newRow, column))
                elif piece2.colour == piece.colour:
                    moves.append((newRow, column))

        #Responsible for movement in the bottom left direction
        if 0 <= row + direction <= 7 and 1 <= column - direction <= 8:
            square = board[row + direction][column - direction]
            piece = square.piece
            piece2 = board[row][column].piece

            if piece is None:
                moves.append((row + direction, column - direction))
            elif piece2.colour == piece.colour:
                moves.append((row + direction, column - direction))

        #Responsible for movement in the top right direction
        if 0 <= row - direction <= 7 and 1 <= column + direction <= 8:
            square = board[row - direction][column + direction]
            piece = square.piece
            piece2 = board[row][column].piece

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
    
    
    




        
        

        



        

        

        



