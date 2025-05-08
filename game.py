import pygame
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid

class Game:

    def __init__(self,screen_width,screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width,self.screen_height))
        self.obstacles = self.create_obstacles()

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 2

        gap = (self.screen_width - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 110)
            obstacles.append(obstacle)
        return obstacles