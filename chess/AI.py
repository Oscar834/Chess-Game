from copy import deepcopy
import random
import math

def Minimax(position, depth, maxPlayer, game, difficulty, alpha, beta):

    if difficulty == 'Medium' and depth == 0 or game.Checkmate('White') or game.Checkmate('Black') or game.Stalemate():
        return position.Evaluate(), position

    # Checks if the selected difficulty was Easy
    if difficulty == 'Easy':
        move = MoveChoice(position, 'Black', game) # Stores the new board with the new move

        # Checks if it's valid
        if move:
            return move[0] # Returns the first new board state encountererd
    
    elif difficulty == 'Hard':
        evaluations = []
        moves = AllMoves(position, 'Black', game)
        for move in moves:
            evaluations.append(position.HardEvaluation(game))
        maxEvaluation = max(evaluations)
        index = evaluations.index(maxEvaluation)

        return moves[index]
  
    elif difficulty == 'Medium':
        if maxPlayer:
            maxEval = float('-inf')
            bestMove = None
            for move in AllMoves(position, 'White', game):
                evaluation = Minimax(move, depth - 1, False, game, difficulty, alpha, beta)[0]
                maxEval = max(maxEval, evaluation)
                if evaluation == maxEval:
                    bestMove = move
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break

            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            for move in AllMoves(position, 'Black', game):
                evaluation = Minimax(move, depth - 1, True, game, difficulty, alpha, beta)[0]
                minEval = min(minEval, evaluation)
                if evaluation == minEval:
                    bestMove = move
                beta = min(beta, minEval)
                if beta <= alpha:
                    break  

            return minEval, bestMove
        
    
        
def PlayMove(piece, move, board):
    # Checks if the selected piece to move is a King and kingside castling is attempted
    if piece.piece != None and piece.piece.name == 'King' and move == (0, 7) and board.CanCastleKingside('Black'):
        board.CastleKingside('Black')

    # Checks if the selected piece to move is a King and queenside castling is attempted
    elif piece.piece != None and piece.piece.name == 'King' and move == (0, 3) and board.CanCastleQueenside('Black'):
        board.CastleQueenside('Black')

    # Handles regular piece movement
    else:
        board.MovePiece(piece, move[0], move[1])

    return board

def PieceList(game, piece):
    piecesNum = []

    # Gets the count of a chosen black piece
    pieceCount = game.PlayerPieces('Black').count(piece)
    
    # Adds the numbers from the pieceCount to 1 to the piecesNum list.
    for i in range(pieceCount, 0, -1):
        piecesNum.append(i)

    return piecesNum[::-1] # Reverts the direction of the list so if it was [3, 2, 1] it becomes [1, 2, 3]

def MoveChoice(board, colour, game):
    moves = []
    pieces = game.PlayerPieces(colour) 

    chosenPiece = random.choice(pieces) 
    validMoves = game.PieceMoves(chosenPiece, colour)
    key = random.choice(PieceList(game, chosenPiece)) 
    pos = game.FriendlyPiecePosition(chosenPiece).get(key) 

    if not game.Checkmate(colour):
        # Reselects another piece if the previous selected piece had no moves
        while validMoves.get(key) == []:
            chosenPiece = random.choice(pieces)
            validMoves = game.PieceMoves(chosenPiece, colour)
            key = random.choice(PieceList(game, chosenPiece))
            pos = game.FriendlyPiecePosition(chosenPiece).get(key)

    move = validMoves.get(key) # Stores the valid move for the selected piece
    tempBoard = deepcopy(board) # Copies the current board state
    row, column = pos 
    pieceSquare = tempBoard.GetPiece(row, column) 
    newMove = random.choice(move)
    newBoard = PlayMove(pieceSquare, newMove, tempBoard) 
    if newBoard:
        moves.append(newBoard) 

    return moves

def AllMoves(board, colour, game):
    boardMoves = []

    for piece in ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
        validMoves = game.PieceMoves(piece, colour)

        for num, move in validMoves.items():
            for moves in move:
                position = game.PiecePositions(piece, colour).get(num)
                if position != None:
                    row, column = position
                tempBoard = deepcopy(board)
                tempPiece = tempBoard.GetPiece(row, column)
                newBoard = PlayMove(tempPiece, moves, tempBoard)
                boardMoves.append(newBoard)

    return boardMoves


    


