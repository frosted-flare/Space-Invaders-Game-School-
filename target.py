import pygame
import os
import random
class Target(pygame.sprite.Sprite):

    def __init__(self, x, y): 
        super().__init__()
        self.type = type
        
        self.image = pygame.image.load(f"Sprites/Target_Sprites/Target1.png")
          
        self.rect = self.image.get_rect(topleft = (x,y))
        self.start_time = pygame.time.get_ticks()
        

        


    def update(self):
        if self.start_time - pygame.time.get_ticks() > 10000:
            self.kill()
            