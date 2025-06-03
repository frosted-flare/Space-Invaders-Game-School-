import pygame

class Shield(pygame.sprite.Sprite):
    def __init__(self,spaceship,position,type):
        super().__init__()
        if spaceship != False:
            self.image = pygame.image.load(f"Sprites\Shield_Sprites\Shield1.png")
            self.spaceship = spaceship
            self.rect = self.image.get_rect(center = (spaceship.rect.centerx,spaceship.rect.centery))
        else:
            self.image = pygame.image.load(f"Sprites\Shield_Sprites\Shield2.png")
            self.rect = self.image.get_rect(center = (position))

        self.starttime = pygame.time.get_ticks()
        self.type = type
        self.sway = 1
        self.sway_direction = "Right"
        

    def update(self):
        print(self.sway_direction,self.sway)
        if self.sway_direction == "Right":
            self.sway += 0.1
        elif self.sway_direction == "Left":
            self.sway -= 0.1
        if self.sway > 2:
            self.sway_direction = "Left"
        elif self.sway < -2:
            self.sway_direction = "Right"

        if self.type == 1:
            self.rect.x = self.spaceship.rect.x 
            self.rect.y = self.spaceship.rect.y - 20
        
        self.rect.x = self.rect.x + self.sway
    

  

