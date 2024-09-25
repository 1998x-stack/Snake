import unittest, pygame
from food import Food
from utils import random_position

class TestFood(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a basic environment for each test.
        """
        self.screen_width = 200
        self.screen_height = 200
        self.grid_size = 20
        self.food = Food(screen_width=self.screen_width, screen_height=self.screen_height, grid_size=self.grid_size)

    def test_initial_position_within_bounds(self):
        """
        Test that the initial position of the food is within screen bounds.
        """
        x, y = self.food.position
        self.assertTrue(0 <= x < self.screen_width)
        self.assertTrue(0 <= y < self.screen_height)
        self.assertEqual(x % self.grid_size, 0)
        self.assertEqual(y % self.grid_size, 0)

    def test_respawn(self):
        """
        Test that respawn correctly places the food in a new valid position that doesn't overlap with the snake.
        """
        snake_body = [(20, 20), (40, 20), (60, 20)]
        original_position = self.food.position
        self.food.respawn(snake_body)
        new_position = self.food.position

        # Ensure the new position is within bounds and not overlapping with the snake
        self.assertNotEqual(original_position, new_position)
        self.assertNotIn(new_position, snake_body)
        self.assertTrue(0 <= new_position[0] < self.screen_width)
        self.assertTrue(0 <= new_position[1] < self.screen_height)
        self.assertEqual(new_position[0] % self.grid_size, 0)
        self.assertEqual(new_position[1] % self.grid_size, 0)

    def test_random_position(self):
        """
        Test that random_position generates a position within bounds and aligned with the grid.
        """
        for _ in range(10):
            position = random_position(self.grid_size, self.screen_width, self.screen_height)
            self.assertTrue(0 <= position[0] < self.screen_width)
            self.assertTrue(0 <= position[1] < self.screen_height)
            self.assertEqual(position[0] % self.grid_size, 0)
            self.assertEqual(position[1] % self.grid_size, 0)

    def test_draw(self):
        """
        Test that the draw function does not raise any errors.
        """
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        try:
            self.food.draw(screen)
        except Exception as e:
            self.fail(f"draw() raised {e.__class__.__name__} unexpectedly!")

if __name__ == '__main__':
    unittest.main()