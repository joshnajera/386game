import pygame
import player, projectile
from pygame.locals import *
import sys
from math import sqrt

class grass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('grass.png')
        self.rect = self.image.get_rect()

        ## Placing the object in the center
        self.rect.x = width/2 - self.rect.width/2
        self.rect.y = height/2 - self.rect.height/2
        # screen.blit(grass, grass_rect) # Draw object


''' GAME PROPERTIES '''
size = width, height = 800, 800
pygame.init()
pygame.display.set_caption("This is a test")
clock = pygame.time.Clock()

black = 0, 0, 0
green = 0, 128, 0

''' OBJECT GROUPS '''
enemies = pygame.sprite.Group()
friendlies = pygame.sprite.Group()

def main():
    """ Runs the game """
    screen = pygame.display.set_mode(size)
    playerCharacter = player.Player(screen)
    grass_obj = grass()
    friendlies.add(playerCharacter)
    enemies.add(grass_obj)

    ''' MAIN LOOP '''
    while 1:
        screen.fill(green) # Draw background

        ''' EVENTS '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            
        ''' I/O '''
        keys = pygame.key.get_pressed()
        if keys:
            newObj = playerCharacter.processInput(keys)
            if newObj:        # Store new objects belonging to player
                friendlies.add(newObj)
        
        ''' UPDATES '''
        # playerCharacter.update(0)
        friendlies.update()
        # grass_obj.update(0)

        ''' COLLISIONS '''
        for obj in friendlies:
            collision = pygame.sprite.spritecollideany(obj, enemies)
            if not collision:
                continue

            ##  Projectile Collision
            if isinstance(obj, projectile.Projectile):
                print(obj,' is of class: ', type(obj))
                enemies.remove(collision)
                del collision
        
        ''' OBJECT RENDERING '''
        enemies.draw(screen)
        friendlies.draw(screen)
        pygame.display.update() # pygame.display.flip() is another way to do this
        clock.tick(60)          #Defines FPS/refresh time


if __name__ == "__main__":
    main()
