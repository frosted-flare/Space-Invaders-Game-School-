import pygame
import os

class Boss(pygame.sprite.Sprite):

    def __init__(self, x, y,speed,screen_width, screen_height,offset,laser,game,spaceship): 
        super().__init__()
        self.type = type

        self.paths = {1: f"Sprites/Boss_1_Sprites", 2: f"Sprites/Boss_2_Sprites", 3: f"Sprites/Boss_3_Sprites"} # Uses a dictionary to store many different phases.

        ## Sprites

        self.sprites = {}

        for i in range(1,4): # Has to be 1,4 because for some silly reason 1,3 only counts up to 2.

            ## Adds all the sprites to the sprites dictionary ##

            self.sprites[i] = {}
            self.sprite_names = os.listdir(self.paths[i]) # Does Not list images, only lists names.
            counter = 1
            for image in self.sprite_names:
                image = pygame.image.load(f"Sprites/Boss_{i}_Sprites/Boss{counter}.png")

                self.sprites[i][counter-1] = image 
                counter += 1

        self.image = self.sprites[1][0]
        self.current_image_index = 0
        self.rect = self.image.get_rect(topleft = (x,y))

        ## Important Variables ##

        self.ANIMATION_SPEED = speed
        self.last_update = 0
        self.last_phase_update = pygame.time.get_ticks()
        self.last_move = 0
        self.speed = 1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.direction = 1
        self.game = game
        self.spaceship = spaceship
        self.laser = laser

        ## Boss Fight Related Variables
        
        self.phase = 1
        self.is_firing = True
        self.shots_fired = 0
        self.hp = 100
        self.glich_bullets_spawned = 0


        ## Phase Speeds Are For How Long Each Phase Should Last ##

        self.PHASE_ONE_SPEED = 10000
        self.PHASE_TWO_SPEED = 10000
        self.PHASE_THREE_SPEED = 10000


        


    def update(self):

        contact = False # This needs to be set to false otherwise the boss will move every frame.

        if self.rect.right >= self.screen_width + self.offset/2:
            self.direction = -1
            contact = True

                
        elif self.rect.left <= self.offset/2:
            self.direction = 1
            contact = True


        ## Movement ##

        if pygame.time.get_ticks() - self.last_move > 100 or contact: # Contact ensures that the sprite still moves of the wall.
            self.last_move = pygame.time.get_ticks()
            self.rect.x += self.speed * self.direction


        ## Animation ##
        
        if pygame.time.get_ticks() - self.last_update > self.ANIMATION_SPEED: # This if statment makes sure the sprite does not update every frame
            
            if self.is_firing == False or self.is_firing == True and pygame.time.get_ticks() - self.last_update > self.ANIMATION_SPEED: 
                self.last_update = pygame.time.get_ticks()

                if self.phase == 1:
                    if pygame.time.get_ticks() - self.last_phase_update > self.PHASE_ONE_SPEED: # This if statement ensures the boss can enter next phase, thus it is called first.
                        self.is_firing = False 
                        

                    if self.current_image_index < 5: # Unsures the first frames are played 1 by 1.
                        self.image = self.sprites[1][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                   
                    elif self.is_firing == True:  

                        ## This If Statement Alternates Between The 2 Animations ##
                        if self.current_image_index == 4:
                            self.image = self.sprites[1][4]
                            self.rect = self.image.get_rect(topleft = self.rect.topleft)
                            self.current_image_index = 5
                        elif self.current_image_index == 5:

                            ## Spawns 2 Lasers, As The Boss Has 2 Guns ##

                            laser_sprite = self.laser((self.rect.centerx+85,self.rect.centery), -6,self.screen_height,f"Sprites/Bullet_Sprites/Boss_Bullet_1.png",10,self.spaceship)
                            self.game.aliens_lasers_group.add(laser_sprite)
                            laser_sprite = self.laser((self.rect.centerx-75,self.rect.centery), -6,self.screen_height,f"Sprites/Bullet_Sprites/Boss_Bullet_1.png",10,self.spaceship)
                            self.game.aliens_lasers_group.add(laser_sprite)
                            
                            self.image = self.sprites[1][5]
                            self.rect = self.image.get_rect(topleft = self.rect.topleft)
                            self.current_image_index = 4

                    elif self.is_firing == False and self.current_image_index < 9:

                        ## This If Statement Ends The Animation And Gets Ready For Next Phase ## 

                        self.image = self.sprites[1][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                    else:

                        ## This If Statement Moves The Boss To The Next Phase ##                              

                        self.current_image_index = 0
                        self.phase = 2
                        self.last_phase_update = pygame.time.get_ticks()

                        

                

                elif self.phase == 2:
                    if pygame.time.get_ticks() - self.last_phase_update > self.PHASE_TWO_SPEED:

                        ## This If Statement Moves The Boss To Phase 3 ##

                        self.current_image_index = 0
                        self.phase = 3
                        self.last_phase_update = pygame.time.get_ticks()
                        self.is_firing = True

                    ## This If-Else Statements Loop Through All The Animation, No Firing Needed ##

                    if self.current_image_index != len(self.sprites[2]):
                        self.image = self.sprites[2][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1

                    else:
                        self.image = self.sprites[2][0]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = 1

                elif self.phase == 3:
                    if pygame.time.get_ticks() - self.last_phase_update > self.PHASE_THREE_SPEED: ## This Ensures The Boss Moves To The Next Phase ##
                        self.is_firing = False
                        
                    if self.current_image_index < 2:
                        ## This Part Gets The Animation Moving To The Firing Part ##
                        self.image = self.sprites[3][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                   
                    elif self.is_firing == True and self.current_image_index == 2 and self.glich_bullets_spawned <= 35: ## self.glich_bullets_spawned stops the boss from firing too much tracking bullets.
                        self.glich_bullets_spawned += 1 
                        self.image = self.sprites[3][4]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        laser_sprite = self.laser((self.rect.centerx-10,self.rect.centery+50), -3,self.screen_height,f"Sprites/Bullet_Sprites/Boss_Bullet_2.png",11,self.spaceship)
                        self.game.aliens_lasers_group.add(laser_sprite)

                    elif self.is_firing == False and self.current_image_index < 6: # Ends off the animation.
                        self.image = self.sprites[3][self.current_image_index]
                        self.rect = self.image.get_rect(topleft = self.rect.topleft)
                        self.current_image_index = self.current_image_index+1
                    else: # Moves to the next phase.
                        self.current_image_index = 0
                        self.phase = 1
                        self.last_phase_update = pygame.time.get_ticks()
                        self.is_firing = True
                        self.glich_bullets_spawned = 0


            
