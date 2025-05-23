import pygame,random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip

class Game:

    def __init__(self,screen_width,screen_height,offset):

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width,self.screen_height,self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.aliens_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 2

        gap = (self.screen_width + self.offset*3 - (3 * obstacle_width))/5
        obstacles = []
        for i in range(3):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 130)
            obstacles.append(obstacle)
        return obstacles
    
    def create_aliens(self):
        for row in range(5): 
            for column in range(10): 

                x = 25 + column * 40
                y = 25 + row * 40
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
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(2)
                
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(2)


    def alien_move_down(self,distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6,self.screen_height,f"Sprites/Enemy_Bullet_Sprites/")
            self.aliens_lasers_group.add(laser_sprite)
        
    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width,self.offset/2))

    def check_for_collisions(self):

        ## Spaceship ##

        if self.spaceship_group.sprite.lasers_group: # For player lasers
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True):
                    laser_sprite.kill()
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite,obstacle.blocks_group,True):
                        laser_sprite.kill()
        
        ## Aliens ##

        if self.aliens_lasers_group: # For alien lasers
                    
            for alien_laser_sprite in self.aliens_lasers_group: 

                if pygame.sprite.spritecollide(alien_laser_sprite,self.spaceship_group, False): # Checks for the player
                    alien_laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:

                    if pygame.sprite.spritecollide(alien_laser_sprite,obstacle.blocks_group,False):
                        
                        alien_laser_sprite.rect.y += 10 # Moves the laser down a bit so the hole is deeper

                        for pixel in obstacle.blocks_group:

                            ## Now get rid of obstacle parts in a small area otherwise only one pixel will be destroyed ##

                            pygame.sprite.spritecollide(alien_laser_sprite,obstacle.blocks_group,True) ## Gets rid of all pixels in the obstacle touching the laser


                        alien_laser_sprite.kill()


        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien,self.spaceship_group, False): # Checks for the player
                    self.game_over()

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