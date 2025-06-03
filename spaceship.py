import pygame
import os
from laser import Laser


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height,offset, game):
        super().__init__()
        
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Sprites/Player_Sprites/Player1.png")

        self.path = f"Sprites/Player_Sprites/"

        self.sprite_names = os.listdir(self.path) # Not images
        self.sprites = []

        counter = 1
        for image in self.sprite_names:
            image = pygame.image.load(f"Sprites/Player_Sprites/Player{counter}.png")
            self.sprites.append(image)
            counter += 1

        self.rect = self.image.get_rect(midbottom = ((self.screen_width + offset)/2,self.screen_height - offset))
        self.speed = 2
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_activated = False
        self.laser_time = 0
        self.laser_delay = 300
        self.animation_speed = 200
        self.non_linear_animation_speed = self.animation_speed
        self.current_image_index = 0
        self.last_update = 0
        self.laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")
        self.game = game



    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            self.laser_activated = True

            
    def update_sprites(self,path):
        self.path = path

        self.sprite_names = os.listdir(self.path) # Not images
        self.sprites = []

        counter = 1
        for image in self.sprite_names:
            image = pygame.image.load(path+f"Player{counter}.png")
            self.sprites.append(image)
            counter += 1

            self.image = pygame.image.load(path+"Player1.png")

            
    def fire_laser(self):
        if self.game.powerup == 4:
            laser = Laser((self.rect.centerx,self.rect.centery),5,self.screen_height,f"Sprites/Bullet_Sprites/Bullet2.png",0,self)
        elif self.game.powerup == 3:
            laser = Laser((self.rect.centerx,self.rect.centery),5,self.screen_height,f"Sprites/Bullet_Sprites/Bullet3.png",0,self)
        else:
            laser = Laser((self.rect.centerx,self.rect.centery),5,self.screen_height,f"Sprites/Bullet_Sprites/Bullet1.png",0,self)
        self.lasers_group.add(laser)
        self.laser_time = pygame.time.get_ticks()
        self.laser_sound.play()




    
    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

        if self.game.powerup == 3:
            self.animation_speed = 50
        else:
            self.animation_speed = 200

        if pygame.time.get_ticks() - self.last_update > self.non_linear_animation_speed: # This if statment makes sure the sprite does not update every frame
            
            self.last_update = pygame.time.get_ticks()


            if self.current_image_index != len(self.sprites) and self.laser_activated == True:
                self.non_linear_animation_speed = self.non_linear_animation_speed * 0.8

                self.image = self.sprites[self.current_image_index]
                self.current_image_index = self.current_image_index+1

            elif self.current_image_index == len(self.sprites) and self.laser_activated == True:

                ## Fire the Laser ##

                self.fire_laser()
                if self.game.powerup == 4:
                    self.fire_laser()
                    self.fire_laser()
                    self.fire_laser()


                self.non_linear_animation_speed = self.animation_speed

                self.image = self.sprites[0]
                self.current_image_index = 1
                self.laser_activated = False


    
    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset/2:
            self.rect.left = self.offset/2
    
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True
            
    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2,self.screen_height - self.offset))
        self.lasers_group.empty()