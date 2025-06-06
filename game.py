## Importing Things ##

import pygame,random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grids
from alien import Alien
from laser import Laser
from alien import MysteryShip
from explosion import Explosion
from powerup import Powerup
from shield import Shield
from boss import Boss
from target import Target

class Game:

    def __init__(self,screen_width,screen_height,offset):

        ## Setting Up Useful Variables, Functions And More ##

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width,self.screen_height,self.offset,self))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.shields_group = pygame.sprite.Group()
        self.explosions_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.aliens_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.target_group = pygame.sprite.Group()
        self.lives = 3
        self.run = True
        self.score = 0
        self.high_score = 0

        ## Music And Sounds

        self.explosion_sound = pygame.mixer.Sound("Sounds/8-bit-bomb-explosion.wav")
        self.powerup_sound = pygame.mixer.Sound("Sounds/8-bit-laser-151672.mp3")
        self.load_highscore()
        pygame.mixer.music.load("Sounds/music2.mp3")
        pygame.mixer.music.play(-1)

        ## Random But Useful Variables ##

        self.orignal_alien_group_length = len(self.aliens_group)
        self.powerup = False
        self.powerup_text = "sudo -su"
        self.Alien_speed = 1000 
        self.alien_move_distance = 10
        self.powerup_start_time = 0 
        self.boss_start_countdown = 0 
        self.boss_countdown = False
        self.boss_active = False
        self.boss_group = pygame.sprite.GroupSingle()
        self.game_won = False
        self.time_till_boss = 0
        self.last_target = pygame.time.get_ticks()
        

    def create_obstacles(self): # Creates all 3 obstacles for the game.

        ## A Bunch Of Complicated List Stuff To Make The Obstacles ##

        obstacle_width = len(grids[0]) * 2

        gap = (self.screen_width + self.offset*3 - (3 * obstacle_width))/5
        obstacles = []
        for i in range(3):
            offset_x = (i + 1) * gap + i * obstacle_width - 10
            obstacle = Obstacle(offset_x, self.screen_height - 130,str(i))
            obstacles.append(obstacle)
        return obstacles
    
    def create_aliens(self):

        ## Creates All The Aliens ##

        for row in range(5): 
            for column in range(10): 

                x = 25 + column * 40
                y = 35 + row * 40
                speed = 0
                if row == 0:
                    alien_type = 3
                    speed = 500
                elif row in (1,2):
                    alien_type = 2
                    speed = 500

                else:
                    alien_type = 1
                    speed = 500



                alien = Alien(alien_type,speed, x + self.offset/2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):

        ## Acts Like A Controller Telling The Aliens To Move ##

        contact = False

        alien_sprites = self.aliens_group.sprites()
        
        for alien in alien_sprites:

            ## Moves The Aliens Down ##

            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(5)
                contact = True

                
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(5)
                contact = True

        self.aliens_group.update(self.aliens_direction,contact,self.Alien_speed,self.alien_move_distance) # Gives the aliens important things to know.


    def alien_move_down(self,distance):
        
        ## Tells The Aliens T Move Down

        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):

        ## Picks A Random Alien To Shoot The Laser ##

        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6,self.screen_height,f"Sprites/Bullet_Sprites/Enemy_Bullet_{random_alien.type}.png",random_alien.type,self.spaceship_group.sprite)
            self.aliens_lasers_group.add(laser_sprite)
        
    def create_mystery_ship(self): # Simple, creates the mystery ship
        self.mystery_ship_group.add(MysteryShip(self.screen_width,self.offset/2))
    
    def create_boss(self):
        ## Creates The Boss Once 31 Seconds Have Past, However Gets Run Every Frame ##
        if self.boss_active == False:
            self.time_till_boss = 31000 - (pygame.time.get_ticks() - self.boss_start_countdown)
            if pygame.time.get_ticks() - self.boss_start_countdown > 31000:

                ## Spawns In The Boss ##

                self.obstacles = self.create_obstacles()
                self.target_group.empty()
                self.boss_active = True
                self.boss_countdown = False
                self.boss_group.add(Boss(100,100,200,self.screen_width,self.screen_height,self.offset,Laser,self,self.spaceship_group.sprite))
                self.lives = 3

    def check_for_boss(self):
        ## Similar To Create Boss, However It Tells The Game To Start The Boss Countdown And Gets Other Important Things Ready ##
        if len(self.aliens_group) == 0:
            if self.boss_active == False:
                if self.boss_countdown == False:
                    self.boss_countdown = True
                    self.boss_start_countdown = pygame.time.get_ticks()
                    pygame.mixer.music.load("Sounds/2021-08-30_-_Boss_Time_-_www.FesliyanStudios.com.mp3")
                    pygame.mixer.music.play(-1)
                    self.lives = 3

                self.create_boss()

        if self.boss_active == True: # Checks If The Player Has Won.
            if self.boss_group.sprite.hp <= 0:
                self.boss_group.sprite.kill()
                self.boss_active = False
                self.game_won = True
                self.boss_countdown = False

    def create_targets(self): ## Will Spawn Targets During The Boss Countdown ##
        if self.boss_countdown == True and self.game_won == False:
            if pygame.time.get_ticks() - self.last_target > 2000:
                self.last_target = pygame.time.get_ticks()
                target =  Target(random.randint(0,400),random.randint(0,400))
                self.target_group.add(target)

    def check_for_collisions(self):

        ## Spaceship ##

        if self.spaceship_group.sprite.lasers_group: # For lasers fired by the player.

            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, False)
                targets_hit = pygame.sprite.spritecollide(laser_sprite, self.target_group, False)

                if self.boss_active == True: 
                    boss_hit = pygame.sprite.spritecollide(laser_sprite, self.boss_group, False)

                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, False): # Spawns a powerup and gives points when the player shoots the mystery ship
                    self.powerup_group.add(Powerup((self.mystery_ship_group.sprite.rect.centerx,self.mystery_ship_group.sprite.rect.centery),2))
                    self.score += 500
                    self.explosion_sound.play()
                    self.explosion_sound.set_volume(0.15)
                    self.check_for_highscore()
                    laser_sprite.kill()
                    self.mystery_ship_group.sprite.kill()

                if self.boss_active == True: # Handles shots fired at the boss
                    for boss in boss_hit:
                        if boss_hit:
                            boss.hp -= 1
                            self.explosion_sound.play()
                            self.explosion_sound.set_volume(0.15)
                            laser_sprite.kill()
                            self.explosions_group.add(Explosion((laser_sprite.rect.centerx,laser_sprite.rect.centery)))

                            if self.powerup == 4: 
                                self.spaceship_group.sprite.lasers_group.empty()

                    enemy_bullets_hit = pygame.sprite.spritecollide(laser_sprite,self.aliens_lasers_group, False)

                    for bullet in enemy_bullets_hit: # Allows the player to shoot the bosses bullets.
                        if bullet.type == 11:
                            bullet.kill()
                            laser_sprite.kill()
 
                if aliens_hit: # Handles the player shooting the aliens.
                    self.explosion_sound.play()
                    self.explosion_sound.set_volume(0.15)
                    for alien in aliens_hit:
                        if alien.contains_powerup == True: 
                            self.powerup_group.add(Powerup((alien.rect.centerx,alien.rect.centery),1))
                        
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()
                        self.explosions_group.add(Explosion((alien.rect.centerx,alien.rect.centery)))
                        alien.kill()
                        self.Alien_speed -= 15

                if targets_hit: # Handles the player shooting targets.
                    self.explosion_sound.play()
                    self.explosion_sound.set_volume(0.15)
                    for target in targets_hit:
                        self.score += 500
                        self.check_for_highscore()
                        laser_sprite.kill()
                        self.explosions_group.add(Explosion((target.rect.centerx,target.rect.centery)))
                        target.kill()

                
                if self.boss_countdown == False: ## Alows the player to damage their obstacles.
                    for obstacle in self.obstacles:
                        if pygame.sprite.spritecollide(laser_sprite,obstacle.blocks_group,True):
                            laser_sprite.kill()
                
        ## Aliens ##
        
        if self.aliens_lasers_group: # Handles alien lasers.
                    
            for alien_laser_sprite in self.aliens_lasers_group: 

                if pygame.sprite.spritecollide(alien_laser_sprite,self.shields_group,False) and self.boss_active == False: # Allows the bullets to bounce off shields.
                    alien_laser_sprite.rect.x -= 30
                    alien_laser_sprite.speed =  alien_laser_sprite.speed * -1
                    alien_laser_sprite.bounced = True
                    alien_laser_sprite.flipped = True

                
                if pygame.sprite.spritecollide(alien_laser_sprite,self.spaceship_group, False): # Checks for the player.
                    alien_laser_sprite.kill()
                    self.explosion_sound.play()
                    self.explosion_sound.set_volume(0.15)
                    self.explosions_group.add(Explosion((alien_laser_sprite.rect.centerx,alien_laser_sprite.rect.centery)))
                    if self.powerup == False or 2 or self.boss_active: # Damages the player if they have no player shield powerup, or if the boss shoots them.
                        self.lives -= 1
                        if self.lives == 0:
                            self.game_over()

                if self.powerup != False and alien_laser_sprite.bounced == True: # This allows the alien bullets to shoot aliens if they have been bounced.

                    aliens_hit = pygame.sprite.spritecollide(alien_laser_sprite, self.aliens_group, False)

                    if aliens_hit:
                        self.explosion_sound.play()
                        self.explosion_sound.set_volume(0.15)
                        for alien in aliens_hit:
                            if alien.contains_powerup == True:
                                self.powerup_group.add(Powerup((alien.rect.centerx,alien.rect.centery),1))
                        
                            self.score += alien.type * 100
                            self.check_for_highscore()
                            alien_laser_sprite.kill()
                            self.explosions_group.add(Explosion((alien.rect.centerx,alien.rect.centery)))
                            alien.kill()


                if alien_laser_sprite.type != 3 and alien_laser_sprite.bounced == False and self.boss_countdown == False: # Allows the enemy lasers to damage the obstacles.

                    for obstacle in self.obstacles:
                            
                        if pygame.sprite.spritecollide(alien_laser_sprite,obstacle.blocks_group,False):
                            
                            alien_laser_sprite.rect.y += 10 # Moves the laser down a bit so the hole is deeper

                            for pixel in obstacle.blocks_group:

                                ## Now get rid of obstacle parts in a small area otherwise only one pixel will be destroyed ##

                                pygame.sprite.spritecollide(alien_laser_sprite,obstacle.blocks_group,True) ## Gets rid of all pixels in the obstacle touching the laser

                            self.explosions_group.add(Explosion((alien_laser_sprite.rect.centerx,alien_laser_sprite.rect.centery)))
                            alien_laser_sprite.kill()
                            self.explosion_sound.play()
                            self.explosion_sound.set_volume(0.15)

       
 

        if self.aliens_group and self.boss_countdown == False: # Allows the aliens to remove structures and kill the player by touch.
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien,self.spaceship_group, False): # Checks for the player
                    self.game_over()

        if self.powerup_group: # Allows the player to pick up powerups
            for powerup in self.powerup_group:
                if pygame.sprite.spritecollide(powerup,self.spaceship_group, False): # Checks for the player
                    self.clear_powerups()
                    self.powerup_sound.play(2)
                    self.powerup_sound.set_volume(0.15)
                    self.powerup = powerup.type
                    powerup.kill()
                    if self.powerup == 1:
                        self.shields_group.add(Shield(self.spaceship_group.sprite,False,1))
                    elif self.powerup == 2 and self.boss_countdown == False:
                        for obstacle in self.obstacles:
                            self.shields_group.add(Shield(False,obstacle.position,2))
                    elif self.powerup == 3:
                        self.shields_group.add(Shield(self.spaceship_group.sprite,False,3))
                    elif self.powerup == 4:
                        self.shields_group.add(Shield(self.spaceship_group.sprite,False,4))

                    self.powerup_start_time = pygame.time.get_ticks() 


    def clear_powerups(self): # Removes all powerups.
        for shield in self.shields_group:
                shield.kill()

        self.powerup = False
        self.powerup_start_time = 0
        self.spaceship_group.sprite.update_sprites(f"Sprites/Player_Sprites/")
            
    def check_for_powerups(self): # Removes powerups after 10 seconds.
        if self.powerup != False:
            if pygame.time.get_ticks() - self.powerup_start_time > 10000:
                self.clear_powerups()
                

    def game_over(self):
        self.run = False
    
    def reset(self): ## Resets the game to the original state.
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.aliens_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0
        self.Alien_speed = 1000
        self.boss_active = False
        self.boss_group.empty()
        self.boss_countdown = False
        self.boss_start_countdown = 0
        


    def check_for_highscore(self): # Checks if the score is greater than the current highscore.
        if self.score > self.high_score:
            self.high_score = self.score

        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def load_highscore(self): # Adds the players score to the highscore.
        try:
            with open("highscore.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0