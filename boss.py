import pygame
import os

class Boss(pygame.sprite.Sprite):

    def __init__(self, x, y,speed,screen_width, screen_height,offset,laser,game,spaceship): 
        super().__init__()
        self.type = type

        self.paths = {1: f"Sprites/Boss_1_Sprites", 2: f"Sprites/Boss_2_Sprites", 3: f"Sprites/Boss_3_Sprites"}

        self.sprites = {}

        for i in range(1,4): # For some silly reason 1,3 only counts 1,2
            self.sprites[i] = {}
            self.sprite_names = os.listdir(self.paths[i]) # Not images
            counter = 1
            for image in self.sprite_names:
                image = pygame.image.load(f"Sprites/Boss_{i}_Sprites/Boss{counter}.png")

                self.sprites[i][counter-1] = image
                counter += 1

        self.image = self.sprites[1][0]
        self.current_image_index = 0
        self.rect = self.image.get_rect(topleft = (x,y))

        self.ANIMATION_SPEED = speed
        self.last_update = 0
        self.last_phase_update = pygame.time.get_ticks()
        self.last_move = 0
        self.speed = 1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.direction = 1
        
        self.phase = 1
        self.is_firing = True
        self.shots_fired = 0
        self.hp = 50
        self.laser = laser
        self.spaceship = spaceship
        self.PHASE_ONE_SPEED = 10000
        self.PHASE_TWO_SPEED = 10000
        self.PHASE_THREE_SPEED = 10000

        self.game = game

        


    def update(self):

        contact = False # This needs to be set to false otherwise the boss will move every frame

        if self.rect.right >= self.screen_width + self.offset/2:
            self.direction = -1
            contact = True

                
        elif self.rect.left <= self.offset/2:
            self.direction = 1
            contact = True


        ## Movement ##

        if pygame.time.get_ticks() - self.last_move > 100 or contact: # Contact esures that the sprite still moves of the wall
            self.last_move = pygame.time.get_ticks()
            self.rect.x += self.speed * self.direction


        ## Animation ##
        
        if pygame.time.get_ticks() - self.last_update > self.ANIMATION_SPEED: # This if statment makes sure the sprite does not update every frame
            
            if self.is_firing == False or self.is_firing == True and pygame.time.get_ticks() - self.last_update > self.ANIMATION_SPEED:
                self.last_update = pygame.time.get_ticks()

                if self.phase == 1:
                    if pygame.time.get_ticks() - self.last_phase_update > self.PHASE_ONE_SPEED:
                        self.is_firing = False
                        

                    if self.current_image_index < 5:
                        self.image = self.sprites[1][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                   
                    elif self.is_firing == True:

                        if self.current_image_index == 4:
                            self.image = self.sprites[1][4]
                            self.rect = self.image.get_rect(topleft = self.rect.topleft)
                            self.current_image_index = 5
                        elif self.current_image_index == 5:
                            laser_sprite = self.laser((self.rect.centerx+85,self.rect.centery), -6,self.screen_height,f"Sprites/Bullet_Sprites/Boss_Bullet_1.png",10,self.spaceship)
                            self.game.aliens_lasers_group.add(laser_sprite)
                            laser_sprite = self.laser((self.rect.centerx-75,self.rect.centery), -6,self.screen_height,f"Sprites/Bullet_Sprites/Boss_Bullet_1.png",10,self.spaceship)
                            self.game.aliens_lasers_group.add(laser_sprite)
                            
                            self.image = self.sprites[1][5]
                            self.rect = self.image.get_rect(topleft = self.rect.topleft)
                            self.current_image_index = 4

                    elif self.is_firing == False and self.current_image_index < 9:
                        self.image = self.sprites[1][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                    else:
                        self.current_image_index = 0
                        self.phase = 2
                        self.last_phase_update = pygame.time.get_ticks()

                        

            

                elif self.phase == 2:
                    if pygame.time.get_ticks() - self.last_phase_update > self.PHASE_TWO_SPEED:
                        self.current_image_index = 0
                        self.phase = 3
                        self.last_phase_update = pygame.time.get_ticks()
                        self.is_firing = True


                    if self.current_image_index != len(self.sprites[2]):
                        self.image = self.sprites[2][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1

                    else:
                        self.image = self.sprites[2][0]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = 1

                elif self.phase == 3:
                    if pygame.time.get_ticks() - self.last_phase_update > self.PHASE_THREE_SPEED:
                        self.is_firing = False
                        

                    if self.current_image_index < 2:
                        self.image = self.sprites[3][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                   
                    elif self.is_firing == True and self.current_image_index == 2:
                            self.image = self.sprites[3][4]
                            self.rect = self.image.get_rect(topleft = self.rect.topleft)
                            laser_sprite = self.laser((self.rect.centerx-10,self.rect.centery), -3,self.screen_height,f"Sprites/Bullet_Sprites/Boss_Bullet_2.png",11,self.spaceship)
                            self.game.aliens_lasers_group.add(laser_sprite)

                    elif self.is_firing == False and self.current_image_index < 6:
                        self.image = self.sprites[3][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                    else:
                        self.current_image_index = 0
                        self.phase = 1
                        self.last_phase_update = pygame.time.get_ticks()
                        self.is_firing = True

            
