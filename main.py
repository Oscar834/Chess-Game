import pygame
import sys
from chess.Button import Button
from chess.Constants import SQUARE_HEIGHT, SQUARE_WIDTH, WHITE, GREEN, BLACK, GREY, BLUE, BROWN 
from chess.GameManager import Game
from chess.Board import Board
from chess.AI import Minimax
from copy import deepcopy

pygame.init()
pygame.mixer.init()

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
board = Board()

checkSFX = pygame.mixer.Sound('Sounds/Check sound.mp3')
playerMoveSFX = pygame.mixer.Sound('Sounds/Player Move.mp3')
oppMoveSFX = pygame.mixer.Sound('Sounds/Opp Move.mp3')
gameEndSFX = pygame.mixer.Sound('Sounds/Game end.mp3')
lowTimeSFX = pygame.mixer.Sound('Sounds/Timer Sound.mp3')
castleSFX = pygame.mixer.Sound('Sounds/Castle sound.mp3')
takeImage = pygame.image.load('images/Takeback.png')
takeBackButton = Button(10, 700, takeImage, 1.2)

#Function that first converts the text into an image in order to allow it to be displayed on the screen
def DisplayText(text, font, color, x, y):
    image = font.render(text, True, color)
    gameWindow.blit(image, (x, y))

#This function gets the current row and column from the position of the mouse on the screen
def SelectedRowColumn(mousePosition):
    x, y = mousePosition
    row = y // SQUARE_WIDTH
    column = x // SQUARE_HEIGHT
    return row, column

def Play(time, difficulty=None, colour=None):
    running = True
    FONT = pygame.font.SysFont('Roboto Mono', 50)
    targetMenu = None
    boardColour = None
    checkSFXPlayed = False
    playerMoveSFXPlayed = False
    oppMoveSFXPlayed = False
    wtimeSFXPlayed = False
    btimeSFXPlayed = False

    if colour == 'blue':
        boardColour = BLUE

    elif colour == 'brown':
        boardColour = BROWN

    elif colour == 'green':
        boardColour = GREEN

    # Initialises timer values for white and black depending on the timer option chosing in the timer selection menu
    whiteSeconds = time * 60
    blackSeconds = time * 60
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    moves = [deepcopy(board)]
    count = 1
    while running:
        if game.turn == 'Black' and difficulty == 'Easy':
            newBoard = Minimax(game.GetBoard(), 0, False, game, 'Easy', float('-inf'), float('inf'))
            game.AIMovement(newBoard)
            moves.append(deepcopy(newBoard))

        if game.turn == 'Black' and difficulty == 'Medium':
            value, newBoard = Minimax(game.GetBoard(), 1, False, game, 'Medium', float('-inf'), float('inf'))
            game.AIMovement(newBoard)
            print(value)
            moves.append(deepcopy(newBoard))

        if game.turn == 'Black' and difficulty == 'Hard':
            newBoard = Minimax(game.GetBoard(), 0, False, game, 'Hard', float('-inf'), float('inf'))
            game.AIMovement(newBoard)
            moves.append(deepcopy(newBoard))

        if takeBackButton.Clicked(gameWindow) and (difficulty == 'Medium' or difficulty == 'Easy' or difficulty == 'Hard') and count <= 3:
            count += 1
            if len(moves) > 1:
                moves.pop()
            actualBoard = moves[-1]
            game.AIBoard(deepcopy(actualBoard))

        if game.InCheck(game.turn) != None and not checkSFXPlayed:
            checkSFX.play()
            checkSFXPlayed = True

        elif game.InCheck(game.turn) == None: #Error
            checkSFXPlayed = False

        if game.turn == 'White' and not playerMoveSFXPlayed and game.InCheck(game.turn) == None:
            playerMoveSFX.play()
            playerMoveSFXPlayed = True
            oppMoveSFXPlayed = False

        elif game.turn == 'Black' and not oppMoveSFXPlayed and game.InCheck(game.turn) == None:
            oppMoveSFX.play()
            oppMoveSFXPlayed = True
            playerMoveSFXPlayed = False

        if whiteSeconds < 10 and not wtimeSFXPlayed:
            lowTimeSFX.play()
            wtimeSFXPlayed = True

        if blackSeconds < 10 and not btimeSFXPlayed:
            lowTimeSFX.play()
            btimeSFXPlayed = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Checks where the mouse button is clicked and uses it to determine the
            #row and column from the mouse position
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                row, column = SelectedRowColumn(mousePosition)
                #This method from the Game class is called here and is responsible for
                #the selection of squares which include selecting the piece and moving it to a square.
                game.SelectSquare(row, column)
                
            elif event.type == pygame.USEREVENT:
                # Checks if it is currently white's turn
                if game.turn == 'White':
                    # Makes white's time tick down
                    whiteSeconds -= 1
                # Checks if it is currently black's turn
                elif game.turn == 'Black':
                    # Makes black' time tick down
                    blackSeconds -= 1

        if game.Checkmate('Black'):
            gameEndSFX.play()
            targetMenu = 'White Checkmate'
            running = False
        elif game.Checkmate('White'):
            gameEndSFX.play()
            targetMenu = 'Black Checkmate'
            running = False
        elif game.Stalemate():
            gameEndSFX.play()
            targetMenu = 'Stalemate'
            running = False
        elif game.InsufficientMaterial():
            gameEndSFX.play()
            targetMenu = 'Insufficient Material'
            running = False
        elif whiteSeconds == 0:
            gameEndSFX.play()
            targetMenu = 'Black win time'
            running = False
        elif blackSeconds == 0:
            gameEndSFX.play()
            targetMenu = 'White win time'
            running = False
    
        # Draws the rectangles on which the timers would appear
        pygame.draw.rect(gameWindow, WHITE, (1, 375, 98, 50))
        pygame.draw.rect(gameWindow, BLACK, (901, 375, 98, 50))

        # Displays white's timer
        if whiteSeconds >= 0:
            whiteMinutes = whiteSeconds // 60
            whiteSecs = whiteSeconds % 60
        # Responsible for converting the display into the correct format by using zero padding for seconds
        whiteTimerText = FONT.render(f"{whiteMinutes}:{whiteSecs:02}", True, BLACK)
        whiteTimerRect = whiteTimerText.get_rect(center=(49, 400))
        gameWindow.blit(whiteTimerText, whiteTimerRect)

        # Displays black's timer
        if blackSeconds >= 0:
            blackMinutes = blackSeconds // 60
            blackSecs = blackSeconds % 60
        #Responsible for converting the display into the correct format by using zero padding for seconds
        blackTimerText = FONT.render(f"{blackMinutes}:{blackSecs:02}", True, WHITE)
        blackTimerRect = blackTimerText.get_rect(center=(949, 400))
        gameWindow.blit(blackTimerText, blackTimerRect)

        pygame.display.flip()
        game.UpdateScreen(boardColour)
        clock.tick(fps)

    if targetMenu == 'White Checkmate':
        GameResult('win', 'Checkmate', time, 'White')
    elif targetMenu == 'Black Checkmate':
        GameResult('win', 'Checkmate', time, 'Black')
    elif targetMenu == 'Stalemate':
        GameResult('draw', 'Stalemate', time)
    elif targetMenu == 'Insufficient Material':
        GameResult('draw', 'Insufficient Material', time)
    elif targetMenu == 'Black win time':
        GameResult('win', 'Timeout', time, 'Black')
    elif targetMenu == 'White win time':
        GameResult('win', 'Timeout', time, 'White')
        
def GameResult(outcome, method, time, pieceColour=None, boardColour=None):
    targetMenu = None
    if outcome == 'win' and method == 'Checkmate' and pieceColour == 'White':
        gameWindow.fill(GREEN)
        DisplayText('WHITE WON!', mainText, WHITE, 190, 50)
        DisplayText('by checkmate', subText, WHITE, 360, 180)

    if outcome == 'win' and method == 'Checkmate' and pieceColour == 'Black':
        gameWindow.fill(GREEN)
        DisplayText('BLACK WON!', mainText, BLACK, 190, 50)
        DisplayText('by checkmate', subText, BLACK, 360, 180)

    if outcome == 'win' and method == 'Timeout' and pieceColour == 'White':
        gameWindow.fill(GREEN)
        DisplayText('WHITE WON!', mainText, WHITE, 190, 50)
        DisplayText('by timeout', subText, WHITE, 390, 180)

    if outcome == 'win' and method == 'Timeout' and pieceColour == 'Black':
        gameWindow.fill(GREEN)
        DisplayText('BLACK WON!', mainText, BLACK, 190, 50)
        DisplayText('by timeout', subText, BLACK, 390, 180)

    if outcome == 'draw' and method == 'Stalemate':
        gameWindow.fill(GREY)
        DisplayText('GAME DRAWN!', mainText, WHITE, 140, 50)
        DisplayText('by stalemate', subText, WHITE, 380, 180)

    if outcome == 'draw' and method == 'Insufficient Material':
        gameWindow.fill(GREY)
        DisplayText('GAME DRAWN!', mainText, WHITE, 140, 50)
        DisplayText('by insufficient material', subText, WHITE, 380, 180)

    main, rematch = False, False

    homeImage = pygame.image.load('images/Main Menu.png')
    rematchImage = pygame.image.load('images/rematch.png')
    confirmImage = pygame.image.load('images/Confirm.png')

    homeButton = Button(300, 450, homeImage, 2.5)
    rematchButton = Button(600, 450, rematchImage, 2.5)

    homeBorder = pygame.Rect(300, 450, 130, 130)
    rematchBorder = pygame.Rect(600, 450, 130, 130)

    if boardColour == 'blue':
        colour = BLUE
    elif boardColour == 'brown':
        colour = BROWN
    elif boardColour == 'green':
        colour = GREEN

    run = True
    while run:
        if homeButton.Clicked(gameWindow):
            main, rematch = True, False

        if rematchButton.Clicked(gameWindow):
            main, rematch = False, True

        if main:
            pygame.draw.rect(gameWindow, (241, 249, 26), homeBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'main menu'
                run = False
        elif rematch:
            pygame.draw.rect(gameWindow, (241, 249, 26), rematchBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'play'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    if targetMenu == 'main menu':
        MainMenu()
    elif targetMenu == 'play':
        Play(time, None, time, None, colour)

def DifficultySelection(colour=None):
    targetMenu = None
    bgImage = pygame.image.load('images/Difficulty.png')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    easy, medium, hard, back = False, False, False, False # Flags to set the selected diffculty or back button

    #Displays the menu title
    DisplayText('SELECT DIFFICULTY', diffText, (241, 249, 26), 110, 10)

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
        if backButton.Clicked(gameWindow):
            easy, medium, hard, back = False, False, False, True # Sets the back button flag to true

        # Checks if the easy button is clicked
        if easyButton.Clicked(gameWindow):
            easy, medium, hard, back = True, False, False, False # Sets the easy button flag to true 

        # Checks if the medium button is clicked
        if mediumButton.Clicked(gameWindow):
            easy, medium, hard, back = False, True, False, False # Sets the medium button flag to true

        # Checks if the hard button is clicked
        if hardButton.Clicked(gameWindow):
            easy, medium, hard, back = False, False, True, False # Sets the hard button flag to true

        # Checks if the back button flag is true to indicate that the back button has been selected
        if back:
            # Draws the yellow rectangle border around the back button
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            # Confirm button only dispplayed once a button has been clicked
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button has been clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'game mode'
                run = False

        # Checks if the easy button flag is true to indicate that the easy button has been selected
        elif easy:
            # Draws the yellow rectangle border around the easy button
            pygame.draw.rect(gameWindow, (241, 249, 26), easyBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Easy_AI_timer'
                run = False

        # Checks if the medium button flag is true to indicate that the medium button has been selected       
        elif medium:
            # Draws the yellow rectangle border around the medium button
            pygame.draw.rect(gameWindow, (241, 249, 26), mediumBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Medium_AI_timer'
                run = False

        # Checks if the hard button flag is true to indicate that the hard button has been selected
        elif hard:
            # Draws the yellow rectangle border around the hard button
            pygame.draw.rect(gameWindow, (241, 249, 26), hardBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Hard_AI_timer'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menus
    if targetMenu == 'game mode':
        GameMode(colour)
    elif targetMenu == 'Easy_AI_timer':
        TimerSelection(colour, 'Easy')
    elif targetMenu == 'Medium_AI_timer':
        TimerSelection(colour, 'Medium')
    elif targetMenu == 'Hard_AI_timer':
        TimerSelection(colour, 'Hard')
    
def TimerSelection(colour=None, difficulty=None):
    targetMenu = None
    bgImage = pygame.image.load('images/Timer Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    timer1, timer3, timer5, timer10, back = False, False, False, False, False # Flags to set the selected diffculty or back button

    # Displays the menu title
    DisplayText('SELECT TIMER', mainText, (241, 249, 26), 140, 10)

    # Checks what difficulty was selected from the difficulty selection menu and displays the correct sub heading
    if difficulty == 'Easy':
        DisplayText('Difficulty: EASY', subText, (241, 249, 26), 140, 150)
    elif difficulty == 'Medium':
        DisplayText('Difficulty: MEDIUM', subText, (241, 249, 26), 140, 150)
    elif difficulty == 'Hard':
        DisplayText('Difficulty: HARD', subText, (241, 249, 26), 140, 150)

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
        if backButton.Clicked(gameWindow):
            timer1, timer3, timer5, timer10, back = False, False, False, False, True # Sets the back button flag to true

        # Checks if the 1min timer button is clicked
        if timer1Button.Clicked(gameWindow):
            timer1, timer3, timer5, timer10, back = True, False, False, False, False # Sets the 1min timer button flag to true

        # Checks if the 3min timer button is clicked
        if timer3Button.Clicked(gameWindow):
            timer1, timer3, timer5, timer10, back = False, True, False, False, False # Sets the 3min timer button flag to true

        # Checks if the 5min timer button is clicked
        if timer5Button.Clicked(gameWindow):
            timer1, timer3, timer5, timer10, back = False, False, True, False, False # Sets the 5min timer button flag to true

        # Checks if the 10min timer button is clicked
        if timer10Button.Clicked(gameWindow):
            timer1, timer3, timer5, timer10, back = False, False, False, True, False # Sets the 10min timer button flag to true

        # Checks if the 1min button flag is set to true
        if timer1:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer1Border, 4) #Draws the yellow border around the 1min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'play 1min'
                run = False

        # Checks if the 3min button flag is set to true
        elif timer3:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer3Border, 4) #Draws the yellow border around the 3min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'play 3min'
                run = False

        # Checks if the 5min button flag is set to true
        elif timer5:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer5Border, 4) #Draws the yellow border around the 5min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'play 5min'
                run = False

        # Checks if the 10min button flag is set to true
        elif timer10:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer10Border, 4) #Draws the yellow border around the 10min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'play 10min'
                run = False
                
        # Checks if the back button flag is set to true and the player came from the game mode after clicking play human
        elif back and difficulty == None:
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'game mode'
                run = False

        # Checks if the back button flag is set to true and the player came from the difficulty selection menu
        elif back and (difficulty == 'Easy' or difficulty == 'Medium' or difficulty == 'Hard'):
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'difficulty selection'
                run = False 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menus
    if targetMenu == 'game mode':
        GameMode(colour)
    elif targetMenu == 'difficulty selection':
        DifficultySelection(colour)
    elif targetMenu == 'play 1min' and difficulty == 'Easy':
        Play(1, 'Easy', colour)
    elif targetMenu == 'play 3min' and difficulty == 'Easy':
        Play(3, 'Easy', colour)
    elif targetMenu == 'play 5min' and difficulty == 'Easy':
        Play(5, 'Easy', colour)
    elif targetMenu == 'play 10min' and difficulty == 'Easy':
        Play(10, 'Easy', colour)
    elif targetMenu == 'play 1min' and difficulty == 'Medium':
        Play(1, 'Medium', colour)
    elif targetMenu == 'play 3min' and difficulty == 'Medium':
        Play(3, 'Medium', colour)
    elif targetMenu == 'play 5min' and difficulty == 'Medium':
        Play(5, 'Medium', colour)
    elif targetMenu == 'play 10min' and difficulty == 'Medium':
        Play(10, 'Medium', colour)
    elif targetMenu == 'play 1min' and difficulty == 'Hard':
        Play(1, 'Hard', colour)
    elif targetMenu == 'play 3min' and difficulty == 'Hard':
        Play(3, 'Hard', colour)
    elif targetMenu == 'play 5min' and difficulty == 'Hard':
        Play(5, 'Hard', colour)
    elif targetMenu == 'play 10min' and difficulty == 'Hard':
        Play(10, 'Hard', colour)
    elif targetMenu == 'play 1min':
        Play(1, None, colour)
    elif targetMenu == 'play 3min':
        Play(3, None, colour)
    elif targetMenu == 'play 5min':
        Play(5, None, colour)
    elif targetMenu == 'play 10min':
        Play(10, None, colour)

def Settings():
    targetMenu = None
    bgImage = pygame.image.load('images/Mode Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    blue, brown, green = False, False, False  # Flags to set the selected board colour
    on, off = False, False # Flags to set the selected sound option

    # Displays the menu title as well as the sub heading for the different settings
    DisplayText('GAME SETTINGS', mainText, (241, 249, 26), 100, 10)
    DisplayText('CHOOSE BOARD THEME', subText, (241, 249, 26), 250, 170)
    DisplayText('SOUND OPTIONS:', subText, (241, 249, 26), 100, 500)

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
        if backButton.Clicked(gameWindow):
            targetMenu = 'main menu'
            run = False

        #Checks if the blue board theme is selected 
        if BlueBoardButton.Clicked(gameWindow):
            blue, brown, green = True, False, False # Sets the blue board button flag to true

        #Checks if the brown board theme is selected 
        if BrownBoardButton.Clicked(gameWindow):
            blue, brown, green = False, True, False # Sets the brown board button flag to true

        #Checks if the green board theme is selected 
        if GreenBoardButton.Clicked(gameWindow):
            blue, brown, green = False, False, True # Sets the green board button flag to true

        #Checks if the sound on button is selected 
        if soundOnButton.Clicked(gameWindow):
            on, off = True, False # Sets the sound on button flag to true

        #Checks if the sound off button is selected 
        if soundOffButton.Clicked(gameWindow):
            on, off = False, True # Sets the sound off button flag to true

        #Checks if the reset button is clicked
        if resetButton.Clicked(gameWindow):
            # Deselects all previously selected options
            blue, brown, green = False, False, False 
            on, off = False, False
            
            #Redraws the screen again so it is completely reset
            gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
            DisplayText('GAME SETTINGS', mainText, (241, 249, 26), 100, 10)
            DisplayText('CHOOSE BOARD THEME', subText, (241, 249, 26), 250, 170)
            DisplayText('SOUND OPTIONS:', subText, (241, 249, 26), 100, 500)

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
        if (blue and on) or (blue and off):
            confirmButton = Button(700, 700, confirmImage, 0.5)
            #Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = 'blue game mode'
                run = False

        elif (brown and on) or (brown and off):
            confirmButton = Button(700, 700, confirmImage, 0.5)
            #Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = 'brown game mode'
                run = False

        elif (green and on) or (green and off):
            confirmButton = Button(700, 700, confirmImage, 0.5)
            #Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = 'green game mode'
                run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    #Responsible for directing the players to the correct menus
    if targetMenu == 'main menu':
        MainMenu()
    elif targetMenu == 'blue game mode':
        GameMode('blue')
    elif targetMenu == 'brown game mode':
        GameMode('brown')
    elif targetMenu == 'green game mode':
        GameMode('green')

def GameMode(colour=None):
    targetMenu = None # Variable to keep track of which menu to go to
    bgImage = pygame.image.load('images/Mode Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    human, ai, back = False, False, False # Flags to set the selected game mode or back button

    # Displays the menu title
    DisplayText('MODE SELECTION', mainText, (241, 249, 26), 90, 10)

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
        if backButton.Clicked(gameWindow):
            human, ai, back = False, False, True # Sets the back button flag to true

        # Checks if the play human button is clicked
        if humanButton.Clicked(gameWindow):
            human, ai, back = True, False, False # Sets the play human button flag to true
 
        # Checks if the AI button is clicked
        if AIButton.Clicked(gameWindow):
            human, ai, back = False, True, False # Sets the AI button flag to true

        # Checks if the human button flag is set to true
        if human:
            pygame.draw.rect(gameWindow, (241, 249, 26), humanBorder, 6) # Draws the yellow border around the play human button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'human_timer_selection'
                run = False

        # Checks if the ai button flag is set to true
        elif ai:
            pygame.draw.rect(gameWindow, (241, 249, 26), aiBorder, 6) # Draws the yellow border around the play AI button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'difficulty selection'
                run = False

        # Checks if the back button flag is set to true
        elif back:
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4) # Draws the yellow border around the back button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'settings'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    #Responsible for directing the players to the correct menus
    if targetMenu == 'settings':
        Settings()
    elif targetMenu == 'human_timer_selection':
        TimerSelection(colour)
    elif targetMenu == 'difficulty selection':
        DifficultySelection(colour)

def MainMenu():
    targetMenu = None
    bgImage = pygame.image.load('images/Bg Image.jpg')
    #Displays and scales the image as the background image of the game window.
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))

    DisplayText('MAIN MENU', mainText, (241, 249, 26), 240, 10)

    playImage = pygame.image.load('images/Play Button.png')
    quitImage = pygame.image.load('images/Quit button.png')

    #Uses the button class to create an instance of the play and quit button
    playButton = Button(385, 650, playImage, 0.5)
    quitButton = Button(930, 12, quitImage, 0.75)

    run = True
    while run:
        #Uses the Clicked method in the button class to display the button on the screen and enable the click actions.
        if playButton.Clicked(gameWindow):
            targetMenu = 'settings'
            #Once play is clicked, it exits the game loop
            run = False

        # Checks if the quit button is clicked
        if quitButton.Clicked(gameWindow):
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Directs the players to the correct menus
    if targetMenu == 'settings':
        Settings()

    pygame.quit()
    sys.exit()

MainMenu()














