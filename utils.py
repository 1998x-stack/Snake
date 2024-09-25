import pygame
import random
from typing import Tuple

def random_position(grid_size: int, screen_width: int, screen_height: int) -> Tuple[int, int]:
    """
    Generates a random position on the screen aligned with the grid.

    :param grid_size: The size of the grid (used to align the position on the grid).
    :param screen_width: The width of the game screen.
    :param screen_height: The height of the game screen.
    :return: A tuple representing the (x, y) position.
    """
    x = random.randint(0, (screen_width // grid_size) - 1) * grid_size
    y = random.randint(0, (screen_height // grid_size) - 1) * grid_size
    return (x, y)

def draw_text(screen, text: str, position: Tuple[int, int], font_size: int, color: Tuple[int, int, int] = (255, 255, 255)):
    """
    Renders text on the game screen.

    :param screen: The Pygame display surface where the text will be rendered.
    :param text: The string of text that needs to be displayed.
    :param position: A tuple (x, y) representing the position on the screen.
    :param font_size: The size of the font in which the text will be rendered.
    :param color: The color of the text (default is white).
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def initialize_game(screen_width: int, screen_height: int, grid_size: int):
    """
    Initializes the game state, including setting up the Pygame display, creating the snake, and food.

    :param screen_width: The width of the game screen.
    :param screen_height: The height of the game screen.
    :param grid_size: The size of the grid units.
    :return: A tuple containing the initialized screen, clock, snake, and food objects.
    """
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    from snake import Snake
    from food import Food

    snake = Snake(initial_position=(screen_width // 2, screen_height // 2), grid_size=grid_size)
    food = Food(screen_width=screen_width, screen_height=screen_height, grid_size=grid_size)

    return screen, clock, snake, food