import pygame
import player
from pygame import *
from enum import Enum

class direction(Enum):
    LEFT = -1
    RIGHT = 1

class Projectile:

    def __init__(self, screen, player_rect, player_dir):
        self.screen = screen
        self.speed = 10
        self.sprite = pygame.image.load("turnip.png")
        self.rect = self.sprite.get_rect()
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

        self.screen.blit(self.sprite, self.rect)


    def update(self):
        if self.dir == direction.LEFT:
            self.rect.x -= self.speed
        elif self.dir == direction.RIGHT:
            self.rect.x += self.speed


        self.screen.blit(self.sprite, self.rect)
