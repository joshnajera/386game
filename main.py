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
myfont = pygame.font.SysFont('Comic Sans MS', 100)
smallfont = pygame.font.SysFont('Comic Sans MS', 40)
pygame.display.set_caption("Farm Frenzy")
clock = pygame.time.Clock()

green = 0, 128, 0

''' OBJECT GROUPS '''
enemies = pygame.sprite.Group()
friendlies = pygame.sprite.Group()
flowers = pygame.sprite.Group()

def clean_groups():
    for enemy in enemies:
        pygame.sprite.Sprite.kill(enemy)
    for friendly in friendlies:
        pygame.sprite.Sprite.kill(friendly)
    for flower in flowers:
        pygame.sprite.Sprite.kill(flower)

def main():

    while 1:
        clean_groups()
        """ Runs the game """
        screen = pygame.display.set_mode(size)
        playerCharacter = player.Player(screen)
        friendlies.add(playerCharacter)
        # flowers.add(flower.Flower((0,0)))

        ''' GENERATE FLOWER BED '''
        rows, columns = 3, 3
        startx, starty = width/2 - (flower.width*rows/2), height/2 - (flower.height*columns/2)
        for i in range(columns):
            for j in range(rows):
                flowers.add(flower.Flower((startx + j*flower.width, starty + i*flower.height)))

        score = [0]
        spawner = timer(1.0, spawnNewEnemy)
        scoreTimer = timer(1.0, increment_score, score)
        play = True
        initTimer = time.time()
        gameDuration = 60
        timeRemaining = gameDuration

        while 1:
            screen.fill(green)
            textsurface = myfont.render('FARM FRENZY', False, (255, 0, 0))
            textsurface2 = smallfont.render('Press Space To Start', False, (255, 255, 255))
            screen.blit(textsurface2,(75,370))
            screen.blit(textsurface,(50,260))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                break
            clock.tick(60)

                    
        ''' MAIN LOOP '''
        while 1:
            timeRemaining = gameDuration - (time.time() - initTimer)
            if timeRemaining <= 0.0:
                play = False

            ''' EVENTS '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()

            ''' END OF GAME '''
            if len(flowers) <= 0:
                play = False
            if not play:
                screen.fill((0,0,0)) # Draw background
                textsurface = myfont.render('GAME OVER', False, (255, 0, 0))
                textsurface2 = myfont.render('Score: {}'.format(score[0]), False, (255, 255, 255))
                textsurface3 = smallfont.render('Press Space To Restart', False, (255, 255, 255) )
                screen.blit(textsurface,(100,260))
                screen.blit(textsurface2,(75,370))
                screen.blit(textsurface3,(75,470))
                pygame.display.update() # pygame.display.flip() is another way to do this
                clock.tick(60)          # Defines FPS/refresh time
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    break
                continue


            newEnemy = spawner.update()
            if newEnemy:  # Was able to create new enemy and it has a target
                enemies.add(newEnemy)
                
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
                    friendlies.remove(obj)
                    del obj
                    score[0] += 100
            
            # for obj in friendlies:
            #     collision = pygame.sprite.spritecollideany(obj, flowers)
            #     if not collision:
            #         continue
            #     if isinstance(obj, player.Player):
            #         # obj.rect.move((-obj.speed[0], -obj.speed[1]))
            #         obj.speed = list(map(lambda x: x*.5, obj.speed))

            # for enemy in enemies:
            #     collision = pygame.sprite.spritecollideany(enemy, flowers)
            #     if not collision:
            #         continue
            #     collision.hit(enemy.damage)


            ''' Draw background and score '''
            screen.fill(green) # Draw background
            textsurface = smallfont.render('Score: {}'.format(score[0]), False, (0, 0, 0))
            textsurface2 = smallfont.render('Time: {:0.1f}'.format(timeRemaining), False, (0, 0, 0))
            screen.blit(textsurface,(300,0))
            screen.blit(textsurface2,(300,50))
            
            ''' OBJECT RENDERING '''
            flowers.draw(screen)
            enemies.draw(screen)
            friendlies.draw(screen)
            pygame.display.update() # pygame.display.flip() is another way to do this
            clock.tick(60)          # Defines FPS/refresh time

            scoreTimer.update()

def spawnNewEnemy():
    """ Creates a new enemy on a random side of the screen """
    side = random.randint(0,3)
    if side == 0:   # TOP
        y = -20
        x = random.randrange(0, width)
    elif side == 1: # BOTTOM
        y = width + 10
        x = random.randrange(0, width)
    elif side == 2: # LEFT
        y = random.randrange(0, height)
        x = -20
    else:           # RIGHT
        y = random.randrange(0, height)
        x = width + 10

    try:
        dest = random.choice(flowers.sprites())
        return enemy.Enemy((x, y), dest)
    except Exception as e:
        print(e)
        print("Flowers all gone")

def increment_score(score):
    score[0][0] += 10

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
