#region Libraries
import pygame

#      IMPORTING OTHER FILES
from Entity import *
#endregion

#      INTIALISING PYGAME
pygame.init()

#      SETUP WINDOW
#      (SETTING FRAMERATE/FPS)
clock = pygame.time.Clock()
FPS = 60

#      WINDOW PROPERTIES
UPDATE_LOG = ' 0.0.1'     # Logs of current game version for verison control
GAME_EVENTS = "SCRN_MENU" # Holding game events as a referenced variable 

WIDTH, HEIGHT = 1200, 600                         # Determining the measurements of the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Applying those measurements to make the screen dimensions

#      ALL COLOURS
# - Using variables to have callable colour for applying to the gui
# - All colours will be in RGB format 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 151, 23)

#      GUI CLASS 
#region GUI Functions
class GUICreator():
    def __init__(self, surface):
        self.surface = surface

    def draw_text(self, text, x, y, txt_size, txt_colour, txt_font=None):
        # - A function for rendering and creating text on the screen 
        font = pygame.font.Font(txt_font, txt_size)        # Loading the font with it specifified size
        text_surface = font.render(text, True, txt_colour) # Rendering text surface with colour
        text_rect = text_surface.get_rect(center=(x, y))   # Positioning the text at the given X|Y coordinates
        self.surface.blit(text_surface, text_rect)         # Drawing the text on the screen

    def draw_bars(self, amount, max_amount, x, y, br_colour):
        # - A function for drawing bars for either player health indication or etc
        ratio = amount / max_amount
        pygame.draw.rect(self.surface, WHITE, (x - 2, y - 2, 404, 34))     # White bars surrounding the bar
        pygame.draw.rect(self.surface, BLACK, (x, y, 400, 30))             # The intial size of the bar
        pygame.draw.rect(self.surface, br_colour, (x, y, 400 * ratio, 30)) # The changeable bar depending what it used for

#      (SETTING UP GUI VARIABLE)
UI = GUICreator(screen) # Will be kept as a reference when wanting to draw certain GUI elements
#endregion

#     BUTTON CLASS
#region Button Class
main_font = pygame.font.SysFont("Orbitronio", 50) # defining the font the button will use
class ButtonFunc():
    def __init__(self, image, x_pos, y_pos, text_input, img2):
        self.image = image
        self.originalimage = image 
        self.imgae2 = img2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        # Ensure the image has an alpha channel (transparency)
        if self.image.get_alpha() is None:
            self.image = self.image.convert_alpha()  # Convert to support transparency

        self.mask = pygame.mask.from_surface(self.image)  # Create a pixel mask

    def update(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        # Convert screen coordinates to local button coordinates
        local_x = position[0] - self.rect.left
        local_y = position[1] - self.rect.top
        
        # Check if the position is within the image mask (non-transparent pixel)
        if 0 <= local_x < self.rect.width and 0 <= local_y < self.rect.height:
            if self.mask.get_at((local_x, local_y)):  # If pixel is not transparent
                #print("Button pressed!")
                return True  # Click is valid

        return False  # Click is outside the button shape

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = main_font.render(self.text_input, True, "orange")
            if self.image != self.imgae2:
                self.image = self.imgae2
                self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
                self.mask = pygame.mask.from_surface(self.image)
        else:
            self.text = main_font.render(self.text_input, True, "white")
            if self.image != self.originalimage:
                self.image = self.originalimage
                self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
                self.mask = pygame.mask.from_surface(self.image)

#      (RESUSABLE BUTTON VARIABLE)
BTN_IMG_DIR = "Assets/Images/UI/Buttons/" # The directory to the button assets

#      [SETUP BUTTON PROPERTIES]
BTN_MENU_surface = pygame.image.load(BTN_IMG_DIR+"button2.png")        # Attaching the sprite 
BTN_MENU_surface = pygame.transform.scale(BTN_MENU_surface, (250, 75)) # Determining its size and height

# - Doing again but for a different sprite that for hovering over the button
BTN_MENULIT_surface = pygame.image.load(BTN_IMG_DIR+"button1.png")           # Attaching the sprite 
BTN_MENULIT_surface = pygame.transform.scale(BTN_MENULIT_surface, (250, 75)) # Determining its size and height

#      [MENU BUTTONS]
BTN_MENU_START = ButtonFunc(BTN_MENU_surface, 600, 460, "START", BTN_MENULIT_surface) # Creating button for the menu
#endregion

#region Player 
player = Player(x=100, y=400, speed =5, screen_height=HEIGHT)
#endregion