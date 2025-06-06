import pygame
import random

class Laser(pygame.sprite.Sprite):
    def __init__(self,position,speed,screen_height,path,type,spaceship):
        super().__init__()
        
        self.path = path
        self.sprites = []

        
        image = pygame.image.load(path)
        self.sprites.append(image)


        self.image = self.sprites[0]
        self.current_image_index = 0
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.screen_height = screen_height
        self.type = type
        self.spaceship = spaceship
        self.bounced = False
        self.flipped = False

    def update(self):

        if self.type == 2:
            self.rect.y -= self.speed/2

            if self.spaceship.rect.x > self.rect.x:
                self.rect.x += 1
            elif self.spaceship.rect.x < self.rect.x:
                self.rect.x -= 1
            else:
                pass
        elif self.type == 11:
            self.rect.y -= self.speed

            if self.spaceship.rect.x > self.rect.x:
                self.rect.x += random.randint(4,20)/10
            elif self.spaceship.rect.x < self.rect.x:
                self.rect.x -= random.randint(4,20)/10
            else:
                pass    
        else:
            self.rect.y -= self.speed

       
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()
        
        if self.flipped == True:
            self.flipped = False
            self.image = pygame.transform.flip(self.image,False,True)


