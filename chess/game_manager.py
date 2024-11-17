import pygame
from .constants import SQUARE_HEIGHT, SQUARE_WIDTH, LGREY, BLACK, WHITE, GREEN
from .board import Board
from .pieces import *

class Game:
    def __init__(self, screen):
        self.board = Board()
        self.pawn = Pawn(Piece)
        self.bishop = Bishop(Piece)
        self.knight = Knight(Piece)
        self.rook = Rook(Piece)
        self.queen = Queen(Piece)
        self.king = King(Piece)
        self.square_selected = None
        self.turn = 'White'
        self.valid_piece_moves = []
        self.kingside_castle_moves = []
        self.queenside_castle_moves = []
        self.screen = screen

    def update_screen(self):
        self.board.draw_board(self.screen)
        self.board.display_BoardnPieces(self.screen)
        #self.winner(self.screen)
        #Promotion is called here for white and for black for visual display
        self.board.promotion('White', self.screen)
        self.board.promotion('Black', self.screen)
        self.draw_all_valid_moves(self.valid_piece_moves)

    def select_square(self, row, column):
        #checks if a square is selected
        if self.square_selected:
            final_square = self.move(row, column)
            if not final_square:
                #If the square they tried to move to is not valid, reset the valid moves, and allow them to select a piece again
                self.valid_piece_moves= []
                self.square_selected = None
                self.select_square(row, column)

        piece = self.board.get_piece_at_square(row, column)
        piece_square = self.board.get_piece_position(row, column)
        #All these hold the current row and column of the piece giving the check
        first_pawn_position = self.first_pawn_giving_check()
        second_pawn_position = self.second_pawn_giving_check()
        third_pawn_position = self.third_pawn_giving_check()
        fourth_pawn_position = self.fourth_pawn_giving_check()
        fifth_pawn_position = self.fifth_pawn_giving_check()
        sixth_pawn_position = self.sixth_pawn_giving_check()
        seventh_pawn_position = self.seventh_pawn_giving_check()
        eighth_pawn_position = self.eighth_pawn_giving_check()
        queen_position = self.queen_giving_check()
        dark_bishop_position = self.dark_bishop_giving_check()
        light_bishop_position = self.light_bishop_giving_check()
        first_knight_position = self.first_knight_giving_check()
        second_knight_position = self.second_knight_giving_check()
        first_rook_position = self.first_rook_giving_check()
        second_rook_position = self.second_rook_giving_check()

        #These hold the squares where a piece could go to block a check
        queen_block_moves = self.block_queen_check()
        first_rook_block_moves = self.block_first_rook_check()
        second_rook_block_moves = self.block_second_rook_check()
        light_bishop_block_moves = self.block_light_bishop_check()
        dark_bishop_block_moves = self.block_dark_bishop_check()

        #This list holds the positions of the pieces giving the check
        piece_positions = [
                    first_pawn_position, second_pawn_position, third_pawn_position,
                    fourth_pawn_position, fifth_pawn_position, sixth_pawn_position,
                    seventh_pawn_position, eighth_pawn_position, queen_position,
                    dark_bishop_position, light_bishop_position,
                    first_knight_position, second_knight_position,
                    first_rook_position, second_rook_position
                ]

        #This is a list which stores the list of the different block moves for either the bishop, queen or rook
        block_moves = [
                    light_bishop_block_moves, dark_bishop_block_moves,
                    first_rook_block_moves, second_rook_block_moves, queen_block_moves
                ]

        #Checks is the selected square is not empty and if it's a pawn
        if piece is not None and piece.name == 'Pawn' and piece.colour == self.turn:
            #Sets this variable to hold all its potential valid moves at its current position
            valid_moves = self.pawn.get_pawn_valid_moves(self.board.board, row, column)
            king_row, king_column = self.board.get_king_position(self.turn)
            first_rook_square = self.get_first_rook_position()
            second_rook_square = self.get_second_rook_position()
            queen_square = self.get_queen_position()
            light_bishop_square = self.get_light_bishop_position()
            dark_bishop_square = self.get_dark_bishop_position()

            if light_bishop_square is not None:
                light_bishop_row, light_bishop_column = light_bishop_square
                light_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column)
                light_bishop_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, light_bishop_row, light_bishop_column)
            else:
                light_bishop_moves = []

            if dark_bishop_square is not None:
                dark_bishop_row, dark_bishop_column = dark_bishop_square
                dark_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column)
                dark_bishop_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, dark_bishop_row, dark_bishop_column)
            else:
                dark_bishop_moves = []

            if queen_square is not None:
                queen_row, queen_column = queen_square
                queen_moves = self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column)
                queen_pin_moves = self.queen.get_queen_pin_moves(self.board.board, queen_row, queen_column)
            else:
                queen_moves = []

            if first_rook_square is not None:
                first_rook_row, first_rook_column = first_rook_square
                first_rook_moves = self.rook.get_rook_valid_moves(self.board.board, first_rook_row, first_rook_column)
                first_rook_pin_moves = self.rook.get_rook_pin_moves(self.board.board, first_rook_row, first_rook_column)
            else:
                first_rook_moves = []

            if second_rook_square is not None:
                second_rook_row, second_rook_column = second_rook_square
                second_rook_moves = self.rook.get_rook_valid_moves(self.board.board, second_rook_row, second_rook_column)
                second_rook_pin_moves = self.rook.get_rook_pin_moves(self.board.board, second_rook_row, second_rook_column)
            else:
                second_rook_moves = []

            if self.piece_pinned('Pawn', 1) and (row, column) == self.board.get_first_pawn_position(self.turn)\
            and (row, column) in first_rook_moves and (king_row, king_column) in first_rook_pin_moves and column == first_rook_column:
                for move in first_rook_moves:
                    if move in valid_moves and move[1] == column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
            
            #Checks if the king is not in check and makes the valid piece moves all its potential valid moves
            elif not self.in_check():
                self.square_selected = piece_square
                self.valid_piece_moves = valid_moves

            #Checks if the king is in check
            else:
                for position in piece_positions:
                    #Checks if the position of the piece giving the check is in one of the potential valid moves
                    #and if it is, it makes the position the only valid position so the piece giving the check can be captured.
                    if position in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves = [position]
                    
                #Loops through the block moves in the block moves list
                for moves in block_moves:
                    #This loops through each move in the each list in the block moves list
                    for move in moves:
                        #Checks if any of those moves are potential valid moves for the pawn and if they are it adds them to the valid piece moves list.
                        if move in valid_moves:
                            self.square_selected = piece_square
                            self.valid_piece_moves.append(move)

        elif piece is not None and piece.name == 'Bishop' and piece.colour == self.turn:
            valid_moves = self.bishop.get_bishop_valid_moves(self.board.board, row, column)
            king_row, king_column = self.board.get_king_position(self.turn)
            light_bishop_square = self.get_light_bishop_position()
            dark_bishop_square = self.get_dark_bishop_position()
            queen_square = self.get_queen_position()
            if queen_square is not None:
                queen_row, queen_column = queen_square
                queen_moves = self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column)
                queen_pin_moves = self.queen.get_queen_pin_moves(self.board.board, queen_row, queen_column)
            else:
                queen_moves = []

            if light_bishop_square is not None:
                light_bishop_row, light_bishop_column = light_bishop_square
                light_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column)
                light_bishop_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, light_bishop_row, light_bishop_column)
            else:
                light_bishop_moves = []

            if dark_bishop_square is not None:
                dark_bishop_row, dark_bishop_column = dark_bishop_square
                dark_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column)
                dark_bishop_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, dark_bishop_row, dark_bishop_column)
            else:
                dark_bishop_moves = []

            if self.piece_pinned('Bishop', 'Light') and self.in_check() and (row, column) == self.board.get_light_bishop_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []

            elif self.piece_pinned('Bishop', 'Dark') and self.in_check() and (row, column) == self.board.get_dark_bishop_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []

            elif self.piece_pinned('Bishop', 'Light') and (row, column) == self.board.get_light_bishop_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves\
            and ((king_row < queen_row and king_column > queen_column) or (king_row > queen_row and king_column < queen_column)):
                for move in queen_pin_moves:
                    if move in valid_moves and (move[0] + move[1] == row + column):
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)

            elif self.piece_pinned('Bishop', 'Light') and (row, column) == self.board.get_light_bishop_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves\
            and ((king_row > queen_row and king_column > queen_column) or (king_row < queen_row and king_column < queen_column)):
                for move in queen_pin_moves:
                    if move in valid_moves and ((move[0] + move[1]) - (row + column)) != 0 and ((move[0] + move[1]) - (row + column)) % 2 == 0:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)

            elif self.piece_pinned('Bishop', 'Light') and (row, column) == self.board.get_light_bishop_position(self.turn)\
            and (row, column) in light_bishop_moves and (king_row, king_column) in light_bishop_pin_moves:
                for move in light_bishop_pin_moves:
                    if move in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(light_bishop_square)

            elif self.piece_pinned('Bishop', 'Dark') and (row, column) == self.board.get_dark_bishop_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves\
            and ((king_row < queen_row and king_column > queen_column) or (king_row > queen_row and king_column < queen_column)):
                for move in queen_pin_moves:
                    if move in valid_moves and (move[0] + move[1] == row + column):
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)

            elif self.piece_pinned('Bishop', 'Dark') and (row, column) == self.board.get_dark_bishop_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves\
            and ((king_row > queen_row and king_column > queen_column) or (king_row < queen_row and king_column < queen_column)):
                for move in queen_pin_moves:
                    if move in valid_moves and ((move[0] + move[1]) - (row + column)) != 0 and ((move[0] + move[1]) - (row + column)) % 2 == 0:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)

            elif self.piece_pinned('Bishop', 'Dark') and (row, column) == self.board.get_dark_bishop_position(self.turn)\
            and (row, column) in dark_bishop_moves and (king_row, king_column) in dark_bishop_pin_moves:
                for move in dark_bishop_pin_moves:
                    if move in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(dark_bishop_square)

            elif self.piece_pinned('Bishop', 'Light') and (row, column) == self.board.get_light_bishop_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []

            elif self.piece_pinned('Bishop', 'Dark') and (row, column) == self.board.get_dark_bishop_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []
                
            elif not self.in_check():
                self.square_selected = piece_square
                self.valid_piece_moves = valid_moves
            else:
                for position in piece_positions:
                    if position in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves = [position]
                    
                for moves in block_moves:
                    for move in moves:
                        if move in valid_moves:
                            self.square_selected = piece_square
                            self.valid_piece_moves.append(move)
                    
        elif piece is not None and piece.name == 'Knight' and piece.colour == self.turn:
            valid_moves = self.knight.get_knight_valid_moves(self.board.board, row, column)

            #Checks if the pinned knight is the first knight and removes all its moves if its pinned
            if self.piece_pinned('Knight', 1) and (row, column) == self.board.get_first_knight_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []
            #Checks if the pinned knight is the second knight and removes all its moves if its pinned
            elif self.piece_pinned('Knight', 2) and (row, column) == self.board.get_second_knight_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []
            
            #Checks if the king is not in check
            elif not self.in_check():
                self.square_selected = piece_square
                self.valid_piece_moves = valid_moves

            #Checks if the king is in check
            elif self.in_check():
                for position in piece_positions:
                    if position in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves = [position]
                    
                for moves in block_moves:
                    for move in moves:
                        if move in valid_moves:
                            self.square_selected = piece_square
                            self.valid_piece_moves.append(move)
        
        elif piece is not None and piece.name == 'Rook' and piece.colour == self.turn:
            valid_moves = self.rook.get_rook_valid_moves(self.board.board, row, column)
            king_row, king_column = self.board.get_king_position(self.turn)
            first_rook_square = self.get_first_rook_position()
            second_rook_square = self.get_second_rook_position()
            queen_square = self.get_queen_position()
            if queen_square is not None:
                queen_row, queen_column = queen_square
                queen_moves = self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column)
                queen_pin_moves = self.queen.get_queen_pin_moves(self.board.board, queen_row, queen_column)
            else:
                queen_moves = []

            if first_rook_square is not None:
                first_rook_row, first_rook_column = first_rook_square
                first_rook_moves = self.rook.get_rook_valid_moves(self.board.board, first_rook_row, first_rook_column)
                first_rook_pin_moves = self.rook.get_rook_pin_moves(self.board.board, first_rook_row, first_rook_column)
            else:
                first_rook_moves = []

            if second_rook_square is not None:
                second_rook_row, second_rook_column = second_rook_square
                second_rook_moves = self.rook.get_rook_valid_moves(self.board.board, second_rook_row, second_rook_column)
                second_rook_pin_moves = self.rook.get_rook_pin_moves(self.board.board, second_rook_row, second_rook_column)
            else:
                second_rook_moves = []

            if self.piece_pinned('Rook', 1) and self.in_check() and (row, column) == self.board.get_first_rook_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []

            elif self.piece_pinned('Rook', 2) and self.in_check() and (row, column) == self.board.get_second_rook_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []

            elif self.piece_pinned('Rook', 1) and (row, column) == self.board.get_first_rook_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves and row == queen_row:
                for move in queen_pin_moves:
                    if move in valid_moves and move[0] == row:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)

            elif self.piece_pinned('Rook', 1) and (row, column) == self.board.get_first_rook_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves and column == queen_column:
                for move in queen_pin_moves:
                    if move in valid_moves and move[1] == column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)
                      
            elif self.piece_pinned('Rook', 1) and (row, column) == self.board.get_first_rook_position(self.turn)\
            and (row, column) in first_rook_moves and (king_row, king_column) in first_rook_pin_moves:
                for move in first_rook_pin_moves:
                    if move in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(first_rook_square)

            elif self.piece_pinned('Rook', 1) and (row, column) == self.board.get_first_rook_position(self.turn)\
            and (row, column) in second_rook_moves and (king_row, king_column) in second_rook_pin_moves:
                for move in second_rook_pin_moves:
                    if move in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(second_rook_square)

            elif self.piece_pinned('Rook', 2) and (row, column) == self.board.get_second_rook_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves and row == queen_row:
                for move in queen_pin_moves:
                    if move in valid_moves and move[0] == row:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)

            elif self.piece_pinned('Rook', 2) and (row, column) == self.board.get_second_rook_position(self.turn)\
            and (row, column) in queen_moves and (king_row, king_column) in queen_pin_moves and column == queen_column:
                for move in queen_pin_moves:
                    if move in valid_moves and move[1] == column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(queen_square)

            elif self.piece_pinned('Rook', 2) and (row, column) == self.board.get_second_rook_position(self.turn)\
            and (row, column) in first_rook_moves and (king_row, king_column) in first_rook_pin_moves:
                for move in first_rook_pin_moves:
                    if move in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(first_rook_square)

            elif self.piece_pinned('Rook', 2) and (row, column) == self.board.get_second_rook_position(self.turn)\
            and (row, column) in second_rook_moves and (king_row, king_column) in second_rook_pin_moves:
                for move in second_rook_pin_moves:
                    if move in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(second_rook_square)

            elif self.piece_pinned('Rook', 1) and (row, column) == self.board.get_first_rook_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []

            elif self.piece_pinned('Rook', 2) and (row, column) == self.board.get_second_rook_position(self.turn):
                self.square_selected = piece_square
                self.valid_piece_moves = []
            
            elif not self.in_check():
                self.square_selected = piece_square
                self.valid_piece_moves = valid_moves

            else:
                for position in piece_positions:
                    if position in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves = [position]
                    
                for moves in block_moves:
                    for move in moves:
                        if move in valid_moves:
                            self.square_selected = piece_square
                            self.valid_piece_moves.append(move)
        
        elif piece is not None and piece.name == 'Queen' and piece.colour == self.turn:
            valid_moves = self.queen.get_queen_valid_moves(self.board.board, row, column)
            king_row, king_column = self.board.get_king_position(self.turn)
            first_rook_square = self.get_first_rook_position()
            second_rook_square = self.get_second_rook_position()
            opp_queen_square = self.get_queen_position()
            light_bishop_square = self.get_light_bishop_position()
            dark_bishop_square = self.get_dark_bishop_position()

            if light_bishop_square is not None:
                light_bishop_row, light_bishop_column = light_bishop_square
                light_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column)
                light_bishop_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, light_bishop_row, light_bishop_column)
            else:
                light_bishop_moves = []

            if dark_bishop_square is not None:
                dark_bishop_row, dark_bishop_column = dark_bishop_square
                dark_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column)
                dark_bishop_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, dark_bishop_row, dark_bishop_column)
            else:
                dark_bishop_moves = []

            if opp_queen_square is not None:
                opp_queen_row, opp_queen_column = opp_queen_square
                opp_queen_moves = self.queen.get_queen_valid_moves(self.board.board, opp_queen_row, opp_queen_column)
                opp_queen_pin_moves = self.queen.get_queen_pin_moves(self.board.board, opp_queen_row, opp_queen_column)
            else:
                opp_queen_moves = []

            if first_rook_square is not None:
                first_rook_row, first_rook_column = first_rook_square
                first_rook_moves = self.rook.get_rook_valid_moves(self.board.board, first_rook_row, first_rook_column)
                first_rook_pin_moves = self.rook.get_rook_pin_moves(self.board.board, first_rook_row, first_rook_column)
            else:
                first_rook_moves = []

            if second_rook_square is not None:
                second_rook_row, second_rook_column = second_rook_square
                second_rook_moves = self.rook.get_rook_valid_moves(self.board.board, second_rook_row, second_rook_column)
                second_rook_pin_moves = self.rook.get_rook_pin_moves(self.board.board, second_rook_row, second_rook_column)
            else:
                second_rook_moves = []

            if self.piece_pinned('Queen', 1) and self.in_check():
                self.square_selected = piece_square
                self.valid_piece_moves = []

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in opp_queen_moves and (king_row, king_column) in opp_queen_pin_moves and row == opp_queen_row:
                for move in opp_queen_pin_moves:
                    if move in valid_moves and move[0] == row:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(opp_queen_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in opp_queen_moves and (king_row, king_column) in opp_queen_pin_moves and column == opp_queen_column:
                for move in opp_queen_pin_moves:
                    if move in valid_moves and move[1] == column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(opp_queen_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in opp_queen_moves and (king_row, king_column) in opp_queen_pin_moves\
            and ((king_row < opp_queen_row and king_column > opp_queen_column) or (king_row > opp_queen_row and king_column < opp_queen_column)):
                for move in opp_queen_pin_moves:
                    if move in valid_moves and (move[0] + move[1] == row + column):
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(opp_queen_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in opp_queen_moves and (king_row, king_column) in opp_queen_pin_moves\
            and ((king_row > opp_queen_row and king_column > opp_queen_column) or (king_row < opp_queen_row and king_column < opp_queen_column)):
                for move in opp_queen_pin_moves:
                    if move in valid_moves and move[0] != row and move[1] != column\
                        and (move[0] + move[1] != row + column):
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(opp_queen_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in first_rook_moves and (king_row, king_column) in first_rook_pin_moves and row == first_rook_row:
                for move in first_rook_pin_moves:
                    if move in valid_moves and move[0] == row:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(first_rook_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in first_rook_moves and (king_row, king_column) in first_rook_pin_moves and column == first_rook_column:
                for move in first_rook_pin_moves:
                    if move in valid_moves and move[1] == column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(first_rook_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in second_rook_moves and (king_row, king_column) in second_rook_pin_moves and row == second_rook_row:
                for move in second_rook_pin_moves:
                    if move in valid_moves and move[0] == row:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(second_rook_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in second_rook_moves and (king_row, king_column) in second_rook_pin_moves and column == second_rook_column:
                for move in second_rook_pin_moves:
                    if move in valid_moves and move[1] == column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(second_rook_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in light_bishop_moves and (king_row, king_column) in light_bishop_pin_moves\
            and ((king_row < light_bishop_row and king_column > light_bishop_column) or (king_row > light_bishop_row and king_column < light_bishop_column)):
                for move in light_bishop_pin_moves:
                    if move in valid_moves and (move[0] + move[1] == row + column):
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(light_bishop_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in light_bishop_moves and (king_row, king_column) in light_bishop_pin_moves\
            and ((king_row > light_bishop_row and king_column > light_bishop_column) or (king_row < light_bishop_row and king_column < light_bishop_column)):
                for move in light_bishop_pin_moves:
                    if move in valid_moves and move[0] != row and move[1] != column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(light_bishop_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in dark_bishop_moves and (king_row, king_column) in dark_bishop_pin_moves\
            and ((king_row < dark_bishop_row and king_column > dark_bishop_column) or (king_row > dark_bishop_row and king_column < dark_bishop_column)):
                for move in dark_bishop_pin_moves:
                    if move in valid_moves and (move[0] + move[1] == row + column):
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(dark_bishop_square)

            elif self.piece_pinned('Queen', 1) and (row, column) == self.board.get_queen_position(self.turn)\
            and (row, column) in dark_bishop_moves and (king_row, king_column) in dark_bishop_pin_moves\
            and ((king_row > dark_bishop_row and king_column > dark_bishop_column) or (king_row < dark_bishop_row and king_column < dark_bishop_column)):
                for move in dark_bishop_pin_moves:
                    if move in valid_moves and move[0] != row and move[1] != column:
                        self.square_selected = piece_square
                        self.valid_piece_moves.append(move)
                        self.valid_piece_moves.append(dark_bishop_square)
            
            elif not self.in_check():
                self.square_selected = piece_square
                self.valid_piece_moves = valid_moves

            else:
                for position in piece_positions:
                    if position in valid_moves:
                        self.square_selected = piece_square
                        self.valid_piece_moves = [position]
                    
                for moves in block_moves:
                    for move in moves:
                        if move in valid_moves:
                            self.square_selected = piece_square
                            self.valid_piece_moves.append(move)
        
        elif piece != None and piece.name == 'King' and piece.colour == self.turn:
            self.square_selected = piece_square
            kingside = 'kingside'
            queenside = 'queenside'
            #Set this variable to the new method (get_new_king_moves) so it accounts for the removal of moves.
            self.valid_piece_moves = self.get_new_king_moves(row, column)
            #Contains the castle_moves of each side
            self.kingside_castle_moves = self.get_new_king_moves(row, column, kingside)
            self.queenside_castle_moves = self.get_new_king_moves(row, column, queenside)
            #Checks if kingside castling is possible and ensures you can't castle through a controlled square or into a controlled square.
            if self.board.can_castle_kingside(self.turn)\
                and ((7, 6) in self.valid_piece_moves or (0, 6) in self.valid_piece_moves)\
                and ((7, 7) in self.kingside_castle_moves or (0, 7) in self.kingside_castle_moves)\
                and self.in_check() == False:
                result = self.king.get_kingside_castle_moves(self.board.board, row, column)
                #Adds the kingside castling move to the valid moves list
                self.valid_piece_moves.extend(result)
            #Checks if queenside castling is possible and ensures you can't castle through a controlled square or into a controlled square.
            if self.board.can_castle_queenside(self.turn)\
                and ((7, 4) in self.valid_piece_moves or (0, 4) in self.valid_piece_moves)\
                and ((7, 3) in self.queenside_castle_moves or (0, 3) in self.queenside_castle_moves)\
                and self.in_check() == False:
                result2 = self.king.get_queenside_castle_moves(self.board.board, row, column)
                #Adds the queenside castling move to the valid moves list
                self.valid_piece_moves.extend(result2)
            
    def move(self, row, column):
        #Checks if a square is selected and checks the row and column selected and
        #ensures it is in the valid moves of the king and also checks if kingside castling is possible
        if self.square_selected.piece is not None and self.square_selected.piece.name == 'King' and (row == 7 or row == 0)\
            and column == 7 and (row, column) in self.valid_piece_moves and self.board.can_castle_kingside(self.turn):
            #Performs kingside castling
            self.board.castle_kingside(self.turn)
            self.switch_turns()
        #Does the same checks as the first if statement but this time checks if queenside castling is possible
        elif self.square_selected.piece is not None and self.square_selected.piece.name == 'King' and (row == 7 or row == 0)\
            and column == 3 and (row, column) in self.valid_piece_moves and self.board.can_castle_queenside(self.turn):
            #Performs queenside castling
            self.board.castle_queenside(self.turn)
            self.switch_turns()
        #This is the if block responsible for every other move
        elif self.square_selected and (row, column) in self.valid_piece_moves:
            self.board.move_piece(self.square_selected, row, column)
            self.switch_turns()
            return True
        
        return False
        
    def draw_all_valid_moves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.screen, LGREY, (column * SQUARE_WIDTH + SQUARE_HEIGHT//2, row * SQUARE_HEIGHT + SQUARE_WIDTH//2), 14)
    
    def switch_turns(self):
        #resets the valid moves so the previous players valid moves
        #no longer appears on the screen
        self.valid_piece_moves = []
        #This 'if else' block is responsible for switching turns
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'

    def switch_timer(self):
        # Returns white if it's white's turn
        if self.turn == 'White':
            return 'White'
        elif self.turn == 'Black':
            return 'Black'


    def get_first_pawn_position(self):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_second_pawn_position(self):
        first_pawn = self.get_first_pawn_position()
        for row in range(0, 8):
            for column in range(1, 9):
                #Skips the first pawn
                if (row, column) == first_pawn:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_third_pawn_position(self):
        first_pawn = self.get_first_pawn_position()
        second_pawn = self.get_second_pawn_position()
        for row in range(0, 8):
            for column in range(1, 9):
                #Skips the first and second pawn
                if (row, column) == first_pawn or (row, column) == second_pawn:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_fourth_pawn_position(self):
        first_pawn = self.get_first_pawn_position()
        second_pawn = self.get_second_pawn_position()
        third_pawn = self.get_third_pawn_position()
        for row in range(0, 8):
            for column in range(1, 9):
                #Skips the first, second and third pawn and so on.. for the remaining methods
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_fifth_pawn_position(self):
        first_pawn = self.get_first_pawn_position()
        second_pawn = self.get_second_pawn_position()
        third_pawn = self.get_third_pawn_position()
        fourth_pawn = self.get_fourth_pawn_position()
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_sixth_pawn_position(self):
        first_pawn = self.get_first_pawn_position()
        second_pawn = self.get_second_pawn_position()
        third_pawn = self.get_third_pawn_position()
        fourth_pawn = self.get_fourth_pawn_position()
        fifth_pawn = self.get_fifth_pawn_position()
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn\
                or (row, column) == fifth_pawn:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_seventh_pawn_position(self):
        first_pawn = self.get_first_pawn_position()
        second_pawn = self.get_second_pawn_position()
        third_pawn = self.get_third_pawn_position()
        fourth_pawn = self.get_fourth_pawn_position()
        fifth_pawn = self.get_fifth_pawn_position()
        sixth_pawn = self.get_sixth_pawn_position()
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn\
                or (row, column) == fifth_pawn\
                or (row, column) == sixth_pawn:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_eighth_pawn_position(self):
        first_pawn = self.get_first_pawn_position()
        second_pawn = self.get_second_pawn_position()
        third_pawn = self.get_third_pawn_position()
        fourth_pawn = self.get_fourth_pawn_position()
        fifth_pawn = self.get_fifth_pawn_position()
        sixth_pawn = self.get_sixth_pawn_position()
        seventh_pawn = self.get_seventh_pawn_position()
        for row in range(0, 8):
            for column in range(1, 9):
                if (row, column) == first_pawn\
                or (row, column) == second_pawn\
                or (row, column) == third_pawn\
                or (row, column) == fourth_pawn\
                or (row, column) == fifth_pawn\
                or (row, column) == sixth_pawn\
                or (row, column) == seventh_pawn:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Pawn'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column

    def get_light_bishop_position(self):
        for row in range(0, 8):
            for column in range(1, 9):
                #Checks if the square is not empty and the colour is not the turn of whoever is playing
                #because you only want to the check the position of the enemy pieces for the king.
                if self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Bishop'\
                and self.board.board[row][column].piece.colour != self.turn\
                and (row + column) % 2 == 1:#This checks if the the bishop is a light squared bishop
                    return row, column
                 
    def get_dark_bishop_position(self):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Bishop'\
                and self.board.board[row][column].piece.colour != self.turn\
                and (row + column) % 2 == 0:#Checks if the bishop is a dark squared bishop
                    return row, column
                
    def get_first_knight_position(self):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Knight'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_second_knight_position(self):
        result = self.get_first_knight_position()
        for row in range(0, 8):
            for column in range(1, 9):
                #This check is necessary because you will always encounter the first knight first so the for loop just skips
                #this row and column when checking to ensure it gets the second knight
                if (row, column) == result:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Knight'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column  

    def get_first_rook_position(self):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Rook'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_second_rook_position(self):
        result = self.get_first_rook_position()
        for row in range(0, 8):
            for column in range(1, 9):
                #Similar thought process for the knights
                if (row, column) == result:
                    continue
                elif self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Rook'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_queen_position(self):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'Queen'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_king_position(self):
        for row in range(0, 8):
            for column in range(1, 9):
                if self.board.board[row][column].piece is not None\
                and self.board.board[row][column].piece.name == 'King'\
                and self.board.board[row][column].piece.colour != self.turn:
                    return row, column
                
    def get_queen_moves(self):
        queen_position = self.get_queen_position()
        if queen_position is not None:
            queen_row, queen_column = queen_position
            queen_moves = self.queen.get_queen_pin_moves(self.board.board, queen_row, queen_column)
        elif queen_position is None:
            queen_moves = []

        return queen_moves

    def get_new_king_moves(self, row, column, side=None):
        first_pawn_position = self.get_first_pawn_position()
        #Checks if the pawn exists
        if first_pawn_position is not None:
            first_pawn_row, first_pawn_column = first_pawn_position
            #Instead of using valid moves, I used the control moves.
            first_pawn_moves = self.pawn.get_control_moves(self.board.board, first_pawn_row, first_pawn_column)
        #Checks if the pawn no longer exists on the board (i.e has been captured)
        elif first_pawn_position is None:
            #If the pawn has been captured then all its moves are cleared
            first_pawn_moves = []

        second_pawn_position = self.get_second_pawn_position()
        if second_pawn_position is not None:
            second_pawn_row, second_pawn_column = second_pawn_position
            second_pawn_moves = self.pawn.get_control_moves(self.board.board, second_pawn_row, second_pawn_column)
        elif second_pawn_position is None:
            second_pawn_moves = []

        third_pawn_position = self.get_third_pawn_position()
        if third_pawn_position is not None:
            third_pawn_row, third_pawn_column = third_pawn_position
            third_pawn_moves = self.pawn.get_control_moves(self.board.board, third_pawn_row, third_pawn_column)
        elif third_pawn_position is None:
            third_pawn_moves = []

        fourth_pawn_position = self.get_fourth_pawn_position()
        if fourth_pawn_position is not None:
            fourth_pawn_row, fourth_pawn_column = fourth_pawn_position
            fourth_pawn_moves = self.pawn.get_control_moves(self.board.board, fourth_pawn_row, fourth_pawn_column)
        elif fourth_pawn_position is None:
            fourth_pawn_moves = []

        fifth_pawn_position = self.get_fifth_pawn_position()
        if fifth_pawn_position is not None:
            fifth_pawn_row, fifth_pawn_column = fifth_pawn_position
            fifth_pawn_moves = self.pawn.get_control_moves(self.board.board, fifth_pawn_row, fifth_pawn_column)
        elif fifth_pawn_position is None:
            fifth_pawn_moves = []

        sixth_pawn_position = self.get_sixth_pawn_position()
        if sixth_pawn_position is not None:
            sixth_pawn_row, sixth_pawn_column = sixth_pawn_position
            sixth_pawn_moves = self.pawn.get_control_moves(self.board.board, sixth_pawn_row, sixth_pawn_column)
        elif sixth_pawn_position is None:
            sixth_pawn_moves = []

        seventh_pawn_position = self.get_seventh_pawn_position()
        if seventh_pawn_position is not None:
            seventh_pawn_row, seventh_pawn_column = seventh_pawn_position
            seventh_pawn_moves = self.pawn.get_control_moves(self.board.board, seventh_pawn_row, seventh_pawn_column)
        elif seventh_pawn_position is None:
            seventh_pawn_moves = []

        eighth_pawn_position = self.get_eighth_pawn_position()
        if eighth_pawn_position is not None:
            eighth_pawn_row, eighth_pawn_column = eighth_pawn_position
            eighth_pawn_moves = self.pawn.get_control_moves(self.board.board, eighth_pawn_row, eighth_pawn_column)
        elif eighth_pawn_position is None:
            eighth_pawn_moves = []

        light_bishop_position = self.get_light_bishop_position()
        #Checks if the piece exists
        if light_bishop_position is not None:
            light_bishop_row, light_bishop_column = light_bishop_position
            light_bishop_moves = self.bishop.get_bishop_control_moves(self.board.board, light_bishop_row , light_bishop_column)
        #Checks if the piece no longer exists on the board (i.e has been captured)
        elif light_bishop_position is None:
            #If the piece has been captured then all its moves are cleared
            light_bishop_moves = []

        dark_bishop_position = self.get_dark_bishop_position()
        if dark_bishop_position is not None:
            dark_bishop_row, dark_bishop_column = dark_bishop_position
            dark_bishop_moves = self.bishop.get_bishop_control_moves(self.board.board, dark_bishop_row , dark_bishop_column)
        elif dark_bishop_position is None:
            dark_bishop_moves = []

        first_knight_position = self.get_first_knight_position()
        if first_knight_position is not None:
            first_knight_row, first_knight_column = first_knight_position
            first_knight_moves = self.knight.get_knight_control_moves(self.board.board, first_knight_row , first_knight_column)
        elif first_knight_position is None:
            first_knight_moves = []

        second_knight_position = self.get_second_knight_position()
        if second_knight_position is not None:
            second_knight_row, second_knight_column = second_knight_position
            second_knight_moves = self.knight.get_knight_control_moves(self.board.board, second_knight_row , second_knight_column)
        elif second_knight_position is None:
            second_knight_moves = []

        first_rook_position = self.get_first_rook_position()
        if first_rook_position is not None:
            first_rook_row, first_rook_column = first_rook_position
            first_rook_moves = self.rook.get_rook_control_moves(self.board.board, first_rook_row , first_rook_column)
        elif first_rook_position is None:
            first_rook_moves = []

        second_rook_position = self.get_second_rook_position()
        if second_rook_position is not None:
            second_rook_row, second_rook_column = second_rook_position
            second_rook_moves = self.rook.get_rook_control_moves(self.board.board, second_rook_row , second_rook_column)
        elif second_rook_position is None:
            second_rook_moves = []

        queen_position = self.get_queen_position()
        if queen_position is not None:
            queen_row, queen_column = queen_position
            queen_moves = self.queen.get_queen_control_moves(self.board.board, queen_row , queen_column)
        elif queen_position is None:
            queen_moves = []

        king_position = self.get_king_position()
        #King can't be captured so no need to check if it doesn't exist
        if king_position is not None:
            king_row, king_column = king_position
            opp_king_moves = self.king.get_king_control_moves(self.board.board, king_row , king_column)
        
        #These moves (king_moves) are now for the king which is selected
        king_moves = self.king.get_king_valid_moves(self.board.board, row, column)
        short_castle_moves = self.king.get_kingside_castle_moves(self.board.board, row, column)
        long_castle_moves = self.king.get_queenside_castle_moves(self.board.board, row, column)

        if side == 'kingside':
            king_moves.extend(short_castle_moves)
        elif side == 'queenside':
            king_moves.extend(long_castle_moves)

        #Loop through all the moves for the selected king
        for move in king_moves[:]:
            #First checks if the colour of the king selected is the colour of the current turn
            #and then goes on to check if any of the moves in king moves are in any of the moves of the enemy pieces
            #If they are it removes them
            if self.board.board[row][column].piece.colour == self.turn\
            and move in queen_moves\
            or move in first_pawn_moves\
            or move in second_pawn_moves\
            or move in third_pawn_moves\
            or move in fourth_pawn_moves\
            or move in fifth_pawn_moves\
            or move in sixth_pawn_moves\
            or move in seventh_pawn_moves\
            or move in eighth_pawn_moves\
            or move in light_bishop_moves\
            or move in dark_bishop_moves\
            or move in first_knight_moves\
            or move in second_knight_moves\
            or move in first_rook_moves\
            or move in second_rook_moves\
            or move in opp_king_moves:
                king_moves.remove(move)

        return king_moves
    
    def in_check(self):
        first_pawn_position = self.get_first_pawn_position()
        #Checks if the pawn exists
        if first_pawn_position is not None:
            first_pawn_row, first_pawn_column = first_pawn_position
            #Instead of using control moves, I used the valid moves.
            first_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, first_pawn_row, first_pawn_column)
        #Checks if the pawn no longer exists on the board (i.e has been captured)
        elif first_pawn_position is None:
            #If the pawn has been captured then all its moves are cleared
            first_pawn_moves = []

        second_pawn_position = self.get_second_pawn_position()
        if second_pawn_position is not None:
            second_pawn_row, second_pawn_column = second_pawn_position
            second_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, second_pawn_row, second_pawn_column)
        elif second_pawn_position is None:
            second_pawn_moves = []

        third_pawn_position = self.get_third_pawn_position()
        if third_pawn_position is not None:
            third_pawn_row, third_pawn_column = third_pawn_position
            third_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, third_pawn_row, third_pawn_column)
        elif third_pawn_position is None:
            third_pawn_moves = []

        fourth_pawn_position = self.get_fourth_pawn_position()
        if fourth_pawn_position is not None:
            fourth_pawn_row, fourth_pawn_column = fourth_pawn_position
            fourth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, fourth_pawn_row, fourth_pawn_column)
        elif fourth_pawn_position is None:
            fourth_pawn_moves = []

        fifth_pawn_position = self.get_fifth_pawn_position()
        if fifth_pawn_position is not None:
            fifth_pawn_row, fifth_pawn_column = fifth_pawn_position
            fifth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, fifth_pawn_row, fifth_pawn_column)
        elif fifth_pawn_position is None:
            fifth_pawn_moves = []

        sixth_pawn_position = self.get_sixth_pawn_position()
        if sixth_pawn_position is not None:
            sixth_pawn_row, sixth_pawn_column = sixth_pawn_position
            sixth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, sixth_pawn_row, sixth_pawn_column)
        elif sixth_pawn_position is None:
            sixth_pawn_moves = []

        seventh_pawn_position = self.get_seventh_pawn_position()
        if seventh_pawn_position is not None:
            seventh_pawn_row, seventh_pawn_column = seventh_pawn_position
            seventh_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, seventh_pawn_row, seventh_pawn_column)
        elif seventh_pawn_position is None:
            seventh_pawn_moves = []

        eighth_pawn_position = self.get_eighth_pawn_position()
        if eighth_pawn_position is not None:
            eighth_pawn_row, eighth_pawn_column = eighth_pawn_position
            eighth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, eighth_pawn_row, eighth_pawn_column)
        elif eighth_pawn_position is None:
            eighth_pawn_moves = []

        light_bishop_position = self.get_light_bishop_position()
        #Checks if the piece exists
        if light_bishop_position is not None:
            light_bishop_row, light_bishop_column = light_bishop_position
            light_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row , light_bishop_column)
        #Checks if the piece no longer exists on the board (i.e has been captured)
        elif light_bishop_position is None:
            #If the piece has been captured then all its moves are cleared
            light_bishop_moves = []

        dark_bishop_position = self.get_dark_bishop_position()
        if dark_bishop_position is not None:
            dark_bishop_row, dark_bishop_column = dark_bishop_position
            dark_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row , dark_bishop_column)
        elif dark_bishop_position is None:
            dark_bishop_moves = []

        first_knight_position = self.get_first_knight_position()
        if first_knight_position is not None:
            first_knight_row, first_knight_column = first_knight_position
            first_knight_moves = self.knight.get_knight_valid_moves(self.board.board, first_knight_row , first_knight_column)
        elif first_knight_position is None:
            first_knight_moves = []

        second_knight_position = self.get_second_knight_position()
        if second_knight_position is not None:
            second_knight_row, second_knight_column = second_knight_position
            second_knight_moves = self.knight.get_knight_valid_moves(self.board.board, second_knight_row , second_knight_column)
        elif second_knight_position is None:
            second_knight_moves = []

        first_rook_position = self.get_first_rook_position()
        if first_rook_position is not None:
            first_rook_row, first_rook_column = first_rook_position
            first_rook_moves = self.rook.get_rook_valid_moves(self.board.board, first_rook_row , first_rook_column)
        elif first_rook_position is None:
            first_rook_moves = []

        second_rook_position = self.get_second_rook_position()
        if second_rook_position is not None:
            second_rook_row, second_rook_column = second_rook_position
            second_rook_moves = self.rook.get_rook_valid_moves(self.board.board, second_rook_row , second_rook_column)
        elif second_rook_position is None:
            second_rook_moves = []

        queen_position = self.get_queen_position()
        if queen_position is not None:
            queen_row, queen_column = queen_position
            queen_moves = self.queen.get_queen_valid_moves(self.board.board, queen_row , queen_column)
        elif queen_position is None:
            queen_moves = []

        #Gets the current row and column of the king of the current players turn
        king_row, king_column = self.board.get_king_position(self.turn)

        #Checks if this row and column is in any of the valid moves of all the enemy pieces and returns True if it is
        if (king_row, king_column) in first_pawn_moves\
        or (king_row, king_column) in second_pawn_moves\
        or (king_row, king_column) in third_pawn_moves\
        or (king_row, king_column) in fourth_pawn_moves\
        or (king_row, king_column) in fifth_pawn_moves\
        or (king_row, king_column) in sixth_pawn_moves\
        or (king_row, king_column) in seventh_pawn_moves\
        or (king_row, king_column) in eighth_pawn_moves\
        or (king_row, king_column) in light_bishop_moves\
        or (king_row, king_column) in dark_bishop_moves\
        or (king_row, king_column) in first_knight_moves\
        or (king_row, king_column) in second_knight_moves\
        or (king_row, king_column) in first_rook_moves\
        or (king_row, king_column) in second_rook_moves\
        or (king_row, king_column) in queen_moves:
            return True
        else:
            return False
        
    #These following methods are used to check the position of the piece giving the check
    #in order to allow them to be captured or block the checks if necessary.
    def first_pawn_giving_check(self):
        first_pawn_position = self.get_first_pawn_position()
        if first_pawn_position is not None:
            first_pawn_row, first_pawn_column = first_pawn_position
            first_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, first_pawn_row , first_pawn_column)
        elif first_pawn_position is None:
            first_pawn_moves = []

        #Gets the current row and column of the king of the current player's turn
        king_row, king_column = self.board.get_king_position(self.turn)

        #Checks if the current king position is in the valid moves of the pawn and returns the position of the pawn
        if (king_row, king_column) in first_pawn_moves:
            return first_pawn_position
        
    def second_pawn_giving_check(self):
        second_pawn_position = self.get_second_pawn_position()
        if second_pawn_position is not None:
            second_pawn_row, second_pawn_column = second_pawn_position
            second_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, second_pawn_row , second_pawn_column)
        elif second_pawn_position is None:
            second_pawn_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in second_pawn_moves:
            return second_pawn_position
        
    def third_pawn_giving_check(self):
        third_pawn_position = self.get_third_pawn_position()
        if third_pawn_position is not None:
            third_pawn_row, third_pawn_column = third_pawn_position
            third_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, third_pawn_row , third_pawn_column)
        elif third_pawn_position is None:
            third_pawn_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in third_pawn_moves:
            return third_pawn_position
        
    def fourth_pawn_giving_check(self):
        fourth_pawn_position = self.get_fourth_pawn_position()
        if fourth_pawn_position is not None:
            fourth_pawn_row, fourth_pawn_column = fourth_pawn_position
            fourth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, fourth_pawn_row , fourth_pawn_column)
        elif fourth_pawn_position is None:
            fourth_pawn_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in fourth_pawn_moves:
            return fourth_pawn_position
        
    def fifth_pawn_giving_check(self):
        fifth_pawn_position = self.get_fifth_pawn_position()
        if fifth_pawn_position is not None:
            fifth_pawn_row, fifth_pawn_column = fifth_pawn_position
            fifth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, fifth_pawn_row , fifth_pawn_column)
        elif fifth_pawn_position is None:
            fifth_pawn_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in fifth_pawn_moves:
            return fifth_pawn_position
        
    def sixth_pawn_giving_check(self):
        sixth_pawn_position = self.get_sixth_pawn_position()
        if sixth_pawn_position is not None:
            sixth_pawn_row, sixth_pawn_column = sixth_pawn_position
            sixth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, sixth_pawn_row , sixth_pawn_column)
        elif sixth_pawn_position is None:
            sixth_pawn_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in sixth_pawn_moves:
            return sixth_pawn_position
        
    def seventh_pawn_giving_check(self):
        seventh_pawn_position = self.get_seventh_pawn_position()
        if seventh_pawn_position is not None:
            seventh_pawn_row, seventh_pawn_column = seventh_pawn_position
            seventh_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, seventh_pawn_row , seventh_pawn_column)
        elif seventh_pawn_position is None:
            seventh_pawn_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in seventh_pawn_moves:
            return seventh_pawn_position
        
    def eighth_pawn_giving_check(self):
        eighth_pawn_position = self.get_eighth_pawn_position()
        if eighth_pawn_position is not None:
            eighth_pawn_row, eighth_pawn_column = eighth_pawn_position
            eighth_pawn_moves = self.pawn.get_pawn_valid_moves(self.board.board, eighth_pawn_row , eighth_pawn_column)
        elif eighth_pawn_position is None:
            eighth_pawn_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in eighth_pawn_moves:
            return eighth_pawn_position
    
    def dark_bishop_giving_check(self):
        dark_bishop_position = self.get_dark_bishop_position()
        if dark_bishop_position is not None:
            dark_bishop_row, dark_bishop_column = dark_bishop_position
            dark_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row , dark_bishop_column)
        elif dark_bishop_position is None:
            dark_bishop_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in dark_bishop_moves:
            return dark_bishop_position
        
    def light_bishop_giving_check(self):
        light_bishop_position = self.get_light_bishop_position()
        if light_bishop_position is not None:
            light_bishop_row, light_bishop_column = light_bishop_position
            light_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row , light_bishop_column)
        elif light_bishop_position is None:
            light_bishop_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in light_bishop_moves:
            return light_bishop_position
        
    def first_knight_giving_check(self):
        first_knight_position = self.get_first_knight_position()
        if first_knight_position is not None:
            first_knight_row, first_knight_column = first_knight_position
            first_knight_moves = self.knight.get_knight_valid_moves(self.board.board, first_knight_row , first_knight_column)
        elif first_knight_position is None:
            first_knight_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in first_knight_moves:
            return first_knight_position
        
    def second_knight_giving_check(self):
        second_knight_position = self.get_second_knight_position()
        if second_knight_position is not None:
            second_knight_row, second_knight_column = second_knight_position
            second_knight_moves = self.knight.get_knight_valid_moves(self.board.board, second_knight_row , second_knight_column)
        elif second_knight_position is None:
            second_knight_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in second_knight_moves:
            return second_knight_position
        
    def first_rook_giving_check(self):
        first_rook_position = self.get_first_rook_position()
        if first_rook_position is not None:
            first_rook_row, first_rook_column = first_rook_position
            first_rook_moves = self.rook.get_rook_valid_moves(self.board.board, first_rook_row , first_rook_column)
        elif first_rook_position is None:
            first_rook_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in first_rook_moves:
            return first_rook_position
        
    def second_rook_giving_check(self):
        second_rook_position = self.get_second_rook_position()
        if second_rook_position is not None:
            second_rook_row, second_rook_column = second_rook_position
            second_rook_moves = self.rook.get_rook_valid_moves(self.board.board, second_rook_row , second_rook_column)
        elif second_rook_position is None:
            second_rook_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in second_rook_moves:
            return second_rook_position
        
    def queen_giving_check(self):
        queen_position = self.get_queen_position()
        if queen_position is not None:
            queen_row, queen_column = queen_position
            queen_moves = self.queen.get_queen_valid_moves(self.board.board, queen_row , queen_column)
        elif queen_position is None:
            queen_moves = []

        king_row, king_column = self.board.get_king_position(self.turn)

        if (king_row, king_column) in queen_moves:
            return queen_position
        
    def block_light_bishop_check(self):
        moves = []
        result = self.light_bishop_giving_check()
        if result is not None:
            light_bishop_row, light_bishop_column = result[0], result[1]

            king_row, king_column = self.board.get_king_position(self.turn)

            if light_bishop_row < king_row and light_bishop_column < king_column:
                for row in range(light_bishop_row + 1, king_row):
                    for column in range(light_bishop_column + 1, king_column):
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column):
                            moves.append((row, column))

            elif light_bishop_row < king_row and light_bishop_column > king_column:
                for row in range(light_bishop_row + 1, king_row):
                    for column in range(king_column + 1, light_bishop_column):
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column):
                            moves.append((row, column))

            elif light_bishop_row > king_row and light_bishop_column < king_column:
                for row in range(king_row + 1, light_bishop_row):
                    for column in range(light_bishop_column + 1, king_column):
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column):
                            moves.append((row, column))

            elif light_bishop_row > king_row and light_bishop_column > king_column:
                for row in range(king_row + 1, light_bishop_row):
                    for column in range(king_column + 1, light_bishop_column):
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column):
                            moves.append((row, column))

        return moves
    
    def block_dark_bishop_check(self):
        moves = []
        result = self.dark_bishop_giving_check()
        if result is not None:
            #Gets the current row and column of the bishop giving the check
            dark_bishop_row, dark_bishop_column = result[0], result[1]

            #Gets the current row and column of the king of the current player's turn
            king_row, king_column = self.board.get_king_position(self.turn)

            #Checks if the king is in the bottom right direction of the bishop
            if dark_bishop_row < king_row and dark_bishop_column < king_column:
                #Checks the squares between the king and the bishop
                for row in range(dark_bishop_row + 1, king_row):
                    for column in range(dark_bishop_column + 1, king_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the bishop from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column):
                            moves.append((row, column))

            #Checks if the king is in the bottom left direction of the bishop
            elif dark_bishop_row < king_row and dark_bishop_column > king_column:
                #Checks the squares between the king and the bishop
                for row in range(dark_bishop_row + 1, king_row):
                    for column in range(king_column + 1, dark_bishop_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the bishop from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column):
                            moves.append((row, column))

            #Checks if the king is in the top right direction of the bishop
            elif dark_bishop_row > king_row and dark_bishop_column < king_column:
                #Checks the squares between the king and the bishop
                for row in range(king_row + 1, dark_bishop_row):
                    for column in range(dark_bishop_column + 1, king_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the bishop from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column):
                            moves.append((row, column))

            #Checks if the king is in the top left direction of the bishop
            elif dark_bishop_row > king_row and dark_bishop_column > king_column:
                #Checks the squares between the king and the bishop
                for row in range(king_row + 1, dark_bishop_row):
                    for column in range(king_column + 1, dark_bishop_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the bishop from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column):
                            moves.append((row, column))

        return moves
    
    def block_first_rook_check(self):
        moves = []
        result = self.first_rook_giving_check()
        if result is not None:
            #Gets the current rook row and column giving the check
            first_rook_row, first_rook_column = result[0], result[1]

            #Gets the row and column of the king of the current player's turn
            king_row, king_column = self.board.get_king_position(self.turn)

            #Checks if the king is below the rook and they are both on the same column
            if first_rook_row < king_row and first_rook_column == king_column:
                #This for loop is then used to check all the squares between the king and the rook and then adds them to moves
                for row in range(first_rook_row + 1, king_row):
                    moves.append((row, first_rook_column))

            #Checks if the king is above the rook and they're on the same column
            elif first_rook_row > king_row and first_rook_column == king_column:
                #This also checks all the squares between the king and rook and adds them to moves
                for row in range(king_row + 1, first_rook_row):
                    moves.append((row, first_rook_column))

            #Checks if the king and rook are on the same row and the king is to the right of the rook
            elif first_rook_row == king_row and first_rook_column < king_column:
                #Adds all the squares between the king and rook in this scenario to moves
                for column in range(first_rook_column + 1, king_column):
                    moves.append((first_rook_row, column))

            #Checks if the king and rook are on the same row and the king is to the left of the rook
            elif first_rook_row == king_row and first_rook_column > king_column:
                #Adds all the squares between the king and rook to moves
                for column in range(king_column + 1, first_rook_column):
                    moves.append((first_rook_row, column))

        return moves
    
    def block_second_rook_check(self):
        moves = []
        result = self.second_rook_giving_check()
        if result is not None:
            second_rook_row, second_rook_column = result[0], result[1]

            king_row, king_column = self.board.get_king_position(self.turn)

            if second_rook_row < king_row and second_rook_column == king_column:
                for row in range(second_rook_row + 1, king_row):
                    moves.append((row, second_rook_column))

            elif second_rook_row > king_row and second_rook_column == king_column:
                for row in range(king_row + 1, second_rook_row):
                    moves.append((row, second_rook_column))

            elif second_rook_row == king_row and second_rook_column < king_column:
                for column in range(second_rook_column + 1, king_column):
                    moves.append((second_rook_row, column))

            elif second_rook_row == king_row and second_rook_column > king_column:
                for column in range(king_column + 1, second_rook_column):
                    moves.append((second_rook_row, column))

        return moves
    
    def block_queen_check(self):
        moves = []
        result = self.queen_giving_check()
        if result is not None:
            #Gets the current row and column of the queen giving the check
            queen_row, queen_column = result[0], result[1]

            #Gets the current row and column of the king of the current player's turn
            king_row, king_column = self.board.get_king_position(self.turn)

            #Checks if the king is in the bottom right direction of the queen
            if queen_row < king_row and queen_column < king_column:
                #Checks the squares between the king and the queen
                for row in range(queen_row + 1, king_row):
                    for column in range(queen_column + 1, king_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column):
                            moves.append((row, column))

            #Checks if the king is in the bottom left direction of the queen
            elif queen_row < king_row and queen_column > king_column:
                #Checks the squares between the king and the queen
                for row in range(queen_row + 1, king_row):
                    for column in range(king_column + 1, queen_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column):
                            moves.append((row, column))

            #Checks if the king is in the top right direction of the queen
            elif queen_row > king_row and queen_column < king_column:
                #Checks the squares between the king and the queen
                for row in range(king_row + 1, queen_row):
                    for column in range(queen_column + 1, king_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column):
                            moves.append((row, column))

            #Checks if the king is in the top left direction of the queen
            elif queen_row > king_row and queen_column > king_column:
                #Checks the squares between the king and the queen
                for row in range(king_row + 1, queen_row):
                    for column in range(king_column + 1, queen_column):
                        #Checks if the squares checked by the for loop are in the valid moves of the queen from that position
                        #and if they are, they are added to moves.
                        if (row, column) in self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column):
                            moves.append((row, column))

            #Checks if the king is below the rook and they are both on the same column
            elif queen_row < king_row and queen_column == king_column:
                #This for loop is then used to check all the squares between the king and the rook and then adds them to moves
                for row in range(queen_row + 1, king_row):
                    moves.append((row, queen_column))

            #Checks if the king is above the rook and they're on the same column
            elif queen_row > king_row and queen_column == king_column:
                #This also checks all the squares between the king and rook and adds them to moves
                for row in range(king_row + 1, queen_row):
                    moves.append((row, queen_column))

            #Checks if the king and rook are on the same row and the king is to the right of the rook
            elif queen_row == king_row and queen_column < king_column:
                #Adds all the squares between the king and rook in this scenario to moves
                for column in range(queen_column + 1, king_column):
                    moves.append((queen_row, column))

            #Checks if the king and rook are on the same row and the king is to the left of the rook
            elif queen_row == king_row and queen_column > king_column:
                #Adds all the squares between the king and rook to moves
                for column in range(king_column + 1, queen_column):
                    moves.append((queen_row, column))

        return moves
    
    def piece_pinned(self, name, position):
        result = False
        if name == 'Pawn' and position == 1:
            piece_position = self.board.get_first_pawn_position(self.turn)
        elif name == 'Pawn' and position == 2:
            piece_position = self.board.get_second_pawn_position(self.turn)
        elif name == 'Pawn' and position == 3:
            piece_position = self.board.get_third_pawn_position(self.turn)
        elif name == 'Pawn' and position == 4:
            piece_position = self.board.get_fourth_pawn_position(self.turn)
        elif name == 'Pawn' and position == 5:
            piece_position = self.board.get_fifth_pawn_position(self.turn)
        elif name == 'Pawn' and position == 6:
            piece_position = self.board.get_sixth_pawn_position(self.turn)
        elif name == 'Pawn' and position == 7:
            piece_position = self.board.get_seventh_pawn_position(self.turn)
        elif name == 'Pawn' and position == 8:
            piece_position = self.board.get_eighth_pawn_position(self.turn)
        elif name == 'Knight' and position == 1:
            piece_position = self.board.get_first_knight_position(self.turn)
        elif name == 'Knight' and position == 2:
            piece_position = self.board.get_second_knight_position(self.turn)
        elif name == 'Rook' and position == 1:
            piece_position = self.board.get_first_rook_position(self.turn)
        elif name == 'Rook' and position == 2:
            piece_position = self.board.get_second_rook_position(self.turn)
        elif name == 'Bishop' and position == 'Light':
            piece_position = self.board.get_light_bishop_position(self.turn)
        elif name == 'Bishop' and position == 'Dark':
            piece_position = self.board.get_dark_bishop_position(self.turn)
        elif name == 'Queen' and position == 1:
            piece_position = self.board.get_queen_position(self.turn)

        if piece_position is not None:
            piece_row, piece_column = piece_position

        king_row, king_column = self.board.get_king_position(self.turn)

        #This gets the valid and pin moves of the light squared bishop
        light_bishop_position = self.get_light_bishop_position()
        if light_bishop_position is not None:
            light_bishop_row, light_bishop_column = light_bishop_position
            light_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, light_bishop_row, light_bishop_column)
            light_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, light_bishop_row, light_bishop_column)

        #This gets the valid and pin moves of the light squared bishop
        dark_bishop_position = self.get_dark_bishop_position()
        if dark_bishop_position is not None:
            dark_bishop_row, dark_bishop_column = dark_bishop_position
            dark_bishop_moves = self.bishop.get_bishop_valid_moves(self.board.board, dark_bishop_row, dark_bishop_column)
            dark_pin_moves = self.bishop.get_bishop_pin_moves(self.board.board, dark_bishop_row, dark_bishop_column)
        
        #These get the valid moves of the two rooks
        first_rook_position = self.get_first_rook_position()
        if first_rook_position is not None:
            first_rook_row, first_rook_column = first_rook_position
            first_rook_moves = self.rook.get_rook_valid_moves(self.board.board, first_rook_row, first_rook_column)

        second_rook_position = self.get_second_rook_position()
        if second_rook_position is not None:
            second_rook_row, second_rook_column = second_rook_position
            second_rook_moves = self.rook.get_rook_valid_moves(self.board.board, second_rook_row, second_rook_column)

        #Gets the valid moves and pin moves of the opponent's queen
        queen_position = self.get_queen_position()
        if queen_position is not None:
            queen_row, queen_column = queen_position
            queen_moves = self.queen.get_queen_valid_moves(self.board.board, queen_row, queen_column)
            queen_pin_moves = self.queen.get_queen_pin_moves(self.board.board, queen_row, queen_column)

        #Checks if the piece is on the same vertical file as the king and rook and the king is below the rook
        if first_rook_position is not None and piece_position is not None and (piece_column == first_rook_column == king_column)\
            and first_rook_row < piece_row < king_row and (piece_row, piece_column) in first_rook_moves:
            result = True

            all_none = True
            for row in range(piece_row + 1, king_row):
                #Checks if the squares between the piece and king are not empty or the king is directly behind the piece
                if self.board.board[row][first_rook_column].piece != None or piece_row + 1 == king_row:
                    all_none = False
                    break
            
            #This then checks if both condtions have been satisfied for the piece to be considered pinned
            if result == True and all_none == True:
                return True
            
        #Checks if the piece is on the same row as the king and rook and the king is to the left of the rook
        elif first_rook_position is not None and piece_position is not None and piece_row == first_rook_row == king_row\
            and king_column < piece_column < first_rook_column and (piece_row, piece_column) in first_rook_moves:
            result = True

            all_none = True
            for column in range(king_column + 1, piece_column):
                #Checks if the squares between the piece and king are not empty or the king is directly to the left of the piece
                if self.board.board[first_rook_row][column].piece != None or king_column + 1 == piece_column:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True
            
        #This is similar to the if block but just checks if the king is above instead of below 
        elif first_rook_position is not None and piece_position is not None and (piece_column == first_rook_column == king_column)\
            and king_row < piece_row < first_rook_row and (piece_row, piece_column) in first_rook_moves:
            result = True

            all_none = True
            for row in range(king_row + 1, piece_row):
                if self.board.board[row][first_rook_column].piece != None or king_row + 1 == piece_row:
                    all_none = False
                    break
                    
            if result == True and all_none == True:
                return True
            
        #This is similar to the previous elif block but just checks if the king is to the right instead of the left of the rook 
        elif first_rook_position is not None and piece_position is not None and piece_row == first_rook_row and king_row == first_rook_row\
            and first_rook_column < piece_column < king_column and (piece_row, piece_column) in first_rook_moves:
            result = True

            all_none = True
            for column in range(piece_column + 1, king_column):
                if self.board.board[first_rook_row][column].piece != None or piece_column + 1 == king_column:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True

        elif second_rook_position is not None and piece_position is not None and piece_column == second_rook_column and king_column == second_rook_column\
            and second_rook_row < piece_row < king_row and (piece_row, piece_column) in second_rook_moves:
            result = True

            all_none = True
            for row in range(piece_row + 1, king_row):
                if self.board.board[row][second_rook_column].piece != None or piece_row + 1 == king_row:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True
            
        elif second_rook_position is not None and piece_position is not None and piece_column == second_rook_column and king_column == second_rook_column\
            and king_row < piece_row < second_rook_row and (piece_row, piece_column) in second_rook_moves:
            result = True

            all_none = True
            for row in range(king_row + 1, piece_row):
                if self.board.board[row][second_rook_column].piece != None or king_row + 1 == piece_row:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True
            
        elif second_rook_position is not None and piece_position is not None and piece_row == second_rook_row and king_row == second_rook_row\
            and king_column < piece_column < second_rook_column and (piece_row, piece_column) in second_rook_moves:
            result = True

            all_none = True
            for column in range(king_column + 1, piece_column):
                if self.board.board[second_rook_row][column].piece != None or king_column + 1 == piece_column:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True
            
        elif second_rook_position is not None and piece_position is not None and piece_row == second_rook_row and king_row == second_rook_row\
            and second_rook_column < piece_column < king_column and (piece_row, piece_column) in second_rook_moves:
            result = True

            all_none = True
            for column in range(piece_column + 1, king_column):
                if self.board.board[second_rook_row][column].piece != None or piece_column + 1 == king_column:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True

        #This checks if the piece is between the bishop and king in the top-left to bottom-right diagonal
        elif light_bishop_position is not None and piece_position is not None and light_bishop_row < piece_row < king_row\
            and light_bishop_column < piece_column < king_column and (piece_row, piece_column) in light_bishop_moves\
            and (king_row, king_column) in light_pin_moves:
            result = True

            all_none = True
            squares = king_row - piece_row

            for i in range(1, squares): 
                #This makes it so that the row and column increment by the same amount so that way only diagonals are considered. 
                row  = piece_row + i 
                column = piece_column + i
                #This checks if the squares between the piece and king are occupied 
                if self.board.board[row][column].piece is not None: 
                    all_none = False 
                    break 
            
            if result == True and all_none == True: 
                return True

        #This checks if the piece is between the bishop and king in the top-right to bottom-left diagonal
        elif light_bishop_position is not None and piece_position is not None and light_bishop_row < piece_row < king_row\
            and king_column < piece_column < light_bishop_column and (piece_row, piece_column) in light_bishop_moves\
            and (king_row, king_column) in light_pin_moves:
            result = True

            all_none = True
            squares = king_row - piece_row

            #Uses same logic as previous elif block
            for i in range(1, squares):
                #This ensures the only the diagonals are checked.
                row  = piece_row + i
                column = piece_column - i

                #This checks if the squares between the piece and king are occupied
                if self.board.board[row][column].piece is not None:
                    all_none = False
                    break

            if result == True and all_none == True:
                return True
        
        #This checks if the piece is between the bishop and king in the bottom-left to top-right diagonal
        elif light_bishop_position is not None and piece_position is not None and king_row < piece_row < light_bishop_row\
            and light_bishop_column < piece_column < king_column and (piece_row, piece_column) in light_bishop_moves\
            and (king_row, king_column) in light_pin_moves:
            result = True

            all_none = True
            squares = piece_row - king_row

            #Uses same logic as previous elif block
            for i in range(1, squares):
                #This ensures the only the diagonals are checked.
                row  = piece_row - i
                column = piece_column + i

                #This checks if the squares between the piece and king are occupied
                if self.board.board[row][column].piece is not None:
                    all_none = False
                    break

            if result == True and all_none == True:
                return True
            
        #This checks if the piece is between the bishop and king in the bottom-right to top-left diagonal
        elif light_bishop_position is not None and piece_position is not None and king_row < piece_row < light_bishop_row\
            and king_column < piece_column < light_bishop_column and (piece_row, piece_column) in light_bishop_moves\
            and (king_row, king_column) in light_pin_moves:
            result = True

            all_none = True
            squares = piece_row - king_row

            #Uses same logic as previous elif block
            for i in range(1, squares):
                #This ensures the only the diagonals are checked.
                row  = piece_row - i
                column = piece_column - i

                #This checks if the squares between the piece and king are occupied
                if self.board.board[row][column].piece is not None:
                    all_none = False
                    break

            if result == True and all_none == True:
                return True
            
        #This checks if the piece is between the bishop and king in the top-left to bottom-right diagonal
        elif dark_bishop_position is not None and piece_position is not None and dark_bishop_row < piece_row < king_row\
            and dark_bishop_column < piece_column < king_column and (piece_row, piece_column) in dark_bishop_moves\
            and (king_row, king_column) in dark_pin_moves:
            result = True

            all_none = True
            squares = king_row - piece_row

            for i in range(1, squares): 
                #This makes it so that the row and column increment by the same amount so that way only diagonals are considered. 
                row  = piece_row + i 
                column = piece_column + i
                #This checks if the squares between the piece and king are occupied 
                if self.board.board[row][column].piece is not None: 
                    all_none = False 
                    break 
            
            if result == True and all_none == True: 
                return True

        #This checks if the piece is between the bishop and king in the top-right to bottom-left diagonal   
        elif dark_bishop_position is not None and piece_position is not None and dark_bishop_row < piece_row < king_row\
            and king_column < piece_column < dark_bishop_column and (piece_row, piece_column) in dark_bishop_moves\
            and (king_row, king_column) in dark_pin_moves:
            result = True

            all_none = True
            squares = king_row - piece_row

            #Uses same logic as previous elif block
            for i in range(1, squares):
                #This ensures the only the diagonals are checked.
                row  = piece_row + i
                column = piece_column - i

                #This checks if the squares between the piece and king are occupied
                if self.board.board[row][column].piece is not None:
                    all_none = False
                    break

            if result == True and all_none == True:
                return True
            
        #This checks if the piece is between the bishop and king in the bottom-left to top-right diagonal
        elif dark_bishop_position is not None and piece_position is not None and king_row < piece_row < dark_bishop_row\
            and dark_bishop_column < piece_column < king_column and (piece_row, piece_column) in dark_bishop_moves\
            and (king_row, king_column) in dark_pin_moves:
            result = True

            all_none = True
            squares = piece_row - king_row

            #Uses same logic as previous elif block
            for i in range(1, squares):
                #This ensures the only the diagonals are checked.
                row  = piece_row - i
                column = piece_column + i

                #This checks if the squares between the piece and king are occupied
                if self.board.board[row][column].piece is not None:
                    all_none = False
                    break

            if result == True and all_none == True:
                return True
            
        #This checks if the piece is between the bishop and king in the bottom-right to top-left diagonal
        elif dark_bishop_position is not None and piece_position is not None and king_row < piece_row < dark_bishop_row\
            and king_column < piece_column < dark_bishop_column and (piece_row, piece_column) in dark_bishop_moves\
            and (king_row, king_column) in dark_pin_moves:
            result = True

            all_none = True
            squares = piece_row - king_row

            #Uses same logic as previous elif block
            for i in range(1, squares):
                #This ensures the only the diagonals are checked.
                row  = piece_row - i
                column = piece_column - i

                #This checks if the squares between the piece and king are occupied
                if self.board.board[row][column].piece is not None:
                    all_none = False
                    break

            if result == True and all_none == True:
                return True
            
        elif queen_position is not None and piece_position is not None and piece_column == queen_column\
            and king_column == queen_column and queen_row < piece_row < king_row and (piece_row, piece_column) in queen_moves:
            result = True

            all_none = True
            for row in range(piece_row + 1, king_row):
                if self.board.board[row][queen_column].piece != None or piece_row + 1 == king_row:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True
            
        elif queen_position is not None and piece_position is not None and piece_column == queen_column\
            and king_column == queen_column and king_row < piece_row < queen_row and (piece_row, piece_column) in queen_moves:
            result = True

            all_none = True
            for row in range(king_row + 1, piece_row):
                if self.board.board[row][queen_column].piece != None or king_row + 1 == piece_row:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True
            
        elif queen_position is not None and piece_position is not None and piece_row == queen_row\
            and king_row == queen_row and king_column < piece_column < queen_column and (piece_row, piece_column) in queen_moves:
            result = True

            all_none = True
            for column in range(king_column + 1, piece_column):
                if self.board.board[queen_row][column].piece != None or king_column + 1 == piece_column:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True
            
        elif queen_position is not None and piece_position is not None and piece_row == queen_row\
            and king_row == queen_row and queen_column < piece_column < king_column and (piece_row, piece_column) in queen_moves:
            result = True

            all_none = True
            for column in range(piece_column + 1, king_column):
                if self.board.board[queen_row][column].piece != None or piece_column + 1 == king_column:
                    all_none = False
                    break
                
            if result == True and all_none == True:
                return True

        #This checks if the piece is between the queen and king in the top-left to bottom-right diagonal
        elif queen_position is not None and piece_position is not None and queen_row < piece_row < king_row\
            and queen_column < piece_column < king_column and (piece_row, piece_column) in queen_moves\
            and (king_row, king_column) in queen_pin_moves:
            result = True

            all_none = True
            squares = king_row - piece_row

            for i in range(1, squares): 
                #This makes it so that the row and column increment by the same amount so that way only diagonals are considered. 
                row  = piece_row + i 
                column = piece_column + i
                #This checks if the squares between the piece and king are occupied 
                if self.board.board[row][column].piece is not None: 
                    all_none = False 
                    break 
            
            if result == True and all_none == True: 
                return True
            
        #This checks if the piece is between the queen and king in the top-right to bottom-left diagonal
        elif queen_position is not None and piece_position is not None and queen_row < piece_row < king_row\
            and king_column < piece_column < queen_column and (piece_row, piece_column) in queen_moves\
            and (king_row, king_column) in queen_pin_moves:
            result = True

            all_none = True
            squares = king_row - piece_row

            for i in range(1, squares): 
                #This makes it so that the row and column increment by the same amount so that way only diagonals are considered. 
                row  = piece_row + i 
                column = piece_column - i
                #This checks if the squares between the piece and king are occupied 
                if self.board.board[row][column].piece is not None: 
                    all_none = False 
                    break 
            
            if result == True and all_none == True: 
                return True
            
        #This checks if the piece is between the queen and king in the bottom-left to top-right diagonal
        elif queen_position is not None and piece_position is not None and king_row < piece_row < queen_row\
            and queen_column < piece_column < king_column and (piece_row, piece_column) in queen_moves\
            and (king_row, king_column) in queen_pin_moves:
            result = True

            all_none = True
            squares = piece_row - king_row

            for i in range(1, squares): 
                #This makes it so that the row and column increment by the same amount so that way only diagonals are considered. 
                row  = piece_row - i 
                column = piece_column + i
                #This checks if the squares between the piece and king are occupied 
                if self.board.board[row][column].piece is not None: 
                    all_none = False 
                    break
            
            if result == True and all_none == True:
                return True
            
        #This checks if the piece is between the queen and king in the bottom-right to top-left diagonal
        elif queen_position is not None and piece_position is not None and king_row < piece_row < queen_row\
            and king_column < piece_column < queen_column and (piece_row, piece_column) in queen_moves\
            and (king_row, king_column) in queen_pin_moves:
            result = True

            all_none = True
            squares = piece_row - king_row

            for i in range(1, squares): 
                #This makes it so that the row and column increment by the same amount so that way only diagonals are considered. 
                row  = piece_row - i 
                column = piece_column - i
                #This checks if the squares between the piece and king are occupied 
                if self.board.board[row][column].piece is not None: 
                    all_none = False 
                    break 
            
            if result == True and all_none == True: 
                return True
            
        return False
    
    
    

    
    
    
    
        

                



    
            
        


    

    


            


        

    



        
        


        

        
    

        


    


   

