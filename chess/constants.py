SQUARE_WIDTH = 100 
SQUARE_HEIGHT = 100

#rgb
GREEN = (118,170,86)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
DGREY = (60, 60, 60)
LGREY = (185, 181, 181)
GREY = (128, 128, 128)
BLUE = (106, 140, 175)
BROWN = (181, 136, 99)

# Pawn can only capture pinning piece if in diagonal capture moves
#Dynamically gets the method to calculate control moves for the given piece. So for instance, if name is queen it becomes self.queen.GetValidMoves and if name is rook, its self.rook.GetValidMoves and so on
