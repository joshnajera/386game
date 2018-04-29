import pygame
import random
import time
import player, projectile, enemy, flower
from pygame.locals import *
import sys
from math import sqrt

''' GAME PROPERTIES '''
size = width, height = 800, 800
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

pygame.display.set_caption("Farm Frenzy")
clock = pygame.time.Clock()

green = 0, 128, 0

''' OBJECT GROUPS '''
enemies = pygame.sprite.Group()
friendlies = pygame.sprite.Group()
flowers = pygame.sprite.Group()


def spawnNewEnemy():
    randx = random.randrange(0, width)
    randy = random.randrange(0, height)
    try:
        dest = random.choice(flowers.sprites())
        return enemy.Enemy((randx, randy), dest)
    except Exception as e:
        print(e)
        print("Flowers all gone")

def increment_score(score:int):
    score[0][0] += 10
    # return(score[0] + 10)


def main():
    """ Runs the game """
    screen = pygame.display.set_mode(size)
    playerCharacter = player.Player(screen)
    # enemy_obj = enemy.Enemy((400,400), (0, 0))
    # enemies.add(enemy_obj)
    friendlies.add(playerCharacter)
    # flowers.add(flower.Flower((0,0)))

    ''' GENERATE FLOWER BED '''
    rows, columns = 3, 3
    startx, starty = width/2 - (flower.width*rows/2), height/2 - (flower.height*columns/2)
    for i in range(columns):
        for j in range(rows):
            flowers.add(flower.Flower((startx + j*flower.width, starty + i*flower.height)))

    score = [0]
    spawner = timer(3.0, spawnNewEnemy)
    scoreTimer = timer(1.0, increment_score, score)

    ''' MAIN LOOP '''
    while 1:
        scoreTimer.update()
        newObj = spawner.update()
        if newObj:
            enemies.add(newObj)

        ''' Draw background and score '''
        screen.fill(green) # Draw background
        textsurface = myfont.render('Score: {}'.format(score[0]), False, (0, 0, 0))
        screen.blit(textsurface,(400,0))

        ''' EVENTS '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            
        ''' I/O '''
        keys = pygame.key.get_pressed()
        if keys:
            newObj = playerCharacter.processInput(keys)
            if newObj:        # Store new player projectiles
                friendlies.add(newObj)
        
        ''' UPDATES OBJECTS '''
        friendlies.update()
        enemies.update()
        flowers.update()

        ''' COLLISIONS '''
        for obj in friendlies:
            collision = pygame.sprite.spritecollideany(obj, enemies)
            if not collision:
                continue

            ##  Projectile Collision
            if isinstance(obj, projectile.Projectile):
                enemies.remove(collision)
                del collision
        
        for obj in friendlies:
            collision = pygame.sprite.spritecollideany(obj, flowers)
            if not collision:
                continue
            if isinstance(obj, player.Player):
                # obj.rect.move((-obj.speed[0], -obj.speed[1]))
                obj.speed = list(map(lambda x: x*.5, obj.speed))

        # for enemy in enemies:
        #     collision = pygame.sprite.spritecollideany(enemy, flowers)
        #     if not collision:
        #         continue
        #     collision.hit(enemy.damage)
        
        ''' OBJECT RENDERING '''
        flowers.draw(screen)
        enemies.draw(screen)
        friendlies.draw(screen)
        pygame.display.update() # pygame.display.flip() is another way to do this
        clock.tick(60)          # Defines FPS/refresh time

class timer:
    def __init__(self, duration: float, fn, *args):
        self.currentTime = time.time()
        self.time = 0.0
        self.duration = duration
        self.fn = fn
        self.args = args
    
    def update(self):
        self.time += time.time() - self.currentTime
        self.currentTime = time.time()
        if self.time >= self.duration:
            self.time %= self.duration
            if self.args:
                return self.fn(self.args)
            return self.fn()
        return None

if __name__ == "__main__":
    main()
