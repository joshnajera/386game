import pygame
import glob
import math
from flower import Flower
height, width = 800, 800
ani_l = glob.glob("ham/haml*")
ani_r = glob.glob("ham/hamr*")

class Enemy(pygame.sprite.Sprite):
    """ Temporary enemy """
    def __init__(self, position:(float,float), destination:Flower):
        """ Setup """
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.destiination = destination
        self.attack_delay = 30
        self.attack_timer = 0
        self.damage = 1
        self.scale = 3
        self.ani_l = ani_l
        self.ani_r = ani_r
        self.ani_frame = 0
        self.ani_counter = 0
        self.ani_speed = 10
        self.ani_max = len(ani_l) - 1

        # self.image = pygame.image.load('grass.png')
        self.image = self.loadFrame('r')
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.LR = 1 if (self.destiination.rect.x - self.rect.x) > 10 else -1
        self.hasTarget = True

    def loadFrame(self, dir: chr):
        """ Set image based on frame and direction """
        if dir == 'r':
            img = pygame.image.load(self.ani_r[self.ani_frame])
        elif dir == 'l':
            img = pygame.image.load(self.ani_l[self.ani_frame])
        else:
            print("ERROR")
        width, height = img.get_size()
        return pygame.transform.scale(img, (width*self.scale, height*self.scale))
    
    def update(self):
        """ Move towards destination """ 
        
        ''' Load next frame based off direction of movement '''
        if self.LR == 1:
            self.image = self.loadFrame('r')
        elif self.LR == -1:
            self.image = self.loadFrame('l')

        UD = 1 if (self.destiination.rect.y - self.rect.y) > 0 else -1
        if abs(self.destiination.rect.y - self.rect.y) < 2:
            UD = 0

        if abs(self.rect.x - self.destiination.rect.x) > 2 or not self.hasTarget:
            self.rect.x += self.LR*self.speed
        self.rect.y += UD*self.speed
         
        if self.hasTarget and self.canAttack():
            if self.destiination.hit(self.damage):
                print("I killed a thing")
                self.hasTarget = False
        
        self.ani_counter = (self.ani_counter + 1) % self.ani_speed
        if self.ani_counter == self.ani_max:
            self.ani_frame = (self.ani_frame + 1) % len(self.ani_l)
    
    def canAttack(self):
        """ If within attacking distance and cooldown is off """
        threshhold = 3
        dx = (self.rect.x - self.destiination.rect.x) ** 2
        dy = (self.rect.y - self.destiination.rect.y) ** 2
        dist = math.sqrt(dx + dy)

        if (dist < threshhold) and (self.attack_timer == 0):
            self.attack_timer += 1
            return True
        else:
            self.attack_timer = (self.attack_timer +  1) % self.attack_delay
        return False
        
