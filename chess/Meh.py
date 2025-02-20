from copy import deepcopy
import random
        
def EasyMode(position, game):
    moves = AllMoves(position, 'Black', game) # Holds all the new possible board states (moves played)

    # Checks if the moves list is not empty
    if moves != []:
        return random.choice(moves) # Returns a random board state 
        
def PlayMove(square, move, board):
    # Checks if the piece to move is a King and kingside castling is attempted
    if square.piece != None and square.piece.name == 'King' and move == (0, 7) and board.CanCastleKingside('Black'):
        board.CastleKingside('Black') # Performs the kingside castling movement

    # Checks if the piece to move is a King and queenside castling is attempted
    elif square.piece != None and square.piece.name == 'King' and move == (0, 3) and board.CanCastleQueenside('Black'):
        board.CastleQueenside('Black') # Performs the queenside castling movement

    # Handles regular piece movement
    else:
        board.MovePiece(square, move[0], move[1])

    return board # Returns the board object

def AllMoves(board, colour, game):
    boardStates = []

    # This ensures all the valid moves of every piece is checked
    for piece in ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
        # Gets the dictionary which stores the valid moves of all pieces using the new method from the game class
        validMoves = game.PieceMoves(piece, colour)

        # Loops through each key and value (list) in the valid moves dict.
        for num, moves in validMoves.items():
            # Loops through all moves inside the value(list)
            for move in moves:
                position = game.PiecePositions(piece, colour).get(num) # Uses the key to get the current position of the piece
                # Checks if the piece exists
                if position != None:
                    row, column = position
                tempBoard = deepcopy(board) # Creates a copy of the current board
                tempSquare = tempBoard.GetPieceSquare(row, column) # Gets the square the current piece is on
                newBoard = PlayMove(tempSquare, move, tempBoard) # Uses the Play Move function to simulate the piece moving on the copied board
                boardStates.append(newBoard) # Adds the new board to the board states list

    return boardStates