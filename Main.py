#region Libraries
import pygame

#      IMPORTING OTHER FILES
from Events import * 
from Datas import * 
#endregion

#      INTIALISING PYGAME
pygame.init()
pygame.display.set_caption('IntellaShooters ver:'+UPDATE_LOG)

#      MAIN LOOP
def main():
    while True:
        clock.tick(FPS)
        handle_events()
        screens_updating()
        pygame.display.update()

#      RUNNING THE MAIN 
if __name__ == "__main__":
    main()