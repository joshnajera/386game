import pygame
import random
import time
import player, projectile, enemy
from pygame.locals import *
import sys
from math import sqrt

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

def spawnNewEnemy():
    randx = random.randrange(0, width)
    randy = random.randrange(0, height)
    return enemy.Enemy((randx, randy), (0,0))

def main():
    """ Runs the game """
    screen = pygame.display.set_mode(size)
    playerCharacter = player.Player(screen)
    enemy_obj = enemy.Enemy((400,400), (0, 0))
    friendlies.add(playerCharacter)
    enemies.add(enemy_obj)

    testTimer = timer(2.0, spawnNewEnemy)
    ''' MAIN LOOP '''
    while 1:
        newObj = testTimer.update()
        if newObj:
            enemies.add(newObj)

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
        friendlies.update()
        enemies.update()

        ''' COLLISIONS '''
        for obj in friendlies:
            collision = pygame.sprite.spritecollideany(obj, enemies)
            if not collision:
                continue

            ##  Projectile Collision
            if isinstance(obj, projectile.Projectile):
                enemies.remove(collision)
                del collision
        
        ''' OBJECT RENDERING '''
        enemies.draw(screen)
        friendlies.draw(screen)
        pygame.display.update() # pygame.display.flip() is another way to do this
        clock.tick(60)          # Defines FPS/refresh time

class timer:
    def __init__(self, duration: float, fn):
        self.currentTime = time.time()
        self.time = 0.0
        self.duration = duration
        self.fn = fn
    
    def update(self):
        self.time += time.time() - self.currentTime
        self.currentTime = time.time()
        if self.time >= self.duration:
            self.time %= self.duration
            return self.fn()



if __name__ == "__main__":
    main()
