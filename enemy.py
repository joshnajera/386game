import pygame
import math
from flower import Flower
height, width = 800, 800

class Enemy(pygame.sprite.Sprite):
    """ Temporary enemy """
    def __init__(self, position:(float,float), destination:Flower):
        """ Setup """
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.destiination = destination
        self.damage = 1
        self.attack_delay = 30
        self.attack_timer = 0

        self.image = pygame.image.load('grass.png')
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
    
    def update(self):
        """ Move towards destination """ 
        LR = 1 if (self.destiination.rect.x - self.rect.x) > 0 else -1
        if abs(self.destiination.rect.x - self.rect.x) < 2:
            LR = 0

        UD = 1 if (self.destiination.rect.y - self.rect.y) > 0 else -1
        if abs(self.destiination.rect.y - self.rect.y) < 2:
            UD = 0

        self.rect.x += LR*self.speed
        self.rect.y += UD*self.speed
         
        if self.canAttack():
            self.destiination.hit(self.damage)
    
    def canAttack(self):
        threshhold = 2
        dx = (self.rect.x - self.destiination.rect.x) ** 2
        dy = (self.rect.y - self.destiination.rect.y) ** 2
        dist = math.sqrt(dx + dy)

        if (dist < threshhold) and (self.attack_timer == 0):
            self.attack_timer += 1
            return True
        else:
            self.attack_timer = (self.attack_timer +  1) % self.attack_delay
        return False
        
