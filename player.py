import sys, glob, pygame, math, projectile
from enum import Enum

class direction(Enum):
    LEFT = -1
    RIGHT = 1

turnip = pygame.image.load("turnip.png")

class Player:
    width, height = 800, 800
    Scale = 5
    def __init__(self, screen):

        self.projectiles = []
        self.reload_time = 0
        self.reload_speed = 30
        self.reloading = False
        self.screen = screen
        self.speed = [0,0]
        self.max_speed = 5
        self.scale = Player.Scale
        self.acceleration = .3
        self.direction = direction.RIGHT

        self.ani_l = glob.glob("bun/bunl*")
        self.ani_r = glob.glob("bun/bunr*")
        self.ani_l.sort()
        self.ani_r.sort()

        self.ani_max = len(self.ani_l) - 1
        self.ani_speed = 10
        self.ani_counter = 0
        self.ani_frame = 0

        self.img = pygame.image.load(self.ani_l[0])
        self.width, self.height = self.img.get_size()

        self.rect = self.img.get_rect()
        self.update(0)
    
    def shoot(self):
        # turnip_rect = turnip.get_rect()
        self.projectiles.append(projectile.Projectile(self.screen, self.rect, self.direction))

        # self.screen.blit(turnip, turnip_rect)

        
    
    def update(self, frame):

        ## Loop through frames depending on animation speed and animation frames
        self.ani_counter = (self.ani_counter + 1) % self.ani_speed
        if self.ani_counter == self.ani_max:
            self.ani_frame = (self.ani_frame + 1) % len(self.ani_l)

        ## Set direction based off movement
        if self.speed[0] < 0:
            self.direction = direction.LEFT
        elif self.speed[0] > 0:
            self.direction = direction.RIGHT
        else:
            self.ani_frame = 0

        ## Set frame based off direction
        if self.direction == direction.RIGHT:
            self.img = pygame.image.load(self.ani_r[self.ani_frame])
        else:
            self.img = pygame.image.load(self.ani_l[self.ani_frame])

        scaled_img = pygame.transform.scale(self.img, (self.width*self.scale, self.height*self.scale))
        scaled_rect = self.rect.inflate((self.scale, self.scale))

        self.screen.blit(scaled_img, scaled_rect)
        if self.reloading:
            self.reload_time = (self.reload_time+1) % self.reload_speed
            if self.reload_time == 0:
                self.reloading = False

        for shot in self.projectiles:
            shot.update()
    
    def processInput(self, keys):

        ## Check keys and calculate speed
        if keys[pygame.K_LEFT]:
            self.speed[0] -= self.acceleration
            if self.speed[0] < -self.max_speed:
                self.speed[0] = -self.max_speed
            print("MOving Left")
        if keys[pygame.K_RIGHT]:
            self.speed[0] += self.acceleration
            if self.speed[0] > self.max_speed:
                self.speed[0] = self.max_speed
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.speed[0] *= .9
        if abs(self.speed[0]) < 0.1:
            self.speed[0] = 0

        if keys[pygame.K_DOWN]:
            self.speed[1] += self.acceleration
            if self.speed[1] > self.max_speed:
                self.speed[1] = self.max_speed
        if keys[pygame.K_UP]:
            self.speed[1] -= self.acceleration
            if self.speed[1] < -self.max_speed:
                self.speed[1] = -self.max_speed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.speed[1] *= .9
        if abs(self.speed[1]) < 0.1:
            self.speed[1] = 0

        if keys[pygame.K_SPACE] and not self.reloading:
            print("Spacebar")
            self.reloading = True
            self.shoot()
        
        ## Move acording to speed
        self.rect = self.rect.move(self.speed)

        ## Checking bounds
        if self.rect.x < 0:
            self.rect.x = 0
            self.speed[0] = 0 
        if self.rect.x > (Player.width - (self.rect.width*self.scale)): 
            self.rect.x = (Player.width - (self.rect.width*self.scale))
            self.speed[0] = 0 

        if self.rect.y < 0:
            self.rect.y = 0
            self.speed[1] = 0 
        if self.rect.y > (Player.height - (self.rect.height*self.scale)): 
            self.rect.y = (Player.height - (self.rect.height*self.scale))
            self.speed[1] = 0 
