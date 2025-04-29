## Python Modules And Imports ##

import pygame, sys

## Initialize  Modules

pygame.init()

## Constants ##

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

GREY = (29,29,27)

## Display ##

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Python Space Invaders")

## Clock ##

clock = pygame.time.Clock()

def main():
    
    while True:

        ## Even Handling ##

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        ## Drawing ##

        screen.fill(GREY)

        ## Update The Display ##

        pygame.display.update()
        clock.tick()




main()