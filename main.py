import pygame
import player, projectile
from pygame.locals import *
import sys
from math import sqrt

## Game Properties
size = width, height = 800, 800
player_speed = [0, 0] # [X-axis, Y-axis]

pygame.init()
pygame.display.set_caption("This is a test")
clock = pygame.time.Clock()

black = 0, 0, 0
green = 0, 128, 0

def main():
    screen = pygame.display.set_mode(size)
    grass = pygame.image.load('grass.png')
    grass_rect = grass.get_rect()
    playerCharacter = player.Player(screen)

    ## Placing the object in the center
    grass_rect.x = width/2 - grass_rect.width/2
    grass_rect.y = height/2 - grass_rect.height/2

    ## Main Game Loop
    while 1:
        screen.fill(green) # Draw background
        # Get all that's going on and iterate over them
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            
        # Check what the player is holding in regards to movement
        keys = pygame.key.get_pressed()
        if keys:
            print("Key Pressed~")
            playerCharacter.processInput(keys)
        
        ## Update locations
        playerCharacter.update(0)

        ## Re-render the screen
        screen.blit(grass, grass_rect) # Draw object
        pygame.display.update() # pygame.display.flip() is another way to do this
        clock.tick(60) #Defines FPS/refresh time


if __name__ == "__main__":
    main()
