import pygame
import os

class Laser(pygame.sprite.Sprite):
    def __init__(self,position,speed,screen_height,path):
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

        self.ANIMATION_SPEED = 200
        self.last_update = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()

        if pygame.time.get_ticks() - self.last_update > self.ANIMATION_SPEED: # This if statment makes sure the sprite does not update every frame
            self.last_update = pygame.time.get_ticks()

            if self.current_image_index != len(self.sprites):
                self.image = self.sprites[self.current_image_index]
                self.current_image_index = self.current_image_index+1

            else:
                self.image = self.sprites[0]
                self.current_image_index = 1

