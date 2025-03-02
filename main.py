import pygame
import sys
import time
from copy import deepcopy
from chess.Button import Button
from chess.Constants import SQUARE_HEIGHT, SQUARE_WIDTH, GREEN, BLUE, BROWN, WHITE, BLACK, GREY
from chess.GameManager import Game
from chess.Board import Board
from chess.AI import EasyMode, MediumMode, HardMode

pygame.init() # Initialises all pygame's modules (i.e graphics, sound, etc.)
pygame.mixer.init() # Initialises pygame's sound module

gameWindow = pygame.display.set_mode((1000, 800))
gameIcon = pygame.image.load('images/king.png')
pygame.display.set_icon(gameIcon)
clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption('Chess')

mainText = pygame.font.SysFont('Arial', 120, bold=True) # Text used for all other menu headings
diffText = pygame.font.SysFont('Arial', 100, bold=True) # Text used for the difficulty menu heading
subText = pygame.font.SysFont('Arial', 50) # Text used for menu sub-headings
game = Game(gameWindow) # Holds an instance of the game class
board = Board() # Holds an instance of the board class

# Loads all the sounds 
checkSFX = pygame.mixer.Sound('Sounds/Check sound.mp3') # Sound for checks
whiteMoveSFX = pygame.mixer.Sound('Sounds/Player Move.mp3') # Sound for white making a move
blackMoveSFX = pygame.mixer.Sound('Sounds/Opp Move.mp3') # Sound for black making a move
gameEndSFX = pygame.mixer.Sound('Sounds/Game end.mp3') # Sound for when the game ends
lowTimeSFX = pygame.mixer.Sound('Sounds/Timer Sound.mp3') # Sound for when a player has less than 10 seconds

#Function that first converts the text into an image in order to allow it to be displayed on the screen
def DisplayText(text, font, colour, x, y):
    image = font.render(text, True, colour)
    gameWindow.blit(image, (x, y))

def SelectedRowColumn(mousePosition):
    x, y = mousePosition # Gets the x and y coordinate of the mouse position passed
    row = y // SQUARE_WIDTH # Determines the row by performing the correct division with the y coordinate
    column = x // SQUARE_HEIGHT # Determines the column by performing the correct division with the x coordinate
    return row, column

def Play(timer, boardColour, sound, difficulty):
    targetMenu = None # Variable to keep track of which menu to go to
    running = True
    checkSFXPlayed = False # Flag to track if the check sound effect has been played
    whiteSFXPlayed = False # Flag to track if the white move sound effect has been played
    blackSFXPlayed = False # Flag to track if the black moves sound effect has been played
    whiteTimePlayed = False # Flag to track if the white low time sound effect has been played
    blackTimePlayed = False # Flag to track if the black low time sound effect has been played

    TIMER_FONT = pygame.font.SysFont('Roboto Mono', 50)

    # Initialises timer values for white and black depending on the timer option choice from the timer selection menu
    whiteSeconds = timer * 60 # Converts to seconds becuase time from timer menu is given in minutes
    blackSeconds = timer * 60
    pygame.time.set_timer(pygame.USEREVENT, 1000) # Triggers a USEREVENT every 1000 milliseconds (i.e. 1 second)

    eventScheduled = False # Initialised to false so the AI can make its move when it is its turn
    AIMOVEMENT = pygame.USEREVENT + 1 # Creates a custom event for the AI moving
    TURNSWITCH = pygame.USEREVENT + 2 # Creates a custom event for the turns to switch after the AI makes a move.

    moves = [deepcopy(board)] # Stores the copy of the original board state so it can't be changed
    count = 1 # Variable to track the number of times the takeback button has been clicked
 
    # Checks if the AI was selected to play so it doesn't display the button if play human was selected.
    if difficulty != None:
        takeBackImage = pygame.image.load('images/Takeback.png')
        takeBackButton = Button(10, 700, takeBackImage, 1.2) # Displays the takeBackButton at its correct position

    while running:
        # Checks if the black king has been checkmated
        if game.Checkmate('Black'):
            # Checks if sound was selected to be on
            if sound == 'On':
                gameEndSFX.play() # PLays the game end sound effect
            targetMenu = 'White Checkmates'
            game.board = deepcopy(board) # Resets the board so it stores the original board state with all pieces on starting positions
            game.turn = 'White' # Resets the turn so white makes the first move
            game.moveHistory = [] # Resets the moveHistory list so it doesn't store moves played in a previous game that already ended
            running = False

        # Checks if the white king has been checkmated
        elif game.Checkmate('White'):
            # Checks if sound was selected to be on
            if sound == 'On':
                gameEndSFX.play() # PLays the game end sound effect
            targetMenu = 'Black Checkmates'
            game.board = deepcopy(board) # Resets the board so it stores the original board state with all pieces on starting positions
            game.turn = 'White' # Resets the turn so white makes the first move
            game.moveHistory = [] # Resets the moveHistory list so it doesn't store moves played in a previous game that already ended
            running = False

        # Checks if the current position is a stalemate
        if game.Stalemate():
            # Checks if sound was selected to be on
            if sound == 'On':
                gameEndSFX.play() # PLays the game end sound effect
            targetMenu = 'Stalemate'
            game.board = deepcopy(board) # Resets the board so it stores the original board state with all pieces on starting positions
            game.turn = 'White' # Resets the turn so white makes the first move
            game.moveHistory = [] # Resets the moveHistory list so it doesn't store moves played in a previous game that already ended
            running = False
            
        # Checks if the current position doesn't have enough pieces to deliver a checkmate
        if game.InsufficientMaterial():
            # Checks if sound was selected to be on
            if sound == 'On':
                gameEndSFX.play() # PLays the game end sound effect
            targetMenu = 'Insufficient Material'
            game.board = deepcopy(board) # Resets the board so it stores the original board state with all pieces on starting positions
            game.turn = 'White' # Resets the turn so white makes the first move
            game.moveHistory = [] # Resets the moveHistory list so it doesn't store moves played in a previous game that already ended
            running = False

        # Checks if white's time has run out but black only has a king left or vice versa
        if (whiteSeconds == 0 and len(game.PlayerPieces('Black')) == 0) or (blackSeconds == 0 and len(game.PlayerPieces('White')) == 0):
            targetMenu = 'Timeout vs Insufficient Material'
            game.board = deepcopy(board) # Resets the board so it stores the original board state with all pieces on starting positions
            game.turn = 'White' # Resets the turn so white makes the first move
            game.moveHistory = [] # Resets the moveHistory list so it doesn't store moves played in a previous game that already ended
            running = False

        # Checks if white's time has run out
        elif whiteSeconds == 0:
            targetMenu = 'White Timeout'
            game.board = deepcopy(board) # Resets the board so it stores the original board state with all pieces on starting positions
            game.turn = 'White' # Resets the turn so white makes the first move
            game.moveHistory = [] # Resets the moveHistory list so it doesn't store moves played in a previous game that already ended
            running = False

        # Checks if black's time has run out
        elif blackSeconds == 0:
            targetMenu = 'Black Timeout'
            game.board = deepcopy(board) # Resets the board so it stores the original board state with all pieces on starting positions
            game.turn = 'White' # Resets the turn so white makes the first move
            game.moveHistory = [] # Resets the moveHistory list so it doesn't store moves played in a previous game that already ended
            running = False

        # Checks if the sound parameter has value 'On' which would have been determined from the sound selection in the settings menu
        if sound == 'On':
            # Checks if a king is in check
            if game.InCheck(game.turn) != None and not checkSFXPlayed:
                checkSFX.play() # Plays the checks sound effect
                checkSFXPlayed = True # Set to true so it doesn't continue playing

            # Checks if a king is not in check
            elif game.InCheck(game.turn) == None:
                checkSFXPlayed = False # Resets the sound effect for 'checks' to false so it can be played again if in check again

            # Checks if it's white's turn and the king is not in check and the white move sound effect was not played previously
            if game.turn == 'White' and game.InCheck(game.turn) == None and not whiteSFXPlayed:
                whiteMoveSFX.play() # Plays the move sound effect for white
                whiteSFXPlayed = True # Sets to true so the sound effect doesn't continue playing
                blackSFXPlayed = False # Sets to false so sound effect can be played again when turns switch

            # Checks if it's black's turn and the king is not in check and the black move sound effect was not played previously
            elif game.turn == 'Black' and game.InCheck(game.turn) == None and not blackSFXPlayed:
                blackMoveSFX.play() # Plays the move sound effect for black
                blackSFXPlayed = True # Sets to true so the sound effect doesn't continue playing
                whiteSFXPlayed = False # Sets to false so sound effect can be played again when turns switch

            # Checks if the game has ended
            if game.TerminalCondition() or whiteSeconds == 0 or blackSeconds == 0:
                gameEndSFX.play() # Plays the game end sound effect

            # Checks if white has less than 10 seconds
            if whiteSeconds < 10 and not whiteTimePlayed:
                lowTimeSFX.play() # Plays the low time sound effect
                whiteTimePlayed = True # Prevents the sound effect from playing continuously

            # Checks if black has less than 10 seconds
            if blackSeconds < 10 and not blackTimePlayed:
                lowTimeSFX.play() # Plays the low time sound effect
                blackTimePlayed = True

        for event in pygame.event.get():
            # Checks if the X button to close the window has been clicked
            if event.type == pygame.QUIT:
                running = False # Exits the game loop

            # Checks if the mouse has been left clicked
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                mousePosition = pygame.mouse.get_pos() # Gets the current position of the mouse
                row, column = SelectedRowColumn(mousePosition) # Gets the row and column from the mouse's current position
                game.SelectSquare(row, column) # Calls the SelectSquare method to allow for piece selection and movement

            # Checks if a USEREVENT has been triggered
            if event.type == pygame.USEREVENT:
                # Checks if it is currently white's turn
                if game.turn == 'White':
                    # Makes white's time tick down by 1 each time a userevent is triggered (i.e every 1 second)
                    whiteSeconds -= 1
                else:
                    # Makes black' time tick down by 1 each time a userevent is triggered
                    blackSeconds -= 1

            # Checks if the event for the AI to move has been triggered
            if event.type == AIMOVEMENT:
                # Checks if it's black's turn
                if game.turn == 'Black':
                    if difficulty == 'Easy':
                        newBoard = EasyMode(game.GetBoard(), game) # Passes the board object and game class the AI easy mode function would use
                    elif difficulty == 'Medium':
                        newBoard = MediumMode(game.GetBoard(), game) # Passes the board object and game class the AI medium mode function would use
                    # Checks if the selected difficulty was hard and the AI has more than 10 seconds left
                    elif difficulty == 'Hard' and blackSeconds >= 10:
                        newBoard = HardMode(game.GetBoard(), game) # Passes the board object and game class the AI hard move function would use
                    # Checks if the selected difficulty was hard and the AI has less than 10 seconds left
                    elif difficulty == 'Hard' and blackSeconds < 10:
                        newBoard = EasyMode(game.GetBoard(), game) # Uses the easy mode function so it plays moves a lot faster

                    game.AIBoard(newBoard[0]) # Performs the visual movement as self.board is reassigned to the new board state
                    game.moveHistory.append(newBoard[1]) # Adds the associated move played to reach the new board state to the moveHistory list
                    moves.append(deepcopy(newBoard[0])) # Adds the copied board state after the AI has played its move to the moves list

                    pygame.event.post(pygame.event.Event(TURNSWITCH)) # Posts the turn switch event after the AI makes its move

            # Checks if the custom event TURNSWITCH has been triggered
            if event.type == TURNSWITCH:
                game.turn = 'White' # Switches the turns back to white so this way the AI isn't using my time
                eventScheduled = False # Sets to false so it can allow the AI to makes its move again once it is its turn

        # Checks if its the AI's turn and it hasn't made a move yet
        if game.turn == 'Black' and difficulty != None and not eventScheduled:
            pygame.time.set_timer(AIMOVEMENT, 500, True) # Triggers the event to make the AI move but delays it by 500 ms (0.5 seconds)
            eventScheduled = True # Sets to true so the AI doesn't make multiple moves at once

        # Checks if the AI was selected to play and the takeback has been clicked 3 times or less
        if difficulty != None and takeBackButton.Clicked(gameWindow) and count <= 3:
            count += 1
            # Checks if the list that stores all played moves has more than 1 left to prevent popping the original board state. 
            if len(moves) > 1:
                moves.pop() # Removes the previously added move
            previousBoard = moves[-1] # Stores the last board state after the previous one has been removed
            game.AIBoard(deepcopy(previousBoard)) # Reassigns self.board so it now holds copy of previous board state which is displayed
            # Removes the moves played by white and black once takeback is clicked so the moveHistory reflects the current board state
            game.moveHistory.pop() # Removes black's move
            game.moveHistory.pop() # Removes white's move

        # Draws the rectangles on which the timers would appear
        pygame.draw.rect(gameWindow, WHITE, (1, 375, 98, 50))
        pygame.draw.rect(gameWindow, BLACK, (901, 375, 98, 50))

        # Checks if white's time is greater than 0 to enusre it doesn't go into the negatives
        if whiteSeconds >= 0:
            whiteMinutes = whiteSeconds // 60 # The minute part in the timer
            whiteSecs = whiteSeconds % 60 # The seconds part in the timer
        # Responsible for converting the display into the correct format by using zero padding for seconds
        whiteTimerText = TIMER_FONT.render(f"{whiteMinutes}:{whiteSecs:02}", True, BLACK)
        whiteTimerRect = whiteTimerText.get_rect(center=(49, 400))
        gameWindow.blit(whiteTimerText, whiteTimerRect) # Displays white's timer onto the screen

        # Checks if black's time is greater than 0 to ensure it doesn't go into the negatives
        if blackSeconds >= 0:
            blackMinutes = blackSeconds // 60 # The minute part in the timer 
            blackSecs = blackSeconds % 60 # The seconds part in the timer
        # Responsible for converting the display into the correct format by using zero padding for seconds
        blackTimerText = TIMER_FONT.render(f"{blackMinutes}:{blackSecs:02}", True, WHITE)
        blackTimerRect = blackTimerText.get_rect(center=(949, 400))
        gameWindow.blit(blackTimerText, blackTimerRect) # Displays black's timer onto the screen

        pygame.display.update()
        game.UpdateScreen(boardColour) # Calls Update Screen with a board Colour parameter so the correct board theme is rendered
        clock.tick(fps)

    # Directs the players to the correct end screens depending on how the game ended
    if targetMenu == 'White Checkmates':
        EndScreen('Win', 'Checkmate', timer, sound, difficulty, boardColour, 'White')
    elif targetMenu == 'Black Checkmates':
        # Checks if the the player was playing the AI and the AI checkmated them
        if difficulty != None: 
            time.sleep(2) # Delays the end screen from loading in for 2 seconds to give the players enough time to see the checkmating move
        EndScreen('Win', 'Checkmate', timer, sound, difficulty, boardColour, 'Black')
    elif targetMenu == 'Stalemate':
        EndScreen('Draw', 'Stalemate', timer, sound, difficulty, boardColour)
    elif targetMenu == 'Insufficient Material':
        EndScreen('Draw', 'Insufficient Material', timer, sound, difficulty, boardColour)
    elif targetMenu == 'Timeout vs Insufficient Material':
        EndScreen('Draw', 'Timeout vs Insufficient Material', timer, sound, difficulty, boardColour)
    elif targetMenu == 'White Timeout':
        EndScreen('Win', 'Timeout', timer, sound, difficulty, boardColour, 'Black')
    elif targetMenu == 'Black Timeout':
        EndScreen('Win', 'Timeout', timer, sound, difficulty, boardColour, 'White')
        
def EndScreen(outcome, method, timer, sound, difficulty, boardColour, pieceColour=None):
    targetMenu = None # Variable to keep track of which menu to go to
    colourMapping = {'White': WHITE, 'Black': BLACK} # Maps the piece colour to a colour constant

    # Checks if a player won
    if outcome == 'Win':
        gameWindow.fill(GREEN)
        message = f'{pieceColour.upper()} WON!' # Stores message dynamically so if pieceColour was black, it would be BLACK WON! and vice versa
        subMessage = f'by {method}' # Stores the sub message dynamically similar to how the message variable works

        # Displays the end screen heading and sub headings which shows who won and how, respectively
        # and displays the text colour dynamically by using the correct mapping from the colourMapping dictionary
        DisplayText(message, mainText, colourMapping[pieceColour], 190, 50)
        DisplayText(subMessage, subText, colourMapping[pieceColour], 360, 180)

    # Checks if the game ended in a draw
    if outcome == 'Draw':
        gameWindow.fill(GREY)
        subMessage = f'by {method}'

        # Displays the end screen heading and sub headings which shows game drawn and how the game was drawn in white text
        DisplayText('GAME DRAWN!', mainText, WHITE, 140, 50)
        DisplayText(subMessage, subText, WHITE, 380, 180)

    main, rematch = False, False # Flags to set the selected button choice

    # Loads the button images
    homeImage = pygame.image.load('images/Main Menu.png')
    rematchImage = pygame.image.load('images/rematch.png')
    confirmImage = pygame.image.load('images/Confirm.png')

    # Initialises the buttons using an instance of the button class
    homeButton = Button(300, 450, homeImage, 2.5)
    rematchButton = Button(600, 450, rematchImage, 2.5)

    # Sets the border width, height and top left coordinates
    homeBorder = pygame.Rect(300, 450, 130, 130)
    rematchBorder = pygame.Rect(600, 450, 130, 130)

    run = True
    # Start of the game loop
    while run:
        # Check if the home button was clicked
        if homeButton.Clicked(gameWindow):
            main, rematch = True, False # Sets the main menu button flag to True

        # Checks if the rematch button was clicked
        if rematchButton.Clicked(gameWindow):
            main, rematch = False, True # Sets the rematch button flag to True

        # Checks if the main menu button flag is set to true to indicate the home button has been selected
        if main:
            pygame.draw.rect(gameWindow, (241, 249, 26), homeBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5) # Displays the confirm button
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Main Menu'
                run = False # Exits the game loop

        # Checks if the rematch button flag is set to true to indicate the rematch button has been selected
        elif rematch:
            pygame.draw.rect(gameWindow, (241, 249, 26), rematchBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5) # Displays the confirm button
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Play'
                run = False # Exits the game loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Exits the game loop

        pygame.display.update()
        clock.tick(fps)

    # Directs the player to the main menu
    if targetMenu == 'Main Menu':
        MainMenu()
    
    # Directs the player to the main game screen
    elif targetMenu == 'Play':
        Play(timer, boardColour, sound, difficulty)

def DifficultySelection(boardColour, sound):
    targetMenu = None # Variable to keep track of which menu to go to
    bgImage = pygame.image.load('images/Difficulty.png')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    easy, medium, hard, back = False, False, False, False # Flags to set the selected diffculty or back button

    # Displays the menu title
    DisplayText('SELECT DIFFICULTY', diffText, (241, 249, 26), 110, 10)

    # Loads the button images
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
    # Start of the game loop
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
                targetMenu = 'Game Mode'
                run = False

        # Checks if the easy button flag is true to indicate that the easy button has been selected
        elif easy:
            # Draws the yellow rectangle border around the easy button
            pygame.draw.rect(gameWindow, (241, 249, 26), easyBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Easy'
                run = False

        # Checks if the medium button flag is true to indicate that the medium button has been selected       
        elif medium:
            # Draws the yellow rectangle border around the medium button
            pygame.draw.rect(gameWindow, (241, 249, 26), mediumBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Medium'
                run = False

        # Checks if the hard button flag is true to indicate that the hard button has been selected
        elif hard:
            # Draws the yellow rectangle border around the hard button
            pygame.draw.rect(gameWindow, (241, 249, 26), hardBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Hard'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menus
    if targetMenu == 'Game Mode':
        GameMode(boardColour, sound)
    else:
        TimerSelection(boardColour, sound, targetMenu) # The target menu indicates the difficulty
    
def TimerSelection(boardColour, sound, difficulty=None):
    targetMenu = None # Variable to keep track of which menu to go to
    bgImage = pygame.image.load('images/Timer Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    timer1, timer3, timer5, timer10, back = False, False, False, False, False # Flags to set the selected timers and back button

    # Displays the menu title
    DisplayText('SELECT TIMER', mainText, (241, 249, 26), 140, 10)

    # Checks what difficulty was selected from the difficulty selection menu and displays the correct sub heading
    if difficulty == 'Easy':
        DisplayText('Difficulty: EASY', subText, (241, 249, 26), 140, 150)
    elif difficulty == 'Medium':
        DisplayText('Difficulty: MEDIUM', subText, (241, 249, 26), 140, 150)
    elif difficulty == 'Hard':
        DisplayText('Difficulty: HARD', subText, (241, 249, 26), 140, 150)

    # Loads the button images
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
    # Start of the game loop
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
                targetMenu = 1 # This would be used to indicate the time to be used
                run = False

        # Checks if the 3min button flag is set to true
        elif timer3:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer3Border, 4) #Draws the yellow border around the 3min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 3
                run = False

        # Checks if the 5min button flag is set to true
        elif timer5:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer5Border, 4) #Draws the yellow border around the 5min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 5
                run = False

        # Checks if the 10min button flag is set to true
        elif timer10:
            pygame.draw.rect(gameWindow, (241, 249, 26), timer10Border, 4) #Draws the yellow border around the 10min timer
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 10
                run = False
                
        # Checks if the back button flag is set to true and the player came from the game mode after clicking play human
        elif back and difficulty == None:
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Game Mode'
                run = False

        # Checks if the back button flag is set to true and the player came from the difficulty selection menu
        elif back and difficulty != None:
            pygame.draw.rect(gameWindow, (241, 249, 26), backBorder, 4)
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Difficulty Selection'
                run = False 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menus
    if targetMenu == 'Game Mode':
        GameMode(boardColour, sound)
    elif targetMenu == 'Difficulty Selection':
        DifficultySelection(boardColour, sound)
    elif difficulty != None:
        Play(targetMenu, boardColour, sound, difficulty) # The target menu indicates the time if it's not a string
    else:
        Play(targetMenu, boardColour, sound, None) # This is for a game when a human was selected to play

def GameMode(boardColour, sound):
    targetMenu = None # Variable to keep track of which menu to go to
    bgImage = pygame.image.load('images/Mode Image.jpg')
    # Displays and scales the background image so it fits the screen
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))
    human, ai, back = False, False, False # Flags to set the selected game mode or back button

    # Displays the menu title
    DisplayText('MODE SELECTION', mainText, (241, 249, 26), 90, 10)

    # Loads the button images
    backImage = pygame.image.load('images/Back Image.png')
    confirmImage = pygame.image.load('images/Confirm.png') 
    playHuman = pygame.image.load('images/Play Human.png')
    playAI = pygame.image.load('images/Play AI.png')

    # Initialises the buttons using an instance of the button class
    backButton = Button(10, 30, backImage, 0.2)
    humanButton = Button(100, 300, playHuman, 1.5)
    AIButton = Button(500, 298, playAI, 1.5)

    # Sets the border width, height and top left coordinates for each button
    humanButtonBorder = pygame.Rect(100, 300, 382.5, 288)
    aiButtonBorder = pygame.Rect(500, 298, 382.5, 291)
    backButtonBorder = pygame.Rect(10, 30, 73, 42.8)

    run = True
    # Start of the game loop
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
            pygame.draw.rect(gameWindow, (241, 249, 26), humanButtonBorder, 6) # Draws the yellow border around the play human button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Human Timer Selection'
                run = False

        # Checks if the ai button flag is set to true
        elif ai:
            pygame.draw.rect(gameWindow, (241, 249, 26), aiButtonBorder, 6) # Draws the yellow border around the play AI button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Difficulty Selection'
                run = False

        # Checks if the back button flag is set to true
        elif back:
            pygame.draw.rect(gameWindow, (241, 249, 26), backButtonBorder, 4) # Draws the yellow border around the back button
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow):
                targetMenu = 'Settings'
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menu
    if targetMenu == 'Settings':
        Settings()
    elif targetMenu == 'Human Timer Selection':
        TimerSelection(boardColour, sound)
    elif targetMenu == 'Difficulty Selection':
        DifficultySelection(boardColour, sound)

def Settings():
    targetMenu = None # Variable to track which menu to go to
    bgImage = pygame.image.load('images/Mode Image.jpg')
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0)) # Scales the background image to fit the screen
    blue, brown, green = False, False, False  # Flags to set the selected board colour
    on, off = False, False # Flags to set the selected sound option

    # Displays the menu title as well as the sub heading for the different settings
    DisplayText('GAME SETTINGS', mainText, (241, 249, 26), 100, 10)
    DisplayText('CHOOSE BOARD THEME', subText, (241, 249, 26), 250, 170)
    DisplayText('SOUND OPTIONS:', subText, (241, 249, 26), 100, 500)

    # Loads all the button images
    backImage = pygame.image.load('images/Back Image.png')
    confirmImage = pygame.image.load('images/Confirm.png') 
    soundOn = pygame.image.load('images/Sound on.png')
    soundOff = pygame.image.load('images/Sound off.png')

    # Loads all the board images
    blueBoard = pygame.image.load('images/Blue Board.png')
    brownBoard = pygame.image.load('images/Brown Board.png')
    greenBoard = pygame.image.load('images/Green Board.png')

    # Initialises the buttons using an instance of the button class
    blueBoardButton = Button(100, 250, blueBoard, 0.25)
    brownBoardButton = Button(400, 250, brownBoard, 0.25)
    greenBoardButton = Button(700, 250, greenBoard, 0.25)
    backButton = Button(10, 30, backImage, 0.2)
    soundOnButton = Button(480, 500, soundOn, 0.25)
    soundOffButton = Button(600, 500, soundOff, 0.25)

    # Sets the border width, height and top left coordinates for each button
    blueBorder = pygame.Rect(100, 250, 186, 186)
    brownBorder = pygame.Rect(400, 250, 186, 186)
    greenBorder = pygame.Rect(700, 250, 186, 186)

    run = True
    # The start if the game loop
    while run:
        # Checks if the back button is clicked
        if backButton.Clicked(gameWindow):
            targetMenu = 'Main Menu'
            run = False

        # Checks if the blue board theme is clicked 
        if blueBoardButton.Clicked(gameWindow):
            blue, brown, green = True, False, False # Sets the blue board button flag to true

        # Checks if the brown board theme is clicked 
        if brownBoardButton.Clicked(gameWindow):
            blue, brown, green = False, True, False # Sets the brown board button flag to true

        # Checks if the green board theme is clicked 
        if greenBoardButton.Clicked(gameWindow):
            blue, brown, green = False, False, True # Sets the green board button flag to true

        # Checks if the sound on button is clicked 
        if soundOnButton.Clicked(gameWindow):
            on, off = True, False # Sets the sound on button flag to true

        # Checks if the sound off button is clicked 
        if soundOffButton.Clicked(gameWindow):
            on, off = False, True # Sets the sound off button flag to true

        # Checks if the blue board flag is set to true
        if blue:
            pygame.draw.rect(gameWindow, (241, 249, 26), blueBorder, 4) # Draws the yellow border around the board theme
        # Checks if the brown board flag is set to true
        elif brown:
            pygame.draw.rect(gameWindow, (241, 249, 26), brownBorder, 4) # Draws the yellow border around the board theme
        # Checks if the green board flag is set to true
        elif green:
            pygame.draw.rect(gameWindow, (241, 249, 26), greenBorder, 4) # Draws the yellow border around the board theme

        # Checks if the sound on flag is set to true
        if on:
            pygame.draw.circle(gameWindow, (241, 249, 26), (512, 530), 32, 5) # Draws the yellow circle border around the sound on option
        # Checks if the sound off flag is set to true
        elif off:
            pygame.draw.circle(gameWindow, (241, 249, 26), (632, 530), 32, 5) # Draws the yellow circle border around the sound off option

        # This checks if the blue board theme AND the sound on option has been selected
        if blue and on:
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = (BLUE, 'On') # Assigns to target menu a tuple which indicates the board colour constant and a string for on/off
                run = False

        # This checks if the brown board theme AND the sound on option has been selected
        elif brown and on:
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = (BROWN, 'On') # Assigns to target menu a tuple which indicates the board colour constant and a string for on/off
                run = False

        # This checks if the green board theme AND the sound on option has been selected
        elif green and on:
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = (GREEN, 'On') # Assigns to target menu a tuple which indicates the board colour constant and a string for on/off
                run = False

        # This checks if the blue board theme AND the sound off option has been selected
        elif blue and off:
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = (BLUE, 'Off')  # Assigns to target menu a tuple which indicates the board colour constant and a string for on/off
                run = False

        # This checks if the brown board theme AND the sound off option has been selected
        elif brown and off:
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = (BROWN, 'Off') # Assigns to target menu a tuple which indicates the board colour constant and a string for on/off
                run = False

        # This checks if the green board theme AND the sound off option has been selected
        elif green and off:
            confirmButton = Button(700, 700, confirmImage, 0.5)
            # Checks if the confirm button is clicked
            if confirmButton.Clicked(gameWindow): 
                targetMenu = (GREEN, 'Off') # Assigns to target menu a tuple which indicates the board colour constant and a string for on/off
                run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(fps)

    # Responsible for directing the players to the correct menus
    if targetMenu == 'Main Menu':
        MainMenu()
    else:
        GameMode(targetMenu[0], targetMenu[1])

def MainMenu():
    targetMenu = None
    bgImage = pygame.image.load('images/Bg Image.jpg')
    #Displays and scales the image as the background image of the game window.
    gameWindow.blit(pygame.transform.scale(bgImage, (1000, 800)), (0, 0))

    # Displays the MAIN MENU heading onto the screen
    DisplayText('MAIN MENU', mainText, (241, 249, 26), 240, 10)

    # Loads the button images
    playImage = pygame.image.load('images/Play Button.png')
    quitImage = pygame.image.load('images/Quit button.png')

    #Uses the button class to create an instance of the play and quit button
    playButton = Button(385, 650, playImage, 0.5)
    quitButton = Button(930, 12, quitImage, 0.75)

    run = True
    while run:
        # Uses the Clicked method in the button class to display the button on the screen and enable the click actions.
        if playButton.Clicked(gameWindow):
            targetMenu = 'Settings'
            # Once play is clicked, it exits the game loop
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
    if targetMenu == 'Settings':
        Settings()

    pygame.quit()
    sys.exit()

MainMenu()
