import pygame
height, width = 800, 800

class Enemy(pygame.sprite.Sprite):
    """ Temporary enemy """
    def __init__(self, position:(float,float), destination:(int,int)):
        """ Setup """
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.destiination = destination

        self.image = pygame.image.load('grass.png')
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
    
    def update(self):
        """ Move towards destination """ 
        LR = 1 if (self.destiination[0] - self.rect.x) > 0 else -1
        if abs(self.destiination[0] - self.rect.x) < 2:
            LR = 0

        UD = 1 if (self.destiination[1] - self.rect.y) > 0 else -1
        if abs(self.destiination[1] - self.rect.y) < 2:
            UD = 0

        self.rect.x += LR*self.speed
        self.rect.y += UD*self.speed
