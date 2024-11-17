import os

class Piece:
    def __init__(self, name, colour, image=None, image_rect=None):
        self.name = name
        self.colour = colour
        self.image = image
        self.display_images()
        self.image_rect = image_rect

    def display_images(self):
        self.image = os.path.join(f"Piece Images/{self.colour} {self.name}.png")

class Pawn(Piece):
    def __init__(self, colour):
        #Using inheritance so I don't have to write all the code in the __init__ method for each piece.
        super().__init__('Pawn', colour)

    def get_pawn_valid_moves(self, board, row, column):
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
            new_column = column + col
            
            #Checks if the diagonal capture squares are within bounds of the board
            if 1 <= new_column <= 8 and row < 7:
                square = board[row + direction][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                #Only makes it a valid move if there is a piece at the potential diagonal capture square and the piece there is not
                # the same colour as the pawn 
                if piece is not None and piece.colour != piece2.colour:
                    moves.append((row + direction, new_column))
                
        return moves
    
    def get_control_moves(self, board, row, column):
        moves = []

        if board[row][column].piece.colour == 'White':
            direction = -1 #White moves up
        else:
            direction = 1 #Black moves down

        for col in [-1, 1]:
            new_column = column + col
            
            #Checks if the diagonal capture squares are within bounds of the board
            if 1 <= new_column <= 8:
                square = board[row + direction][new_column]
                piece = square.piece
                #Checks if the square is empty or another piece of same colour is there so it can defend that piece from the king.
                if piece is None or (piece.colour == board[row][column].piece.colour):
                    moves.append((row + direction, new_column))
                
        return moves


class Bishop(Piece):
    def __init__(self, colour):
        super().__init__('Bishop', colour)

    def get_bishop_valid_moves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                else:
                    #It stops if it encounters a piece of the same colour
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    break
                else:
                    break  

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column + dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    break
                else:
                    break

        return moves
    
    def get_bishop_control_moves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square the same as the piece
                #in one of the valid squares so it can defend it from the king.
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
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
            new_row = row - dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column + dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        return moves
    
    def get_bishop_pin_moves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, new_column))
                #If it encounters a piece of opposite colour that is not a king it skips it
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                #If it encounters a king of opposite colour, it adds it to the moves list and stops
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    break
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break 

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column + dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        return moves

class Knight(Piece):
    def __init__(self, colour):
        super().__init__('Knight', colour)

    def get_knight_valid_moves(self, board, row, column):
        moves = []
        direction1 = 1
        direction2 = 2

        for col in [-1, 1]:
            new_column = column + col
            new_row = row - direction2

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None :
                    moves.append((new_row, new_column))
                #Checks if the piece in the valid square is not the same colour as the current piece
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
            
        for col in [-1, 1]:
            new_column = column + col
            new_row = row + direction2

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))

        for col in [-2, 2]:
            new_column = column + col
            new_row = row - direction1

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))

        for col in [-2, 2]:
            new_column = column + col
            new_row = row + direction1

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
        
        return moves
    
    def get_knight_control_moves(self, board, row, column):
        moves = []
        direction1 = 1
        direction2 = 2

        for col in [-1, 1]:
            new_column = column + col
            new_row = row - direction2

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None :
                    moves.append((new_row, new_column))
                #Defending its own piece so king cant capture
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
            
        for col in [-1, 1]:
            new_column = column + col
            new_row = row + direction2

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))

        for col in [-2, 2]:
            new_column = column + col
            new_row = row - direction1

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))

        for col in [-2, 2]:
            new_column = column + col
            new_row = row + direction1

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
        
        return moves
   
class Rook(Piece):
    def __init__(self, colour):
        super().__init__('Rook', colour)

    def get_rook_valid_moves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour:
                    moves.append((new_row, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                else:
                    #It stops if it encounters a piece of the same colour
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            new_row = row - dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, column))
                    break
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((row, new_column))
                    break
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            new_column = column - dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((row, new_column))
                    break
                else:
                    break

        return moves
    
    def get_rook_control_moves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, column))
                #Checks if piece in valid square is same colour so it can defend it.
                elif piece2.colour == piece.colour:
                    moves.append((new_row, column))
                    #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                    break
                #If it encounters a king, it skips and adds the squares behind it.
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            new_row = row - dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            new_column = column - dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        return moves
    
    def get_rook_pin_moves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            new_row = row - dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break 

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            new_column = column - dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        return moves

class Queen(Piece):
    def __init__(self, colour):
        super().__init__('Queen', colour)

    def get_queen_valid_moves(self, board, row, column):
        moves = []

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, column))
                    break
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            new_row = row - dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, column))
                    break
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((row, new_column))
                    break
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            new_column = column - dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((row, new_column))
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                #Checks if the square is not occupied or the piece at that square is of a different colour to allow captures
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    break
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    break
                else:
                    break  

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column + dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))
                    break
                else:
                    break
       
        return moves
    
    def get_queen_control_moves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square the same as the piece
                #in one of the valid squares to defend it.
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the same colour, it stops so no more moves are added along that direction
                    break
                #If it encounters a king, it skips it and adds the squares behind it
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column + dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((new_row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, column))
                #Checks if piece in valid square is same colour so it can defend it.
                elif piece2.colour == piece.colour:
                    moves.append((new_row, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            new_row = row - dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            new_column = column - dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((row, new_column))
                    #If it encounters a piece of the opposite colour, it stops so no more moves are added along that direction
                    break
                elif piece.name == 'King' and piece2.colour != piece.colour:
                    continue
                else:
                    break

        return moves
    
    def get_queen_pin_moves(self, board, row, column):
        moves = []

        #Responsible for diagonal moves in the bottom right direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column + dir

            #Checks to see if the new row and column to move to is within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break
                
        #Responsible for diagonal moves in the top left direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        #Responsible for diagonal moves in the bottom left direction
        for dir in range(1, 8):
            new_row = row + dir
            new_column = column - dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for diagonal moves in the top right direction
        for dir in range(1, 8):
            new_row = row - dir
            new_column = column + dir

            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break

        #Responsible for vertical moves downwards
        for dir in range(1, 8):
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                #Checks if the square is empty
                if piece is None:
                    moves.append((new_row, column))
                #Checks if the colour of the piece at the current square is not the same as the piece
                #in one of the valid squares.
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for vertical moves upwards
        for dir in range(1, 8):
            new_row = row - dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((new_row, column))
                    #It stops if it encounters a piece of the same colour
                    break
                else:
                    break 

        #Responsible for horizontal moves to the right
        for dir in range(1, 8):
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        #Responsible for horizontal moves to the left
        for dir in range(1, 8):
            new_column = column - dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece
                if piece is None:
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour and piece.name != 'King':
                    continue
                elif piece2.colour != piece.colour and piece.name == 'King':
                    moves.append((row, new_column))
                    #It stops if it encounters a piece of the same colour
                    break 
                else:
                    break

        return moves

class King(Piece):
    def __init__(self, colour):
        super().__init__('King', colour)

    def get_king_valid_moves(self, board, row, column):
        moves = []
        direction = 1
        
        #Responsible for movement in the top left and bottom right directions
        for dir in [-1, 1]:
            new_row = row + dir
            new_column = column + dir
        
            #Checks if the new row and new column are within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                #Checks if the square it's moving to is empty
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the piece at the square it's moving to is of a different colour and not a king
                elif piece2.colour != piece.colour:
                    moves.append((new_row, new_column))

        #Responsible for movement in the horizontal left and right directions
        for dir in [-1, 1]:
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None: 
                    moves.append((row, new_column))
                elif piece2.colour != piece.colour:
                    moves.append((row, new_column))

        #Responsible for movement in the vertical top and bottom directions
        for dir in [-1, 1]:
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour != piece.colour:
                    moves.append((new_row, column))

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
    
    def get_king_control_moves(self, board, row, column):
        moves = []
        direction = 1
        
        #Responsible for movement in the top left and bottom right directions
        for dir in [-1, 1]:
            new_row = row + dir
            new_column = column + dir
        
            #Checks if the new row and new column are within the bounds of the board
            if 0 <= new_row <= 7 and 1 <= new_column <= 8:
                square = board[new_row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                #Checks if the square it's moving to is empty
                if piece is None:
                    moves.append((new_row, new_column))
                #Checks if the piece at the square is the same colour so it can defend it.
                elif piece2.colour == piece.colour:
                    moves.append((new_row, new_column))

        #Responsible for movement in the horizontal left and right directions
        for dir in [-1, 1]:
            new_column = column + dir

            if 1 <= new_column <= 8:
                square = board[row][new_column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None: 
                    moves.append((row, new_column))
                elif piece2.colour == piece.colour:
                    moves.append((row, new_column))

        #Responsible for movement in the vertical top and bottom directions
        for dir in [-1, 1]:
            new_row = row + dir

            if 0 <= new_row <= 7:
                square = board[new_row][column]
                piece = square.piece
                piece2 = board[row][column].piece

                if piece is None:
                    moves.append((new_row, column))
                elif piece2.colour == piece.colour:
                    moves.append((new_row, column))

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
    
    def get_kingside_castle_moves(self, board, row, column):
        moves = []
        #Checks if it's black or white by checking the row
        if (row == 7 or row == 0) and column == 5:
            #Checks if the squares between the king and the rook on the right are empty
            if board[row][column + 1].piece is None and board[row][column + 2].piece is None:
                moves.append((row, column + 2))

        return moves
    
    def get_queenside_castle_moves(self, board, row, column):
        moves = []
        #Checks if it's black or white by checking the row
        if (row == 7 or row == 0) and column == 5:
            #Checks if the three squares between the king and rook on the left are empty
            if board[row][column - 1].piece is None and board[row][column - 2].piece is None and board[row][column - 3].piece is None:
                moves.append((row, column - 2))

        return moves
    
    #def check_kingside_castle_moves(self, board, row, column):
        #moves = []
        #Checks if it's black or white by checking the row
        #if (row == 7 or row == 0) and column == 5:
            #Checks if the squares between the king and the rook on the right are empty
            #if board[row][column + 1].piece is None and board[row][column + 2].piece is None:
                #moves.append((row, column + 2))

        #return moves
    
    #def check_queenside_castle_moves(self, board, row, column):
        #moves = []
        #Checks if it's black or white by checking the row
        #if (row == 7 or row == 0) and column == 5:
            #Checks if the three squares between the king and rook on the left are empty
            #if board[row][column - 1].piece is None and board[row][column - 2].piece is None and board[row][column - 3].piece is None:
                #moves.append((row, column - 2))

        #return moves

    
    




        
        

        



        

        

        



