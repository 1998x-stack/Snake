import pygame
from typing import List, Tuple

class Snake:
    def __init__(self, initial_position: Tuple[int, int], grid_size: int = 20, initial_length: int = 3):
        """
        Initializes the snake's attributes when a new instance is created.
        
        :param initial_position: The starting position of the snake's head.
        :param grid_size: The size of the grid (used to align the snake on the grid).
        :param initial_length: The initial length of the snake.
        """
        self.grid_size = grid_size
        self.direction = (1, 0)  # Start by moving right
        self.body = [(
            initial_position[0] - i * grid_size, initial_position[1]
        ) for i in range(initial_length)]
        self.speed = 10  # Snake's movement speed (can be adjusted)

    def move(self):
        """
        Updates the snake's position on the screen by moving it in the current direction.
        """
        # Calculate new head position
        new_head = (
            self.body[0][0] + self.direction[0] * self.grid_size,
            self.body[0][1] + self.direction[1] * self.grid_size
        )
        # Insert new head position
        self.body.insert(0, new_head)
        # Remove the last segment unless snake has eaten
        self.body.pop()

    def grow(self):
        """
        Increases the length of the snake when it eats food.
        """
        # Add a new segment to the snake by not removing the tail
        new_head = (
            self.body[0][0] + self.direction[0] * self.grid_size,
            self.body[0][1] + self.direction[1] * self.grid_size
        )
        self.body.insert(0, new_head)

    def check_collision(self, screen_width: int, screen_height: int) -> bool:
        """
        Detects whether the snake has collided with the boundaries of the screen or itself.
        
        :param screen_width: The width of the game screen.
        :param screen_height: The height of the game screen.
        :return: True if the snake has collided (game over), False otherwise.
        """
        head_x, head_y = self.body[0]

        # 检查是否碰撞到墙壁
        if (head_x < 0 or head_x >= screen_width or
            head_y < 0 or head_y >= screen_height):
            return True

        # 检查是否与自身碰撞
        if self.body[0] in self.body[1:]:
            return True

        return False

    def change_direction(self, new_direction: Tuple[int, int]):
        """
        Updates the snake's direction based on player input while ensuring the snake doesn't reverse into itself.
        
        :param new_direction: The new direction to move in (tuple).
        """
        # Prevent the snake from reversing
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
            print(f"Direction changed to: {self.direction}")

    def draw(self, screen):
        """
        Renders the snake on the screen.
        
        :param screen: The Pygame display surface where the snake will be rendered.
        """
        for segment in self.body:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], self.grid_size, self.grid_size))