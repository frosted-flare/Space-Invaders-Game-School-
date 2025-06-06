import pygame

class Explosion(pygame.sprite.Sprite):

    ## Simple Explosion That Removes Itself After A Tiny While ## 

    def __init__(self,position):
        super().__init__()
    
        self.image = pygame.image.load(f"Sprites\Explosion_Sprites\Explosion_1.png")
        self.rect = self.image.get_rect(center = position)
        self.starttime = pygame.time.get_ticks()
        

    def update(self):
        if pygame.time.get_ticks() - self.starttime > 200:
            self.kill()
        
 

  

