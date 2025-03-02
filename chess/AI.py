from copy import deepcopy
import random
from .BotManager import AIGame

aiGame = AIGame() # Holds an instance of the AIGame class
def EasyMode(position, game):
    moves = AllMoves(position, 'Black', game) # Holds all the possible board states and the move associated with that board state

    # Checks if the moves list is not empty
    if moves != []:
        boardChoice = random.choice(moves) # Picks a random one from the moves list
        
        # Checks the key and value of the board choice
        for board, move in boardChoice.items():
            chosenBoard = board # Holds the board object
            playedMove = move # Holds the move played

        return chosenBoard, playedMove # Returns a tuple of the board object and the associated move played

def MediumMode(position, game):
    moves = AllMoves(position, 'Black', game) # Holds all the possible board states and the move associated with that board state
    bestChoice = None 
    bestEvaluation = float('-inf') # I set it to -infinity not +infinity because I want to keep track of the highest evaluation

    # Loops through all the board states in the moves list
    for boards in moves:
        # Checks the board object and associated move played of each board state
        for board, move in boards.items():
            evaluation = aiGame.MediumEvaluation(board) # Sets evaluation to hold the medium evalutation of the current board state

            # Checks if the current evaluation is better than the best evaluation
            if evaluation > bestEvaluation:
                bestEvaluation = evaluation # Reassigns the best evaluation so it now holds the current evaluation
                bestChoice = board # Sets the bestChoice to the board state
                playedMove = move # Sets played move to store the move associated with the best board state

    return bestChoice, playedMove # Returns a tuple holding the best board state and the associated move to reach that board state

def HardMode(position, game):
    moves = AllMoves(position, 'Black', game) # Holds all the possible board states and the move associated with that board state
    bestChoice = None
    bestEvaluation = float('-inf') # I set it to -infinity and not +infinity becuase I want to keep track of the highest evaluation

    # Loops through all the board states in the moves list
    for boards in moves:
        # Checks the board object and associated move played of each board state
        for board, move in boards.items():
            lost = False  # Resets the lost variable for each board state
            whiteMoves = CheckMoves(board, 'White') # Stores all board states that white plays to result in a check to the black king
            
            # Loops through all check board states white can play
            for whiteMove in whiteMoves:
                # Checks if that move will result in the black king getting checkmated
                if aiGame.Checkmate(whiteMove, 'Black'):
                    lost = True # Sets lost to true if so
                    worstChoice = board # Sets worstMove to current board state if so
                    worstMove = move
                    break  # It stops checking because it has already found the losing move

            # Checks if the position after white makes a move would not result in a checkmate
            if not lost:
                evaluation = aiGame.HardEvaluation(board) # Stores the hard evaluation of the current board state
                
                # Checks if the current evaluation is better than the best evaluation
                if evaluation > bestEvaluation:
                    bestEvaluation = evaluation # Reassigns best evaluation so it now stores the current one
                    bestChoice = board # Holds the board state with the highest evaluation
                    playedMove = move # Holds the move associated with the best board state

            # Checks if no moves have been registered because all of them lead to checkmate anyways
            if bestChoice == None:
                bestChoice = worstChoice # Allows it to play any move
                playedMove = worstMove

    return bestChoice, playedMove # Returns a tuple holding the best board state and the associated move to reach that board state
        
def PlayMove(square, move, board, game):
    # Checks if the piece to move is a King and kingside castling is attempted
    if square.piece != None and square.piece.name == 'King' and move == (0, 7) and board.CanCastleKingside('Black'):
        board.CastleKingside('Black') # Performs the kingside castling movement

    # Checks if the piece to move is a King and queenside castling is attempted
    elif square.piece != None and square.piece.name == 'King' and move == (0, 3) and board.CanCastleQueenside('Black'):
        board.CastleQueenside('Black') # Performs the queenside castling movement

    # Checks if the piece to move is a pawn and the promotion square was moved to
    elif square.piece != None and square.piece.name == 'Pawn' and move[0] == 7:
        board.Promote(move[0], move[1], 'Black') # Promotes the pawn to a queen using the promote method in the board class
        square.piece = None # Removes the pawn that just queened

    # Checks if the piece to move is a pawn the enPassant move was attempted
    elif square.piece != None and square.piece.name == 'Pawn' and game.EnPassantPossible and move in game.EnPassantMove:
        board.EnPassant(square, move[0], move[1], 'Black') # Uses the board method EnPassant to perform the enPassant movement

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
        enemyPiecePositions = game.AllPiecePositions('White') # Stores the positions of all enemy pieces

        # Loops through each key and value (list) in the valid moves dict.
        for num, moves in validMoves.items():
            # Loops through all moves inside the value(list)
            for move in moves:
                position = game.PiecePositions(piece, colour).get(num) # Uses the key to get the current position of the piece
                # Checks if the piece exists to prevent the game from crashing
                if position != None:
                    row, column = position
                    tempBoard = deepcopy(board) # Creates a copy of the current board
                    tempSquare = tempBoard.GetPieceSquare(row, column) # Gets the square the current piece is on
                    newBoard = PlayMove(tempSquare, move, tempBoard, game) # Uses the Play Move function to simulate the piece moving on the copied board
                    
                    # This checks if the move to be made would be a capture
                    if move in enemyPiecePositions:
                        # Adds a dictionary holding the newBoard object as the key and the move it played to achieve that position as the value
                        # The value type for the move is a list to indicate a capture
                        boardStates.append({newBoard: {piece.lower(): [move[0], move[1]]}})
                    else:
                        # The value type for the move is a tuple to indicate a normal non-capture move
                        boardStates.append({newBoard: {piece.lower(): (move[0], move[1])}})

    return boardStates

# This method stores all moves that could result in the black king being in check
def CheckMoves(board, colour):
    boardMoves = []

    for piece in ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
        validMoves = aiGame.PieceMoves(board, piece, colour) # Stores the dictionary which holds the valid moves of all the pieces

        # Loops through each key and value in valid moves dictionary
        for num, moves in validMoves.items():
            # Loops through the moves inside each list 
            for move in moves:
                position = aiGame.PiecePositions(board, piece, colour).get(num) # Uses the key to get the current position of the piece
                # Checks if the piece exists
                if position != None:
                    row, column = position
                    tempBoard = deepcopy(board) # Creates a copy of the board object it is passed
                    tempSquare = tempBoard.GetPieceSquare(row, column) # Gets the square the current piece is on
                    newBoard = PlayMove(tempSquare, move, tempBoard, aiGame)  # Uses the Play Move function to simulate the piece moving on the copied board

                    # Checks if in the new board state, the black king is in check
                    if aiGame.InCheck(newBoard, 'Black') != None:
                        boardMoves.append(newBoard) # Adds the board state

    return boardMoves


