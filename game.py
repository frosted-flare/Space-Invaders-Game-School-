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

class Game:

    def __init__(self,screen_width,screen_height,offset):

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width,self.screen_height,self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.shields_group = pygame.sprite.Group()
        self.explosions_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.aliens_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.high_score = 0
        self.explosion_sound = pygame.mixer.Sound("Sounds/8-bit-bomb-explosion.wav")
        self.powerup_sound = pygame.mixer.Sound("Sounds/8-bit-laser-151672.mp3")
        self.load_highscore()
        pygame.mixer.music.load("Sounds/music2.mp3")
        pygame.mixer.music.play(-1)
        self.orignal_alien_group_length = len(self.aliens_group)
        self.powerup = False
        self.powerup_text = "sudo -su"

        self.ALIEN_SPEED = 1000 
        self.alien_move_distance = 10
        self.powerup_start_time = 0 

    def create_obstacles(self):
        obstacle_width = len(grids[0]) * 2

        gap = (self.screen_width + self.offset*3 - (3 * obstacle_width))/5
        obstacles = []
        for i in range(3):
            offset_x = (i + 1) * gap + i * obstacle_width - 10
            obstacle = Obstacle(offset_x, self.screen_height - 130,str(i))
            obstacles.append(obstacle)
        return obstacles
    
    def create_aliens(self):
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

        contact = False

        alien_sprites = self.aliens_group.sprites()
        
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(5)
                contact = True

                
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(5)
                contact = True

        self.aliens_group.update(self.aliens_direction,contact,self.ALIEN_SPEED,self.alien_move_distance)


    def alien_move_down(self,distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6,self.screen_height,f"Sprites/Bullet_Sprites/Enemy_Bullet_{random_alien.type}.png",random_alien.type,self.spaceship_group.sprite)
            self.aliens_lasers_group.add(laser_sprite)
        
    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width,self.offset/2))
    

    def check_for_collisions(self):

        ## Spaceship ##

        if self.spaceship_group.sprite.lasers_group: # For player lasers

            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, False)

                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, False):
                    self.powerup_group.add(Powerup((self.mystery_ship_group.sprite.rect.centerx,self.mystery_ship_group.sprite.rect.centery)))
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laser_sprite.kill()
                    self.mystery_ship_group.sprite.kill()


                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()
                        self.explosions_group.add(Explosion((alien.rect.centerx,alien.rect.centery)))
                        alien.kill()


                

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite,obstacle.blocks_group,True):
                        laser_sprite.kill()
        
        ## Aliens ##
        
        if self.aliens_lasers_group: # For alien lasers
                    
            for alien_laser_sprite in self.aliens_lasers_group: 

                if pygame.sprite.spritecollide(alien_laser_sprite,self.shields_group,False): # Checks for shields
                    alien_laser_sprite.rect.x -= 30
                    alien_laser_sprite.speed =  alien_laser_sprite.speed * -1
                    alien_laser_sprite.bounced = True
                    alien_laser_sprite.flipped = True


                
                if pygame.sprite.spritecollide(alien_laser_sprite,self.spaceship_group, False): # Checks for the player
                   
                    alien_laser_sprite.kill()
                    self.explosion_sound.play()
                    self.explosions_group.add(Explosion((alien_laser_sprite.rect.centerx,alien_laser_sprite.rect.centery)))
                    if self.powerup == False:
                        self.lives -= 1
                        if self.lives == 0:
                            self.game_over()

                if self.powerup != False and alien_laser_sprite.bounced == True:

                    aliens_hit = pygame.sprite.spritecollide(alien_laser_sprite, self.aliens_group, False)

                    if aliens_hit:
                        self.explosion_sound.play()
                        for alien in aliens_hit:
                            self.score += alien.type * 100
                            self.check_for_highscore()
                            alien_laser_sprite.kill()
                            self.explosions_group.add(Explosion((alien.rect.centerx,alien.rect.centery)))
                            alien.kill()


                if alien_laser_sprite.type != 3 and alien_laser_sprite.bounced == False:

                    for obstacle in self.obstacles:
                            
                        if pygame.sprite.spritecollide(alien_laser_sprite,obstacle.blocks_group,False):
                            
                            alien_laser_sprite.rect.y += 10 # Moves the laser down a bit so the hole is deeper

                            for pixel in obstacle.blocks_group:

                                ## Now get rid of obstacle parts in a small area otherwise only one pixel will be destroyed ##

                                pygame.sprite.spritecollide(alien_laser_sprite,obstacle.blocks_group,True) ## Gets rid of all pixels in the obstacle touching the laser

                            self.explosions_group.add(Explosion((alien_laser_sprite.rect.centerx,alien_laser_sprite.rect.centery)))
                            alien_laser_sprite.kill()
                            self.explosion_sound.play()


        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien,self.spaceship_group, False): # Checks for the player
                    self.game_over()

        if self.powerup_group:
            for powerup in self.powerup_group:
                if pygame.sprite.spritecollide(powerup,self.spaceship_group, False): # Checks for the player
                    self.powerup_sound.play(2)
                    self.powerup = powerup.type
                    powerup.kill()
                    if self.powerup == 1:
                        self.shields_group.add(Shield(self.spaceship_group.sprite,False,1))
                    elif self.powerup == 2:
                        for obstacle in self.obstacles:
                            self.shields_group.add(Shield(False,obstacle.position,2))

                    self.powerup_start_time = pygame.time.get_ticks() 

    def check_for_powerups(self):
        if self.powerup != False:
            if pygame.time.get_ticks() - self.powerup_start_time > 10000:
                for shield in self.shields_group:
                    shield.kill()

                self.powerup = False
                self.powerup_start_time = 0
                self.spaceship_group.sprite.update_sprites(f"Sprites/Player_Sprites/")
                

    def game_over(self):
        self.run = False
    
    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.aliens_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def check_for_highscore(self):
        if self.score > self.high_score:
            self.high_score = self.score

        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0