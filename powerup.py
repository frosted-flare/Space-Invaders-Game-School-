import pygame,os,random

class Powerup(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()

        type = random.randint(1,2)

        if type == 1:
            self.image = pygame.image.load(f"Sprites\Power_Up_1_Sprites\Powerup1.png")
        elif type == 2:
            self.image = pygame.image.load(f"Sprites\Power_Up_2_Sprites\Powerup2.png")
       
    
        self.rect = self.image.get_rect(center = position)
        self.starttime = pygame.time.get_ticks()
        self.speed = 2
        self.type = type


    def update(self):
        self.rect.y += self.speed
        if pygame.time.get_ticks() - self.starttime > 5000:
            self.kill()
            
        
 

  

