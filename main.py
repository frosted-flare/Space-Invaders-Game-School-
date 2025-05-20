## Python Modules And Imports ##

import pygame, sys, random 
from game import Game

## Initialize  Modules

pygame.init()

## Constants ##

SCREEN_WIDTH = 448
SCREEN_HEIGHT = 512

BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

## Display ##

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Python Space Invaders")

## Clock ##

clock = pygame.time.Clock()

## Game  ##

game = Game(SCREEN_WIDTH,SCREEN_HEIGHT)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER,1000)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP,random.randint(10000,15000))

def main():
    
    while True:

        ## Even Handling ##

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        

            if event.type == SHOOT_LASER:
                game.alien_shoot_laser()
            
            if event.type == MYSTERYSHIP:

                game.create_mystery_ship()
                pygame.time.set_timer(MYSTERYSHIP, random.randint(10000,15000))
         
        ## Updating ##

        game.spaceship_group.update()
        game.move_aliens()
        game.aliens_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

        ## Drawing ##

        screen.fill(WHITE)
        game.spaceship_group.sprite.lasers_group.draw(screen)
        game.aliens_lasers_group.draw(screen)
        game.spaceship_group.draw(screen)

        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)

        game.aliens_group.draw(screen)
        game.mystery_ship_group.draw(screen)

        ## Update The Display ##

        pygame.display.update()
        clock.tick(60)




main()