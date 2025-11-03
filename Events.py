#region Libraries
import pygame
import sys

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
        "SCRN_OVER": drawing_menu
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
    UI.draw_text("IntellaShooters", 600, 105, 90, WHITE, ORBITRONIO)

    #      (MAKING BUTTONS VISIBLE)
    for button in [BTN_MENU_START]:
        button.update(screen)
        button.changeColor(pygame.mouse.get_pos())

#     LEVELS SCREEN 
def drawing_Level(): 
    global GAME_EVENTS
    # - A function for drawing the menu for the game
    screen.fill((0, 0, 0))

    #     (DRAWIGN TEXT ON SCREEN)
    UI.draw_text("SELECT DIFFICULTY", 600, 75, 55, WHITE, ORBITRONIO)

    #     (UPDATING PLAYER MOVMENT)
    keys = pygame.key.get_pressed()
    player.movement(keys)

    #     (DRAWING PLAYER)
    player.draw(screen)

    #     (DRAWING BOXES)
    # - Setting out the Rect for collision detection
    rect_easy = pygame.Rect(500, 140, 200, 100)
    rect_normal = pygame.Rect(500, 300, 200, 100)
    rect_hard = pygame.Rect(500, 460, 200, 100)

    # - Drawing boxes for the options for level of difficult
    pygame.draw.rect(screen, BLUE, rect_easy)
    pygame.draw.rect(screen, BLUE, rect_normal)
    pygame.draw.rect(screen, BLUE, rect_hard)

    #     (DRAWING LABELS)
    UI.draw_text("EASY", rect_easy.centerx, rect_easy.centery, 35, WHITE, ORBITRONIO)
    UI.draw_text("NORM", rect_normal.centerx, rect_normal.centery, 35, WHITE, ORBITRONIO)
    UI.draw_text("HARD", rect_hard.centerx, rect_hard.centery, 35, WHITE, ORBITRONIO)

    #     (CHECKING COLLISIONS)
    # - Checking if player projectiles has collided with the boxes
    for Proj in player.projectiles:

        #     [HITTING THE EASY BOX]
        if Proj.rect.colliderect(rect_easy): # If it collides with the easy box
            GAME_EVENTS = "SCRN_GAME"        # Changes the game state to active gameplay
            Proj.kill()                      # Remoes the projectiles after hit
            break                            # Stops checking
        
        #     [HITTING THE NORMAL BOX]
        elif Proj.rect.colliderect(rect_normal): # If it collides with the easy box
            GAME_EVENTS = "SCRN_GAME"            # Changes the game state to active gameplay
            Proj.kill()                          # Remoes the projectiles after hit
            break                                #  Stops checking
        
        #     [HITTING THE HARD BOX]
        elif Proj.rect.colliderect(rect_hard): # If it collides with the easy box
            GAME_EVENTS = "SCRN_GAME"            # Changes the game state to active gameplay
            Proj.kill()                          # Remoes the projectiles after hit
            break                                #  Stops checking
#     LEVELS SCREEN 
def drawing_gameplay():
    screen.fill((0, 0, 0)) 

    #     (UPDATING PLAYER MOVMENT)
    keys = pygame.key.get_pressed()
    player.movement(keys)

    #     (DRAWING PLAYER)
    player.draw(screen)
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