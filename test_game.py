import unittest
import pygame
from game import Game
from advanced import Obstacle
from snake import Snake
from food import Food

class TestGame(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a basic environment for each test. Initializes the Game instance.
        """
        self.game = Game(screen_width=200, screen_height=200, grid_size=20)
    
    def test_initialization(self):
        """
        Test that the game initializes with the correct attributes.
        """
        self.assertEqual(self.game.screen.get_width(), 200)
        self.assertEqual(self.game.screen.get_height(), 200)
        self.assertEqual(self.game.snake.grid_size, 20)
        self.assertIsInstance(self.game.snake, Snake)
        self.assertIsInstance(self.game.food, Food)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)

    def test_process_events_quit(self):
        """
        Test that the game processes a QUIT event correctly.
        """
        # Simulate QUIT event
        for event in [pygame.event.Event(pygame.QUIT)]:
            pygame.event.post(event)
        self.game.process_events()
        self.assertTrue(self.game.game_over)

    def test_process_events_direction_change(self):
        """
        Test that the game processes direction change events correctly.
        """
        initial_direction = self.game.snake.direction

        # Simulate arrow key events to change direction
        for key, expected_direction in [
            (pygame.K_UP, (0, -1)),
            (pygame.K_DOWN, (0, 1)),
            (pygame.K_LEFT, (-1, 0)),
            (pygame.K_RIGHT, (1, 0))
        ]:
            event = pygame.event.Event(pygame.KEYDOWN, key=key)
            pygame.event.post(event)
            self.game.process_events()
            print(f"Expected direction: {expected_direction}, Actual direction: {self.game.snake.direction}")
            self.assertEqual(self.game.snake.direction, expected_direction)

        # Test that the direction does not change to the opposite (invalid move)
        opposite_direction = (-initial_direction[0], -initial_direction[1])
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT if initial_direction[0] == 1 else pygame.K_RIGHT)
        pygame.event.post(event)
        self.game.process_events()
        print(f"Testing invalid direction change. Initial direction: {initial_direction}, "
              f"Attempted direction: {opposite_direction}, Actual direction: {self.game.snake.direction}")
        self.assertNotEqual(self.game.snake.direction, opposite_direction)

    def test_update_collision_with_food(self):
        """
        Test that the snake eats the food and the score increases correctly.
        """
        # Set snake head on food position
        self.game.snake.body = [self.game.food.position]

        initial_score = self.game.score
        initial_snake_length = len(self.game.snake.body)

        self.game.update()

        # Debug information
        print(f"Snake head: {self.game.snake.body[0]}, Food position: {self.game.food.position}")
        print(f"Score after update: {self.game.score}, Snake length after update: {len(self.game.snake.body)}")

        self.assertEqual(self.game.score, initial_score + 1, "Score did not increase after eating food.")
        self.assertEqual(len(self.game.snake.body), initial_snake_length + 1, "Snake did not grow after eating food.")

    def test_update_collision_with_self(self):
        """
        Test that the game ends when the snake collides with itself.
        """
        # Create a situation where the snake will collide with itself
        self.game.snake.body = [(100, 100), (80, 100), (60, 100), (60, 120), (80, 120), (100, 120), (100, 100)]
        
        self.game.update()

        # Debug information
        print(f"Snake body: {self.game.snake.body}")
        print(f"Game over status after self-collision: {self.game.game_over}")

        self.assertTrue(self.game.game_over, "Game did not end after the snake collided with itself.")

    def test_update_collision_with_wall(self):
        """
        Test that the game ends when the snake collides with the wall.
        """
        # Move the snake's head outside the screen bounds
        self.game.snake.body = [(self.game.screen.get_width() + 20, 100)]
        
        self.game.update()

        # Debug information
        print(f"Snake head position: {self.game.snake.body[0]}, Screen width: {self.game.screen.get_width()}")
        print(f"Game over status after wall collision: {self.game.game_over}")

        self.assertTrue(self.game.game_over, "Game did not end after the snake collided with the wall.")

    def test_render(self):
        """
        Test that rendering does not raise any errors.
        """
        try:
            self.game.render()
        except Exception as e:
            print(f"Render raised an exception: {e}")
            self.fail(f"render() raised {e.__class__.__name__} unexpectedly!")

    def test_draw_score(self):
        """
        Test that the score is drawn on the screen without errors.
        """
        try:
            self.game.draw_score()
        except Exception as e:
            print(f"Draw score raised an exception: {e}")
            self.fail(f"draw_score() raised {e.__class__.__name__} unexpectedly!")

    def test_game_restart(self):
        """
        Test that the game can be restarted after game over.
        """
        # Simulate a game over scenario
        self.game.game_over = True
        
        # Simulate pressing 'R' to restart the game
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
        pygame.event.post(event)
        self.game.wait_for_restart_or_exit()

        # Debug information
        print(f"Game restarted. Game over status: {self.game.game_over}, Score: {self.game.score}, "
              f"Snake length: {len(self.game.snake.body)}")

        self.assertFalse(self.game.game_over, "Game did not restart correctly.")
        self.assertEqual(self.game.score, 0, "Score did not reset after restart.")
        self.assertEqual(len(self.game.snake.body), 3, "Snake length did not reset after restart.")  # Assuming the initial length is 3

    def test_obstacle_collision(self):
        """
        Test that the game ends when the snake collides with an obstacle.
        """
        # Place an obstacle directly in the snake's path
        self.game.obstacles.positions = [(120, 100)]
        self.game.snake.body = [(100, 100), (80, 100), (60, 100)]

        # Move the snake so it will collide with the obstacle
        self.game.snake.move()
        self.assertEqual(self.game.snake.body[0], (120, 100))

        self.game.update()

        # Debug information
        print(f"Snake head: {self.game.snake.body[0]}, Obstacle positions: {self.game.obstacles.positions}")
        print(f"Game over status after obstacle collision: {self.game.game_over}")

        self.assertTrue(self.game.game_over, "Game did not end after the snake collided with an obstacle.")

if __name__ == '__main__':
    unittest.main()