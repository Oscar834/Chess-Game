import pygame

class Button:
    def __init__(self, x, y, image, scale):
        imageWidth = image.get_width()
        imageHeight = image.get_height()
        self.image = pygame.transform.scale(image, (int(imageWidth * scale), int(imageHeight * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def create_button(self, window):
        clickAction = False
        mousePosition = pygame.mouse.get_pos()

        #Checks if the mouse cursor is hovering over the button
        if self.rect.collidepoint(mousePosition):

            #Checks if the left-click button has been clicked and if it wasn't already clicked before
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                clickAction = True

            #Checks if the the left-click button has not been clicked.
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #Displays the button image onto the game window.
        window.blit(self.image, (self.rect.x, self.rect.y))

        return clickAction




        