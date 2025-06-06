import pygame
import random

class Laser(pygame.sprite.Sprite):

    ## Laser That Gets Fired By Aliens And The Player ##

    def __init__(self,position,speed,screen_height,path,type,spaceship):
        super().__init__()
        

        ## Image ##

        self.path = path
        self.sprites = []
        image = pygame.image.load(path)
        self.sprites.append(image)
        self.image = self.sprites[0]
        self.current_image_index = 0
        self.rect = self.image.get_rect(center = position)

        ## Important Variables ##

        self.speed = speed
        self.screen_height = screen_height
        self.type = type
        self.spaceship = spaceship
        self.bounced = False
        self.flipped = False
        self.start_time = pygame.time.get_ticks()
        self.offset = random.randrange(-200,200)

    def update(self):

        ## Allows for very specific bullet movements ##

        if self.type == 2: # Blue bullet that tracks the player.
            self.rect.y -= self.speed/2

            if self.spaceship.rect.x > self.rect.x:
                self.rect.x += 1
            elif self.spaceship.rect.x < self.rect.x:
                self.rect.x -= 1
            else:
                pass
        elif self.type == 11: # Special boss bullet that tracks the player.
            if pygame.time.get_ticks() - self.start_time > 5000:
                self.rect.y -= self.speed * 2

            if self.spaceship.rect.x + self.offset > self.rect.x:
                self.rect.x += 1
            elif self.spaceship.rect.x + self.offset < self.rect.x:
                self.rect.x -= 1
            else:
                pass    
        else:
            self.rect.y -= self.speed

       
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()
        
        if self.flipped == True: # Allows for bullet bouncing.
            self.flipped = False
            self.image = pygame.transform.flip(self.image,False,True)


