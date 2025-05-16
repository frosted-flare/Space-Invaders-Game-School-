import pygame
import os

class Alien(pygame.sprite.Sprite):

    def __init__(self,type,speed, x, y): 
        super().__init__()
        self.type = type

        self.path = f"Sprites/Enemy_{type}_Sprites/"

        self.sprite_names = os.listdir(self.path) # Not images
        self.sprites = []

        
        for image in self.sprite_names:
            image = pygame.image.load(f"Sprites/Enemy_{type}_Sprites/{image}")
            self.sprites.append(image)
        
        self.image = self.sprites[0]
        self.current_image_index = 0
        self.rect = self.image.get_rect(topleft = (x,y))

        self.ANIMATION_SPEED = speed
        self.last_update = 0

    def update(self,direction):

        ## Movement ##
        self.rect.x += direction

        ## Animation ##
        
        if pygame.time.get_ticks() - self.last_update > self.ANIMATION_SPEED: # This if statment makes sure the sprite does not update every frame
            self.last_update = pygame.time.get_ticks()

            if self.current_image_index != len(self.sprites):
                self.image = self.sprites[self.current_image_index]
                self.current_image_index = self.current_image_index+1

            else:
                self.image = self.sprites[0]
                self.current_image_index = 1

