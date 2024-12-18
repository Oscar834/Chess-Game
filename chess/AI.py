from copy import deepcopy
import random

def Minimax(position, depth, maxPlayer, game, difficulty):
    #if depth == 0 or game.Checkmate(maxPlayer) or game.Stalemate():
        #return position.evaluate(), position
    if difficulty == 'Easy':
        if maxPlayer:
            move = AllMoves(position, game.turn, game)

            if move:
                return move[0]

def SimulateMove(piece, move, board):
    if piece.piece.name == 'King' and move == (0, 7) and board.CanCastleKingside('Black'):
        board.CastleKingside('Black')

    elif piece.piece.name == 'King' and move == (0, 3) and board.CanCastleQueenside('Black'):
        board.CastleQueenside('Black')

    else:
        board.MovePiece(piece, move[0], move[1])

    return board

def NumsList(game, piece):
    piecesNum = []

    pieceCount = game.PlayerPieces('Black').count(piece)
    
    for i in range(pieceCount, 0, -1):
        piecesNum.append(i)

    return piecesNum[::-1]

def AllMoves(board, colour, game):
    moves = []
    pieces = game.PlayerPieces(colour)

    chosenPiece = random.choice(pieces)
    validMoves = game.PieceMoves(chosenPiece, colour)
    key = random.choice(NumsList(game, chosenPiece))
    pos = game.FriendlyPiecePosition(chosenPiece).get(key)

    # Re-select a piece if all valid moves are empty
    if not game.Checkmate(colour):
        while validMoves.get(key) == []:
            chosenPiece = random.choice(pieces)
            validMoves = game.PieceMoves(chosenPiece, colour)
            key = random.choice(NumsList(game, chosenPiece))
            pos = game.FriendlyPiecePosition(chosenPiece).get(key)

    move = validMoves.get(key)
    tempBoard = deepcopy(board)
    row, column = pos
    tempPiece = tempBoard.PieceBoardIndex(row, column)
    newMove = random.choice(move)
    newBoard = SimulateMove(tempPiece, newMove, tempBoard)
    if newBoard:
        moves.append(newBoard)

    return moves
