import pygame
import time
import player
from enum import Enum

class direction(Enum):
    LEFT = -1
    RIGHT = 1

class Projectile(pygame.sprite.Sprite):
    """ Turnip Bullet """

    def __init__(self, player_rect, player_dir):
        """ Setup """
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.timeToLive = 1
        self.initTime = time.time()
        self.image = pygame.image.load("turnip.png")
        scale = 2
        width, height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (width*scale, height*scale))
        self.rect = self.image.get_rect()

        ''' Initialize position and direction '''
        self.rect.x = player_rect.x
        self.rect.y = player_rect.y
        if player_dir == player.direction.RIGHT:
            self.dir = direction.RIGHT  
        else:
            self.dir = direction.LEFT

        if self.dir == direction.LEFT:
            self.rect.x = player_rect.x - self.rect.width
            self.rect.y = self.rect.height + (player_rect.y)
        else:
            self.rect.x = player_rect.x + (player_rect.width*player.Player.Scale)
            self.rect.y = player_rect.y + (player_rect.height*player.Player.Scale/2)


    def update(self):
        if self.dir == direction.LEFT:
            self.rect.x -= self.speed
        elif self.dir == direction.RIGHT:
            self.rect.x += self.speed
        
        if (time.time() - self.initTime) > self.timeToLive:
            pygame.sprite.Sprite.kill(self)
            del self
        
