from copy import deepcopy
import random
from.BotManager import AIGame

aiGame = AIGame()

def Minimax(position, depth, maxPlayer, game, alpha, beta):

    if depth == 0 or game.Checkmate('White') or game.Checkmate('Black') or game.Stalemate():
        return aiGame.MaterialEvaluation(position), position
  
    if maxPlayer:
        maxEval = float('-inf')
        bestMove = None
        for move in AllMoves(position, 'White', game):
            evaluation = Minimax(move, depth - 1, False, game, alpha, beta)[0]
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
            evaluation = Minimax(move, depth - 1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            if evaluation == minEval:
                bestMove = move
            beta = min(beta, minEval)
            if beta <= alpha:
                break  

        return minEval, bestMove
        
def EasyMode(position, game):
    moves = AllMoves(position, 'Black', game) # Stores the new board with the new move

    # Checks if it's valid
    if moves:
        return random.choice(moves) # Returns the first new board state encountererd
    
def MediumMode(position, game):
    evaluations = []
    moves = AllMoves(position, 'Black', game)
    for move in moves:
        evaluations.append(aiGame.MediumEvaluation(move))
    
    for positions in moves:
        if aiGame.MediumEvaluation(positions) == max(evaluations):
            return positions
        
def HardMode(position, game):
    evaluations = []
    moves = AllMoves(position, 'Black', game)
    for move in moves:
        evaluations.append(aiGame.MediumEvaluation(move))
    
    for positions in moves:
        if aiGame.MediumEvaluation(positions) == max(evaluations):
            return positions
        
def PlayMove(square, move, board):
    # Checks if the selected piece to move is a King and kingside castling is attempted
    if square.piece != None and square.piece.name == 'King' and move == (0, 7) and board.CanCastleKingside('Black'):
        board.CastleKingside('Black')

    # Checks if the selected piece to move is a King and queenside castling is attempted
    elif square.piece != None and square.piece.name == 'King' and move == (0, 3) and board.CanCastleQueenside('Black'):
        board.CastleQueenside('Black')

    # Handles regular piece movement
    else:
        board.MovePiece(square, move[0], move[1])

    return board

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
                tempSquare = tempBoard.GetPieceSquare(row, column)
                newBoard = PlayMove(tempSquare, moves, tempBoard)
                boardMoves.append(newBoard)

    return boardMoves

def LMode(position, game):
    evaluations = []
    playedPositions = []
    moves = AllMoves(position, 'Black', game)
    for move in moves:
        eval = aiGame.MediumEvaluation(move)
        if len(playedPositions) > 0:
            previousPosition = playedPositions[-1]
            if aiGame.MaterialEvaluation(move) < aiGame.MaterialEvaluation(previousPosition):
                evaluations.append(eval - Minimax(move, 3, False, game, float('-inf'), float('inf'))[0])
            else:
                evaluations.append(eval)
        else:
            evaluations.append(eval)
    
    for positions in moves:
        if aiGame.MediumEvaluation(positions) == max(evaluations):
            playedPositions.append(positions)
            return positions
    


