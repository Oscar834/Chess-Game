import pygame
import sys
from chess.button import Button
from chess.constants import SQUARE_HEIGHT, SQUARE_WIDTH, WHITE, GREEN, BLACK
from chess.game_manager import Game

pygame.init()

gameWindow = pygame.display.set_mode((1000, 800))
gameIcon = pygame.image.load('images/king.png')
pygame.display.set_icon(gameIcon)
clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption('Chess')

mainText = pygame.font.SysFont('Arial', 120, bold=True)
diffText = pygame.font.SysFont('Arial', 100, bold=True)
subText = pygame.font.SysFont('Arial', 50)
game = Game(gameWindow)

#Function that first converts the text into an image in order to allow it to be displayed on the screen
def display_text(text, font, color, x, y):
    image = font.render(text, True, color)
    gameWindow.blit(image, (x, y))

#This function gets the current row and column from the position of the mouse on the screen
def get_row_column_from_mouse(mouse_pos):
    x, y = mouse_pos
    row = y // SQUARE_WIDTH
    column = x // SQUARE_HEIGHT
    return row, column

def play(time):
    running = True
    FONT = pygame.font.SysFont('Roboto Mono', 50)

    # Initialises timer values for white and black depending on the timer option chosing in the timer selection menu
    white_seconds = time * 60
    black_seconds = time * 60
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Checks where the mouse button is clicked and uses it to determine the
            #row and column from the mouse position
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, column = get_row_column_from_mouse(mouse_pos)
                #This method from the Game class is called here and is responsible for
                #the selection of squares which include selecting the piece and moving it to a square.
                game.select_square(row, column)
                
            elif event.type == pygame.USEREVENT:
                # Checks if it is currently white's turn
                if game.switch_timer() == 'White':
                    # Makes white's time tick down
                    white_seconds -= 1
                # Checks if it is currently black's turn
                elif game.switch_timer() == 'Black':
                    # Makes black' time tick down
                    black_seconds -= 1

        # Draws the rectangles on which the timers would appear
        pygame.draw.rect(gameWindow, WHITE, (1, 375, 98, 50))
        pygame.draw.rect(gameWindow, BLACK, (901, 375, 98, 50))

        # Displays white's timer
        if white_seconds >= 0:
            white_minutes = white_seconds // 60
            white_secs = white_seconds % 60
        # Responsible for converting the display into the correct format by using zero padding for seconds
        white_timer_text = FONT.render(f"{white_minutes}:{white_secs:02}", True, BLACK)
        white_timer_rect = white_timer_text.get_rect(center=(49, 400))
        gameWindow.blit(white_timer_text, white_timer_rect)

        # Displays black's timer
        if black_seconds >= 0:
            black_minutes = black_seconds // 60
            black_secs = black_seconds % 60
        #Responsible for converting the display into the correct format by using zero padding for seconds
        black_timer_text = FONT.render(f"{black_minutes}:{black_secs:02}", True, WHITE)
        black_timer_rect = black_timer_text.get_rect(center=(949, 400))
        gameWindow.blit(black_timer_text, black_timer_rect)

        pygame.display.flip()
        game.update_screen()
        clock.tick(fps)

def winner(outcome):
    targetMenu = None
    if outcome == 'win':
        gameWindow.fill(GREEN)
        display_text('WHITE WON!', mainText, WHITE, 190, 50)
        display_text('by checkmate', subText, WHITE, 360, 180)
    elif outcome == 'draw':
        gameWindow.fill((128, 128, 128))
        display_text('GAME DRAWN!', mainText, WHITE, 140, 50)
        display_text('by stalemate', subText, WHITE, 380, 180)

    #gameWindow.fill(GREEN)
    main, rematch = False, False

    homeImage = pygame.image.load('images/Main Menu.png')
    rematchImage = pygame.image.load('images/rematch.png')
    confirmImage = pygame.image.load('images/Confirm.png')

    homeButton = Button(300, 450, homeImage, 2.5)
    rematchButton = Button(600, 450, rematchImage, 2.5)

    homeBorder = pygame.Rect(300, 450, 130, 130)
    rematchBorder = pygame.Rect(600, 450, 130, 130)

    run = True
    while run:
        if homeButton.create_button(gameWindow):
            main, rematch = True, False

        if rematchButton.create_button(gameWindow):
            main, rematch = False, True

        if main:
            pygame.draw.rect(gameWindow, (241, 249, 26), homeBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            if confirmButton.create_button(gameWindow):
                targetMenu = 'main_menu'
                run = False
        elif rematch:
            pygame.draw.rect(gameWindow, (241, 249, 26), rematchBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            if confirmButton.create_button(gameWindow):
                targetMenu = 'play'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    if targetMenu == 'main_menu':
        main_menu()
    elif targetMenu == 'play':
        play()

def difficulty_selection():
    targetMenu = None
    bgImage = pygame.image.load('images/Difficulty.png')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    easy, medium, hard, back = False, False, False, False # Flags to set the selected diffculty or back button

    #Displays the menu title
    display_text('SELECT DIFFICULTY', diffText, (241, 249, 26), 110, 10)

    backImage = pygame.image.load('images/Back Image.png')
    confirmImage = pygame.image.load('images/Confirm.png')
    easyImage = pygame.image.load('images/Easy.png')
    mediumImage = pygame.image.load('images/Medium.png')
    hardImage = pygame.image.load('images/Hard.png')

    # Initialises the buttons using an instance of the button class
    backButton = Button(10, 30, backImage, 0.2)
    easyButton = Button(80, 300, easyImage, 1.5)
    mediumButton = Button(380, 300, mediumImage, 1.5)
    hardButton = Button(680, 300, hardImage, 1.5)

    # Sets the border width, height and top left coordinates
    easyBorder = pygame.Rect(80, 300, 226.5, 127.5)
    mediumBorder = pygame.Rect(380, 300, 229.5, 126)
    hardBorder = pygame.Rect(680, 300, 232.5, 126)
    backBorder = pygame.Rect(10, 30, 73, 42.8)

    run = True
    while run:
        # Checks if the back button is clicked
        if backButton.create_button(gameWindow):
            easy, medium, hard, back = False, False, False, True # Sets the back button flag to true

        # Checks if the easy button is clicked
        if easyButton.create_button(gameWindow):
            easy, medium, hard, back = True, False, False, False # Sets the easy button flag to true 

        # Checks if the medium button is clicked
        if mediumButton.create_button(gameWindow):
            easy, medium, hard, back = False, True, False, False # Sets the medium button flag to true

        # Checks if the hard button is clicked
        if hardButton.create_button(gameWindow):
            easy, medium, hard, back = False, False, True, False # Sets the hard button flag to true

        # Checks if the back button flag is true to indicate that the back button has been selected
        if back:
            # Draws the yellow rectangle border around the back button
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            # Confirm button only dispplayed once a button has been clicked
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button has been clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'game_mode'
                run = False

        # Checks if the easy button flag is true to indicate that the easy button has been selected
        elif easy:
            # Draws the yellow rectangle border around the easy button
            pygame.draw.rect(gameWindow, (241, 249, 26), easyBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'Easy_AI_timer'
                run = False

        # Checks if the medium button flag is true to indicate that the medium button has been selected       
        elif medium:
            # Draws the yellow rectangle border around the medium button
            pygame.draw.rect(gameWindow, (241, 249, 26), mediumBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'Medium_AI_timer'
                run = False

        # Checks if the hard button flag is true to indicate that the hard button has been selected
        elif hard:
            # Draws the yellow rectangle border around the hard button
            pygame.draw.rect(gameWindow, (241, 249, 26), hardBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'Hard_AI_timer'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menus
    if targetMenu == 'game_mode':
        game_mode()
    elif targetMenu == 'Easy_AI_timer':
        timer_selection('Easy')
    elif targetMenu == 'Medium_AI_timer':
        timer_selection('Medium')
    elif targetMenu == 'Hard_AI_timer':
        timer_selection('Hard')
    
def timer_selection(difficulty=None):
    targetMenu = None
    bgImage = pygame.image.load('images/Timer Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    timer1, timer3, timer5, timer10, back = False, False, False, False, False # Flags to set the selected diffculty or back button

    # Displays the menu title
    display_text('SELECT TIMER', mainText, (241, 249, 26), 140, 10)

    # Checks what difficulty was selected from the difficulty selection menu and displays the correct sub heading
    if difficulty == 'Easy':
        display_text('Difficulty: EASY', subText, (241, 249, 26), 140, 150)
    elif difficulty == 'Medium':
        display_text('Difficulty: MEDIUM', subText, (241, 249, 26), 140, 150)
    elif difficulty == 'Hard':
        display_text('Difficulty: HARD', subText, (241, 249, 26), 140, 150)

    backImage = pygame.image.load('images/Back Image.png')
    confirmImage = pygame.image.load('images/Confirm.png')
    firstTimer = pygame.image.load('images/1 min.png')
    secondTimer = pygame.image.load('images/3 min.png')
    thirdTimer = pygame.image.load('images/5 min.png')
    fourthTimer = pygame.image.load('images/10 min.png')

    # Initialises the buttons using an instance of the button class
    backButton = Button(10, 30, backImage, 0.2)
    timer1Button = Button(250, 300, firstTimer, 1.25)
    timer3Button = Button(500, 300, secondTimer, 1.25)
    timer5Button = Button(250, 500, thirdTimer, 1.25)
    timer10Button = Button(500, 500, fourthTimer, 1.25)

    # Sets the border width, height and top left coordinates for each button
    timer1Border = pygame.Rect(250, 300, 200, 71.25)
    timer3Border = pygame.Rect(500, 300, 200, 71.25)
    timer5Border = pygame.Rect(250, 500, 200, 71.25)
    timer10Border = pygame.Rect(500, 500, 198.75, 70)
    backBorder = pygame.Rect(10, 30, 73, 42.8)

    run = True
    while run:
        # Checks if the back button is clicked
        if backButton.create_button(gameWindow):
            timer1, timer3, timer5, timer10, back = False, False, False, False, True # Sets the back button flag to true

        # Checks if the 1min timer button is clicked
        if timer1Button.create_button(gameWindow):
            timer1, timer3, timer5, timer10, back = True, False, False, False, False # Sets the 1min timer button flag to true

        # Checks if the 3min timer button is clicked
        if timer3Button.create_button(gameWindow):
            timer1, timer3, timer5, timer10, back = False, True, False, False, False # Sets the 3min timer button flag to true

        # Checks if the 5min timer button is clicked
        if timer5Button.create_button(gameWindow):
            timer1, timer3, timer5, timer10, back = False, False, True, False, False # Sets the 5min timer button flag to true

        # Checks if the 10min timer button is clicked
        if timer10Button.create_button(gameWindow):
            timer1, timer3, timer5, timer10, back = False, False, False, True, False # Sets the 10min timer button flag to true

        # Checks if the 1min button flag is set to true
        if timer1:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer1Border, 4) #Draws the yellow border around the 1min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'play 1min'
                run = False

        # Checks if the 3min button flag is set to true
        elif timer3:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer3Border, 4) #Draws the yellow border around the 3min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'play 3min'
                run = False

        # Checks if the 5min button flag is set to true
        elif timer5:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer5Border, 4) #Draws the yellow border around the 5min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'play 5min'
                run = False

        # Checks if the 10min button flag is set to true
        elif timer10:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer10Border, 4) #Draws the yellow border around the 10min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'play 10min'
                run = False
                
        # Checks if the back button flag is set to true and the player came from the game mode after clicking play human
        elif back and difficulty == None:
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'game_mode'
                run = False

        # Checks if the back button flag is set to true and the player came from the difficulty selection menu
        elif back and (difficulty == 'Easy' or difficulty == 'Medium' or difficulty == 'Hard'):
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'difficulty_selection'
                run = False 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menus
    if targetMenu == 'game_mode':
        game_mode()
    elif targetMenu == 'difficulty_selection':
        difficulty_selection()
    elif targetMenu == 'play 1min':
        play(1)
    elif targetMenu == 'play 3min':
        play(3)
    elif targetMenu == 'play 5min':
        play(5)
    elif targetMenu == 'play 10min':
        play(10)

def settings():
    targetMenu = None
    bgImage = pygame.image.load('images/Mode Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    blue, brown, green = False, False, False  # Flags to set the selected board colour
    on, off = False, False # Flags to set the selected sound option

    # Displays the menu title as well as the sub heading for the different settings
    display_text('GAME SETTINGS', mainText, (241, 249, 26), 100, 10)
    display_text('CHOOSE BOARD THEME', subText, (241, 249, 26), 250, 170)
    display_text('SOUND OPTIONS:', subText, (241, 249, 26), 100, 500)

    backImage = pygame.image.load('images/Back Image.png')
    confirmImage = pygame.image.load('images/Confirm.png') 
    soundOn = pygame.image.load('images/Sound on.png')
    soundOff = pygame.image.load('images/Sound off.png')
    resetImage = pygame.image.load('images/Reset.png')

    blueBoard = pygame.image.load('images/Blue Board.png')
    brownBoard = pygame.image.load('images/Brown Board.png')
    greenBoard = pygame.image.load('images/Green Board.png')

    #Initialises the buttons using an instance of the button class
    BlueBoardButton = Button(100, 250, blueBoard, 0.25)
    BrownBoardButton = Button(400, 250, brownBoard, 0.25)
    GreenBoardButton = Button(700, 250, greenBoard, 0.25)
    backButton = Button(10, 30, backImage, 0.2)
    soundOnButton = Button(480, 500, soundOn, 0.25)
    soundOffButton = Button(600, 500, soundOff, 0.25)
    resetButton = Button(100, 700, resetImage, 0.35)

    # Sets the border width, height and top left coordinates for each button
    blueBorder = pygame.Rect(100, 250, 186, 186)
    brownBorder = pygame.Rect(400, 250, 186, 186)
    greenBorder = pygame.Rect(700, 250, 186, 186)

    run = True
    while run:
        #Checks if the back button is clicked
        if backButton.create_button(gameWindow):
            targetMenu = 'main_menu'
            run = False

        #Checks if the blue board theme is selected 
        if BlueBoardButton.create_button(gameWindow):
            blue, brown, green = True, False, False # Sets the blue board button flag to true

        #Checks if the brown board theme is selected 
        if BrownBoardButton.create_button(gameWindow):
            blue, brown, green = False, True, False # Sets the brown board button flag to true

        #Checks if the green board theme is selected 
        if GreenBoardButton.create_button(gameWindow):
            blue, brown, green = False, False, True # Sets the green board button flag to true

        #Checks if the sound on button is selected 
        if soundOnButton.create_button(gameWindow):
            on, off = True, False # Sets the sound on button flag to true

        #Checks if the sound off button is selected 
        if soundOffButton.create_button(gameWindow):
            on, off = False, True # Sets the sound off button flag to true

        #Checks if the reset button is clicked
        if resetButton.create_button(gameWindow):
            # Deselects all previously selected options
            blue, brown, green = False, False, False 
            on, off = False, False
            
            #Redraws the screen again so it is completely reset
            gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
            display_text('GAME SETTINGS', mainText, (241, 249, 26), 100, 10)
            display_text('CHOOSE BOARD THEME', subText, (241, 249, 26), 250, 170)
            display_text('SOUND OPTIONS:', subText, (241, 249, 26), 100, 500)

        #Checks if the blue board flag is set to true
        if blue:
            pygame.draw.rect(gameWindow, (241, 249, 26), blueBorder, 4) #Draws the yellow border around the board theme
        #Checks if the brown board flag is set to true
        elif brown:
            pygame.draw.rect(gameWindow, (241, 249, 26), brownBorder, 4) #Draws the yellow border around the board theme
        #Checks if the green board flag is set to true
        elif green:
            pygame.draw.rect(gameWindow, (241, 249, 26), greenBorder, 4) #Draws the yellow border around the board theme

        # Checks if the sound on flag is set to true
        if on:
            pygame.draw.circle(gameWindow, (241, 249, 26), (512, 530), 32, 5) #Draws the yellow circle border around the sound option
        # Checks if the sound off flag is set to true
        elif off:
            pygame.draw.circle(gameWindow, (241, 249, 26), (632, 530), 32, 5)

        #This checks if one option from each sub heading has been selected and displays the confirm button if it is the case
        if (blue and on) or (blue and off) or (brown and on) or (brown and off) or (green and on) or (green and off):
            confirmButton = Button(700, 700, confirmImage, 0.5)
            #Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow): 
                targetMenu = 'game_mode'
                run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    #Responsible for directing the players to the correct menus
    if targetMenu == 'main_menu':
        main_menu()
    elif targetMenu == 'game_mode':
        game_mode()

def game_mode():
    targetMenu = None # Variable to keep track of which menu to go to
    bgImage = pygame.image.load('images/Mode Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    human, ai, back = False, False, False # Flags to set the selected game mode or back button

    # Displays the menu title
    display_text('MODE SELECTION', mainText, (241, 249, 26), 90, 10)

    backImage = pygame.image.load('images/Back Image.png')
    confirmImage = pygame.image.load('images/Confirm.png') 
    playHuman = pygame.image.load('images/Play Human.png')
    playAI = pygame.image.load('images/Play AI.png')

    # Initialises the buttons using an instance of the button class
    backButton = Button(10, 30, backImage, 0.2)
    humanButton = Button(100, 300, playHuman, 1.5)
    AIButton = Button(500, 298, playAI, 1.5)

    # Sets the border width, height and top left coordinates for each button
    humanBorder = pygame.Rect(100, 300, 382.5, 288)
    aiBorder = pygame.Rect(500, 298, 382.5, 291)
    backBorder = pygame.Rect(10, 30, 73, 42.8)

    run = True
    while run:
        # Checks if the back button is clicked
        if backButton.create_button(gameWindow):
            human, ai, back = False, False, True # Sets the back button flag to true

        # Checks if the play human button is clicked
        if humanButton.create_button(gameWindow):
            human, ai, back = True, False, False # Sets the play human button flag to true
 
        # Checks if the AI button is clicked
        if AIButton.create_button(gameWindow):
            human, ai, back = False, True, False # Sets the AI button flag to true

        # Checks if the human button flag is set to true
        if human:
            pygame.draw.rect(gameWindow, (241, 249, 26), humanBorder, 6) # Draws the yellow border around the play human button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            if confirmButton.create_button(gameWindow):
                targetMenu = 'human_timer_selection'
                run = False

        # Checks if the ai button flag is set to true
        elif ai:
            pygame.draw.rect(gameWindow, (241, 249, 26), aiBorder, 6) # Draws the yellow border around the play AI button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'difficulty_selection'
                run = False

        # Checks if the back button flag is set to true
        elif back:
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4) # Draws the yellow border around the back button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.create_button(gameWindow):
                targetMenu = 'settings'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    #Responsible for directing the players to the correct menus
    if targetMenu == 'settings':
        settings()
    elif targetMenu == 'human_timer_selection':
        timer_selection()
    elif targetMenu == 'difficulty_selection':
        difficulty_selection()

def main_menu():
    targetMenu = None
    bgImage = pygame.image.load('images/Bg Image.jpg')
    #Displays and scales the image as the background image of the game window.
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))

    display_text('MAIN MENU', mainText, (241, 249, 26), 240, 10)

    playImage = pygame.image.load('images/Play Button.png')
    quitImage = pygame.image.load('images/Quit button.png')

    #Uses the button class to create an instance of the play and quit button
    playButton = Button(385, 650, playImage, 0.5)
    quitButton = Button(930, 12, quitImage, 0.75)

    run = True
    while run:
        #Uses the create_button method in the button class to display the button on the screen and enable the click actions.
        if playButton.create_button(gameWindow):
            targetMenu = 'settings'
            #Once play is clicked, it exits the game loop
            run = False

        # Checks if the quit button is clicked
        if quitButton.create_button(gameWindow):
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Directs the players to the correct menus
    if targetMenu == 'settings':
        settings()

    pygame.quit()
    sys.exit()

main_menu()














