import unittest
from snake import Snake

class TestSnake(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a basic environment for each test.
        """
        self.snake = Snake(initial_position=(100, 100), grid_size=20, initial_length=3)

    def test_initial_position(self):
        """
        Test that the snake initializes with the correct starting position and length.
        """
        expected_body = [(100, 100), (80, 100), (60, 100)]
        self.assertEqual(self.snake.body, expected_body)

    def test_move(self):
        """
        Test the snake's movement functionality.
        """
        self.snake.move()
        expected_body_after_move = [(120, 100), (100, 100), (80, 100)]
        self.assertEqual(self.snake.body, expected_body_after_move)

    def test_grow(self):
        """
        Test the snake's growth when it consumes food.
        """
        self.snake.grow()
        expected_body_after_grow = [(120, 100), (100, 100), (80, 100), (60, 100)]
        self.assertEqual(self.snake.body, expected_body_after_grow)

    def test_change_direction(self):
        """
        Test that the snake's direction changes correctly.
        """
        initial_direction = self.snake.direction

        # Change direction to UP
        self.snake.change_direction((0, -1))
        self.assertEqual(self.snake.direction, (0, -1))

        # Try to reverse direction to DOWN (should be ignored)
        self.snake.change_direction((0, 1))
        self.assertEqual(self.snake.direction, (0, -1))  # Direction should not change

    def test_check_collision_with_wall(self):
        """
        Test that collision with the walls is correctly detected.
        """
        # Place the snake just outside the screen bounds on the left side
        self.snake.body = [(-20, 100)]
        collision = self.snake.check_collision(screen_width=200, screen_height=200)
        self.assertTrue(collision)

        # Place the snake just outside the screen bounds on the right side
        self.snake.body = [(220, 100)]
        collision = self.snake.check_collision(screen_width=200, screen_height=200)
        self.assertTrue(collision)

        # Place the snake just outside the screen bounds on the top
        self.snake.body = [(100, -20)]
        collision = self.snake.check_collision(screen_width=200, screen_height=200)
        self.assertTrue(collision)

        # Place the snake just outside the screen bounds on the bottom
        self.snake.body = [(100, 220)]
        collision = self.snake.check_collision(screen_width=200, screen_height=200)
        self.assertTrue(collision)

    def test_check_collision_with_self(self):
        """
        Test that collision with itself is correctly detected.
        """
        # Create a situation where the snake collides with itself
        self.snake.body = [(100, 100), (80, 100), (60, 100), (60, 120), (80, 120), (100, 120), (100, 100)]
        collision = self.snake.check_collision(screen_width=200, screen_height=200)
        self.assertTrue(collision)

    def test_no_collision(self):
        """
        Test that no collision is detected when the snake is in a valid state.
        """
        collision = self.snake.check_collision(screen_width=200, screen_height=200)
        self.assertFalse(collision)

if __name__ == '__main__':
    unittest.main()