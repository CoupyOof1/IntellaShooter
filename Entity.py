#region Libraries
import pygame 

#endregion

#      PLAYER CLASS 
#region Player Class 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, screen_height):
        super().__init__() # Intialising the class

        #      (PLAYER HEALTH)
        # - Creating a health sytem for the player 

        #      (PLAYER VISUALS)
        # - For now, creating a simple rectangle (50x50 pixels) for representing the player
        self.image = pygame.Surface((50, 50)) # Creating the rectangle by 50x50 pixels
        self.image.fill((0, 255, 0))          # Making it Green (Changeable)
        
        #      (GETTING RECTANGLE AREA)
        # - Will be used for positoning and collision
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)         # Setting it starting positon

        #      (MOVEMENT SETTINGS)
        self.speed = speed               # Determining how fast the player can move 
        self.scrn_height = screen_height # Ensuring player stays inside the screen

        #      (SHOOTING SETTINGS)
        self.projectiles = pygame.sprite.Group() # Holding all player's projectiles
        self.proj_cooldown = 300                 # Delay in time between each shot measured in ms 
        self.proj_last_shottime = 0              # Determining when the last shot was fired

    def movement(self, pressed_keys):
        # - This will be a function for handling both the player movements and updating the projectiles

        #      (MOVING UPWARDS)
        if pressed_keys[pygame.K_UP]:
            self.rect.y -= self.speed
        #      (MOVING DOWNWARDS)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if pressed_keys[pygame.K_SPACE]:
            self.Shoot()

        #      (LIMITING MOVEMENT SPACE)
        # - Limiting the movement of the player towards the screen height
        if self.rect.top < 0: 
            self.rect.top = 0 
        if self.rect.bottom > self.scrn_height:
            self.rect.bottom = self.scrn_height

        #      (UPDATING PROJECTILES)
        self.projectiles.update()

    def Shoot(self):
        # - This will be a function that handles the shooting projectiles
        current_time = pygame.time.get_ticks() # Retrieving the current time inms

        #      (CHECKING IF ENOUGH TIME HAS PASSED)
        # - Checks if neough time had passsed since the last shot was made
        if current_time - self.proj_last_shottime >= self.proj_cooldown:
            projectile = Projectile(self.rect.right, self.rect.centery) # Making the projectile
            self.projectiles.add(projectile)                            # Adding projectile to the group
            self.proj_last_shottime = current_time                      # Resetting the timer

    def draw(self, surface):
        # - A function for drawing the player and all the projectiles on screen
        surface.blit(self.image, self.rect)
        self.projectiles.draw(surface)
#endregion

#      PROJECTILE CLASS
#region Projectile class 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # Intialising the class 

        #      (PROJECTILE VISUALS)
        self.image = pygame.Surface((10, 5)) # Draws small rectangle for the projectiles
        self.image.fill((255, 255, 0))       # Makes the projectile yellow 
        self.rect = self.image.get_rect()    # Retrieving the rect for collision detection
        self.rect.center = (x, y)            # Setting its intial position

        #      (PROJECTILE MOVEMENT SETTINGS)
        self.speed = 10 # Moves each projectile to the right 

    def update(self):
        # - This will be afunction that moves the projectiles and removes it if it touches the off screen
        self.rect.x += self.speed # Moving the projecitle to the right

        #      (BULLET GOES OFF SCREEN)
        # - If the bullet goes beyond the screen width, it getas removed.
        if self.rect.left > 1200:
            self.kill()
#endregion