## Python Modules And Imports ##

import pygame, sys, random 
from game import Game

## Initialize  Modules

pygame.init()

## Constants ##

SCREEN_WIDTH = 448
SCREEN_HEIGHT = 512
OFFSET = 25

BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (243, 216,63)
NAVY_BLUE = (0, 0, 128)

## Fonts ##

font = pygame.font.Font("Fonts/ElectronPulse-9Yn42.ttf", 20)
level_surface = font.render("LEVEL 01", False, BLUE)
game_over_surface = font.render("GAME OVER", False, BLUE)
score_text_surface = font.render("SCORE:", False, BLUE)
highscore_text_surface = font.render("HIGH-SCORE:", False, BLUE)

## Display ##

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET,SCREEN_HEIGHT + OFFSET))
pygame.display.set_caption("Python Space Invaders")

## Clock ##

clock = pygame.time.Clock()

## Game  ##

game = Game(SCREEN_WIDTH,SCREEN_HEIGHT,OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER,2000)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP,random.randint(8000,13000))

def main():
    
    while True:

        ## Even Handling ##

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        

            if event.type == SHOOT_LASER and game.run:
                game.alien_shoot_laser()
            
            if event.type == MYSTERYSHIP and game.run:
                game.create_mystery_ship()
                pygame.time.set_timer(MYSTERYSHIP, random.randint(8000,13000))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and game.run == False:
                game.reset()
         
        ## Updating ##
        if game.run:
            game.spaceship_group.update()
            game.move_aliens()
            game.aliens_lasers_group.update()
            game.mystery_ship_group.update()
            game.explosions_group.update()
            game.powerup_group.update()
            game.check_for_collisions()
            game.check_for_powerups()
            game.shields_group.update()

        ## Drawing ##
        screen.fill(WHITE)

        # UI #
        pygame.draw.rect(screen,BLUE, (5,5,458,527),2,0,10,10,10,10)
        pygame.draw.line(screen,BLUE, (20, 489), (445, 489), 3)

        if game.run:
            screen.blit(level_surface, (300,500,20,20))
        else:
            screen.blit(game_over_surface, (300,500,20,20))

        x = 50
        for life in range(game.lives):
            screen.blit(pygame.image.load(f"Sprites/Heart_Sprites/Heart.png"),(x,493))
            x += 50

        screen.blit(score_text_surface,(15,10,50,50))
        formated_score = str(game.score).zfill(5)
        score_surface = font.render(str(formated_score), False, BLUE)
        screen.blit(score_surface,(100,10,50,50))
        screen.blit(highscore_text_surface, (250,10,50,50))
        formated_highscore = str(game.high_score).zfill(5)
        high_score_surface = font.render(str(formated_highscore), False, BLUE)
        screen.blit(high_score_surface,(380,10,50,50))



        game.spaceship_group.sprite.lasers_group.draw(screen)
        game.aliens_lasers_group.draw(screen)
        game.spaceship_group.draw(screen)
        game.aliens_group.draw(screen)
        game.mystery_ship_group.draw(screen)
        game.explosions_group.draw(screen)
        game.powerup_group.draw(screen)
        game.shields_group.draw(screen)

        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)

        


        ## Update The Display ##

        pygame.display.update()
        clock.tick(60)




main()