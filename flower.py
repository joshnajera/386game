import pygame
import glob

flower_image = 'flowers1.png'
flower_image_hit = 'flowers1_hit.png'
image = pygame.image.load(flower_image)
image_hit = pygame.image.load(flower_image_hit)

scale = 3
width, height = (dim*scale for dim in image.get_size())
image = pygame.transform.scale(image, (width, height))
image_hit = pygame.transform.scale(image_hit, (width, height))

class Flower(pygame.sprite.Sprite):

    def __init__(self, location: (float, float)):
        pygame.sprite.Sprite.__init__(self)
        self.life = 10
        self.blink = False
        self.blinkCounter = 0
        self.image = image
        self.rect = self.image.get_rect()

        if location:
            self.rect.x = location[0]
            self.rect.y = location[1]
    
    def hit(self, damage=1):
        """ Deal damage to flower """
        self.life -= damage
        self.blink = True
        
        if self.life <= 0:
            pygame.sprite.Sprite.kill(self)
            del self
            return 1
        return 0

    def update(self):
        """ Blink if taking damage """
        if self.blink:
            if self.blinkCounter < 10:
                self.image = image_hit
                self.blinkCounter += 1
            elif self.blinkCounter < 20:
                self.image = image
                self.blinkCounter += 1
            else:
                self.blinkCounter = 0
                self.blink = False