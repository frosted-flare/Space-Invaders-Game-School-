## Python Modules And Imports ##

import pygame, sys
from game import Game

## Initialize  Modules

pygame.init()

## Constants ##

SCREEN_WIDTH = 448
SCREEN_HEIGHT = 512

BLUE = (0,0,255)

## Display ##

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Python Space Invaders")

## Clock ##

clock = pygame.time.Clock()

## Game  ##

game = Game(SCREEN_WIDTH,SCREEN_HEIGHT)


def main():
    
    while True:

        ## Even Handling ##

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        
         
        ## Updating ##

        game.spaceship_group.update()

        ## Drawing ##

        screen.fill(BLUE)
        game.spaceship_group.sprite.lasers_group.draw(screen)
        game.spaceship_group.draw(screen)

        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)

        ## Update The Display ##

        pygame.display.update()
        clock.tick(60)




main()