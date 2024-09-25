import pygame
from typing import Tuple, List
from utils import random_position

class Food:
    def __init__(self, screen_width: int, screen_height: int, grid_size: int, color: Tuple[int, int, int] = (255, 0, 0)):
        """
        Initializes the food object with a starting position and color.
        
        :param screen_width: The width of the game screen.
        :param screen_height: The height of the game screen.
        :param grid_size: The size of the grid (used to align the food on the grid).
        :param color: The color of the food (default is red).
        """
        self.grid_size = grid_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = color
        self.position = random_position(grid_size, screen_width, screen_height)
    
    def respawn(self, snake_body: List[Tuple[int, int]]):
        """
        Repositions the food to a new random location on the screen.
        
        :param snake_body: A list of tuples representing the coordinates of the snake's body.
        """
        while True:
            new_position = random_position(self.grid_size, self.screen_width, self.screen_height)
            if new_position not in snake_body:
                self.position = new_position
                break
    
    def draw(self, screen):
        """
        Renders the food on the screen at its current position.
        
        :param screen: The Pygame display surface where the food will be rendered.
        """
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.grid_size, self.grid_size))