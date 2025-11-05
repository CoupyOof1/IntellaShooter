#region Libraries
import pygame
import sys
import random

#      IMPORTING OTHER FILES
from Datas import * 
from Entity import *
#endregion

#      INTIALISING PYGAME
pygame.init()

#      UPDATING SCREEN
#region updating screen function

def screens_updating():
    # - This will be a function that constantly updates and changes the current screen depending on it events
    global GAME_EVENTS # Extracting a variable for determine what screen should be drawn

    screen.fill((0, 0, 0)) # Clearing screen

    #      (MAPED EVENTS AND IT LINKED FUNCTIONS)
    # - Creating a dictionary for mapping event names to the function they handle
    screen_handler = {
        "SCRN_MENU": drawing_menu,
        "SCRN_LEVEL": drawing_Level,
        "SCRN_GAME": drawing_gameplay,
        "SCRN_OVER": drawing_gameplay_over
    }

    #      (EVENT HANDLING)
    # - Handles the event and switches screen according to the event current name
    if GAME_EVENTS in screen_handler:
        screen_handler[GAME_EVENTS]() # Calling the mapped function corresponding to the event name
    else:
        print(f"Unknown event: {GAME_EVENTS}")

#endregion 

#region Drawing screens

#      MENU SCREEN
def drawing_menu(): 
    # - A function for drawing the menu for the game
    screen.fill((0, 0, 0)) # Clearing the screen 

    #      (DRAWING TEXT ON SCREEN)
    UI.draw_text("IntellaShooters", 600, 105, 90, WHITE, SPACELINE)

    #      (MAKING BUTTONS VISIBLE)
    for button in [BTN_MENU_START]:
        button.update(screen)
        button.changeColor(pygame.mouse.get_pos())

#      GAME OVER SCREEN
def drawing_gameplay_over():
    global RESULT_STATE

    # - A function for drawing the game over screen
    screen.fill((0, 0, 0)) # Clearing the screen 

    #      (DRAWING TEXT ON SCREEN)
    UI.draw_text("GAME OVER", 600, 105, 90, WHITE, SPACELINE)

    #      (ANSWER VALIDATION)
    # - This code will give responsive feedback determining on the user selection of asnwer
    if RESULT_STATE == "CORRECT":
        UI.draw_text("CORRECT", 600, 300, 60, GREEN, SPACELINE)
    else:
        UI.draw_text("INCORRECT", 600, 300, 60, RED, SPACELINE)

#     LEVELS SCREEN 
def drawing_Level(): 
    global GAME_EVENTS, GAMEPLAY_MODE, CURRENT_QUESTION

    # - A function for drawing the menu for the game
    screen.fill((0, 0, 0))

    #     (DRAWIGN TEXT ON SCREEN)
    UI.draw_text("SELECT DIFFICULTY", 600, 75, 55, WHITE, SPACELINE)

    #     (UPDATING PLAYER MOVMENT)
    # - Retrieving player input and turning it into actions
    keys = pygame.key.get_pressed()
    player.movement(keys)

    #     (DRAWING PLAYER)
    player.draw(screen)

    #      (DEFINING DIFFICULTIES)
    # - Creating a List for the difficulties and it correspondong event name and y positoning on screen
    # - Label Name, Y-Position, Event Name, Gameplay Mode
    DIFFICULTIES = [
        ("EASY", 140, "SCRN_GAME", "GM_EASY"), 
        ("NORM", 300, "SCRN_GAME", "GM_NORM"),
        ("HARD", 460, "SCRN_GAME", "GM_HARD"),
    ]

    #      (LOOPING THROUGH ALL DIFFICULTIES)
    # - Loop through and draws all difficulty boxes fynamically 
    for label, y, event_name, game_mode in DIFFICULTIES:
        rect = pygame.Rect(500, y, 200, 100)                                  # Creating a rectangle box
        pygame.draw.rect(screen, BLUE, rect)                                  # Drawing the box itself
        UI.draw_text(label, rect.centerx, rect.centery, 35, WHITE, SPACELINE) # Draws the labels

        #      [CHECKING COLLISIONS]
        # - Checks the collisions between the projectile and the box
        for proj in player.projectiles:
            if proj.rect.colliderect(rect):
                GAME_EVENTS = event_name  # Changes to the approproiate game screen according difficultly selected
                GAMEPLAY_MODE = game_mode # Changes to the appropriate difficultly 
                proj.kill()               # Removes the projectile after collision 
                
                #     <PICKING RANDOM QUESTION>
                # - Pickign a random question from the question data
                CURRENT_QUESTION = random.choice(QUESTIONS_LIST)

                break # Exiting the projectile loop

#     GAMEPLAY SCREEN 
def drawing_gameplay():
    global CURRENT_QUESTION, GAME_EVENTS, GAMEPLAY_MODE, RESULT_STATE, CURRENT_TIME, MAX_TIMER, ACTIVE_TIMER
    screen.fill((0, 0, 0)) 

    #     (DIFFICULTLY LOGIC)
    # - Adjusting the timer based on the game mode selected
    # - Creating a dictionary to apply for the difficultly logic
    DIFFICULTLY_SELECT = {
        "EASY": 45,
        "NORM": 30,
        "HARD": 15
    }
    if GAMEPLAY_MODE in DIFFICULTLY_SELECT:             # Checks through each line of the dictionary and pairs with the appropriate time duration
        MAX_TIMER = DIFFICULTLY_SELECT[GAMEPLAY_MODE]() # Switches the Timer to the corresponding value
        CURRENT_TIME = MAX_TIMER                        # Sets the current timer intially to the max timer
        print(f"Max Timer: {MAX_TIMER} \n Current TImer: {CURRENT_TIME}")

    #     (UPDATING PLAYER MOVMENT)
    keys = pygame.key.get_pressed()
    player.movement(keys)

    #     (DRAWING PLAYER)
    player.draw(screen)

    #     (SETUP TIMER LOGIC)
    if ACTIVE_TIMER:
        # - Decreasing the timer using delta time (time since last frame)
        DT = clock.get_time() / 1000 # Converting miliseconds to seconds
        CURRENT_TIME -= DT           # Draining the bar 

        #     [CLAMPING TO ZERO]
        # - With no negative while clamping to zero
        if CURRENT_TIME < 0: 
            CURRENT_TIME = 0          # Setting the current value to 0 
            ACTIVE_TIMER = False      # Stopping the timer when finished
            GAME_EVENTS = "SCRN_OVER" # Setting it state to game over 

    #     (DRAWING TIMER BAR)
    # - Using the existing GUI function for displaying time remaining with the timer logic
    UI.draw_bars(
        amount=CURRENT_TIME,
        max_amount=MAX_TIMER,
        x=100, 
        y=150,
        br_colour=BLUE,
        width=1000,
        height=15
    )

    #     (QUESTION LOGIC)
    # - The question text will be shown above the timer
    if CURRENT_QUESTION:
        txt_question = CURRENT_QUESTION["question"]

        #     [DRAWING THE QUESTION]
        UI.draw_text(txt_question, x=600, y=80, txt_size=50, txt_colour=WHITE, txt_font=SPACELINE)

        #     [SETUP DYNAMIC ANSWER BOXES]
        # - Makign sure each answer box is spaced evenly
        base_y = 260
        spacing = 150

        #     [SETTING UP THE ANSWER BOXES]
        for i, (label, ans_validation) in enumerate(CURRENT_QUESTION["answers"]):
            y = base_y + i * spacing             # Spacing each box vertically 
            rect = pygame.Rect(850, y, 200, 100) # Getting the rect of the asnwer box
            pygame.draw.rect(screen, BLUE, rect) # Drawing the asnwer boxes
            UI.draw_text(label, rect.centerx, rect.centery, 35, WHITE, SPACELINE)

            #    <CHECKING COLLISION WITH PROJECTILES>
            for proj in player.projectiles:
                if proj.rect.colliderect(rect):
                    RESULT_STATE = ans_validation # Changes the result state to determine if the player selected the right one
                    GAME_EVENTS = "SCRN_OVER"     # Changes to the approproiate game screen according difficultly selected
                    proj.kill()                   # Removes the projectile after collision 
                    break                         # Exiting the projectile loop
#endregion

#region handling mouse clicks and events

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_events()

def handle_mouse_events():
    # - A function to handle mouse clicks 

    global GAME_EVENTS 

    pos = pygame.mouse.get_pos()

    if GAME_EVENTS == "SCRN_MENU":
        handle_menu_clicks(pos)

def handle_menu_clicks(pos):
    # - A function for handling button clicks and inputs

    global GAME_EVENTS

    #      (MAPPPING BUTTONS + LINKED GAME STATE)
    # - Creating a dictionary for buttons and it linked game state for changing the state of the game
    BTN_EVENTS = {
        BTN_MENU_START: "SCRN_LEVEL", # Start button for triggering level selection
    }

    #      (LOOPS ALL BUTTON ACTIONS + ITS PAIRS)
    # - Loopigng through all the button-action pairs within the dictionary
    for B, event in BTN_EVENTS.items():
        # - Checking the current button has been clicked based on the mouse position
        if B.checkForInput(pos):
            GAME_EVENTS = event # Changing the event to the corresponding event string
            break               # Breaks to stop checking other buttons (Triggered once)'''
#endregion