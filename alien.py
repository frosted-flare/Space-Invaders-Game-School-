import pygame
import os
import random
class Alien(pygame.sprite.Sprite):

    def __init__(self,type,speed, x, y): 
        super().__init__()
        self.type = type

        self.path = f"Sprites/Enemy_{type}_Sprites/"

        self.sprite_names = os.listdir(self.path) # Not images
        self.sprites = []
        
        counter = 1
        for image in self.sprite_names:
            image = pygame.image.load(f"Sprites/Enemy_{type}_Sprites/Enemy{counter}.png")
            self.sprites.append(image)
            counter += 1

        
        self.image = self.sprites[0]
        self.current_image_index = 0
        self.rect = self.image.get_rect(topleft = (x,y))

        self.ANIMATION_SPEED = speed
        self.last_update = 0
        self.last_move = 0
        if random.randint(1,5) == 1:
            self.contains_powerup = True
        else:
            self.contains_powerup = False


        


    def update(self,direction,contact,Alien_speed,move_distance):

        ## Movement ##

        if pygame.time.get_ticks() - self.last_move > Alien_speed or contact: # Contact esures that the sprite still moves of the wall
            self.last_move = pygame.time.get_ticks()
            self.rect.x += direction * move_distance

        ## Animation ##
        
        if pygame.time.get_ticks() - self.last_update > self.ANIMATION_SPEED: # This if statment makes sure the sprite does not update every frame
            self.last_update = pygame.time.get_ticks()

            if self.current_image_index != len(self.sprites):
                self.image = self.sprites[self.current_image_index]
                self.current_image_index = self.current_image_index+1

            else:
                self.image = self.sprites[0]
                self.current_image_index = 1


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self,screen_width,offset):
        super().__init__()

        self.direction = random.choice([0,1])
        self.offset = offset
        self.screen_width = screen_width

        if self.direction == 0:
            self.image = pygame.image.load(f"Sprites/Mystery_Ship_Sprites/MysteryShipRight.png")
        else:
            self.image = pygame.image.load(f"Sprites/Mystery_Ship_Sprites/MysteryShipLeft.png")

        if self.direction == 0:
            x = self.offset/2
        else:
            x = self.screen_width - self.image.get_width()

        if x == self.offset/2:
            self.speed = 1
        else:
            self.speed = -1

        self.rect = self.image.get_rect(topleft = (x,20))

    def update(self):

        self.rect.x += self.speed
        if self.rect.right > self.screen_width + self.offset/2 + 80:
            self.kill()
        elif self.rect.left < self.offset/2 - 80:
            self.kill()
