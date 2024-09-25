import pygame
import random
from typing import List, Tuple

class Obstacle:
    def __init__(self, screen_width: int, screen_height: int, grid_size: int, number_of_obstacles: int = 5):
        """
        Initializes the obstacle objects with random or predefined positions.
        
        :param screen_width: The width of the game screen.
        :param screen_height: The height of the game screen.
        :param grid_size: The size of the grid (used to align the obstacle on the grid).
        :param number_of_obstacles: The number of obstacles to generate.
        """
        self.grid_size = grid_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (139, 69, 19)  # Brown color for obstacles
        self.positions = self.generate_obstacles(number_of_obstacles)
    
    def generate_obstacles(self, number_of_obstacles: int) -> List[Tuple[int, int]]:
        """
        Generates a list of random positions for the obstacles on the grid.
        
        :param number_of_obstacles: The number of obstacles to generate.
        :return: A list of tuples representing the (x, y) positions of the obstacles.
        """
        positions = []
        for _ in range(number_of_obstacles):
            x = random.randint(0, (self.screen_width // self.grid_size) - 1) * self.grid_size
            y = random.randint(0, (self.screen_height // self.grid_size) - 1) * self.grid_size
            positions.append((x, y))
        return positions
    
    def draw(self, screen):
        """
        Renders the obstacles on the screen.
        
        :param screen: The Pygame display surface where the obstacles will be rendered.
        """
        for position in self.positions:
            pygame.draw.rect(screen, self.color, pygame.Rect(position[0], position[1], self.grid_size, self.grid_size))


class AdvancedGame:
    def __init__(self, screen_width=600, screen_height=400, grid_size=20):
        """
        Initializes the advanced game by creating the necessary game objects and setting up the environment.
        
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        :param grid_size: Size of the grid units.
        """
        pygame.init()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Advanced Snake Game')
        
        self.clock = pygame.time.Clock()
        self.snake = Snake(initial_position=(self.screen_width // 2, self.screen_height // 2), grid_size=self.grid_size)
        self.food = Food(screen_width=self.screen_width, screen_height=self.screen_height, grid_size=self.grid_size)
        self.obstacles = Obstacle(screen_width=self.screen_width, screen_height=self.screen_height, grid_size=self.grid_size)
        
        self.score = 0
        self.high_score = self.load_high_score()
        self.difficulty_level = 1
        self.game_over = False

    def load_high_score(self) -> int:
        """
        Loads the high score from a file or initializes it to 0 if the file doesn't exist.
        
        :return: The high score.
        """
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0
    
    def save_high_score(self):
        """
        Saves the current high score to a file.
        """
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))
    
    def process_events(self):
        """
        Handles all player inputs, primarily controlling the snake's direction.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
    
    def update(self):
        """
        Updates the game state, including the snake's movement, collision detection, and score management.
        """
        self.snake.move()
        
        # Check for collisions with walls, self, or obstacles
        if self.snake.check_collision(self.screen_width, self.screen_height) or \
                any(pos == self.snake.body[0] for pos in self.obstacles.positions):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
        
        # Check if the snake eats the food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 1
            self.adjust_difficulty()
    
    def adjust_difficulty(self):
        """
        Adjusts the game's difficulty level based on the score.
        """
        if self.score % 5 == 0:
            self.difficulty_level += 1
            self.snake.speed += 1  # Increase the snake's speed as difficulty increases
    
    def check_game_over(self):
        """
        Determines if the game has ended based on the current state of the game.
        """
        if self.game_over:
            self.render_game_over()
            self.wait_for_restart_or_exit()

    def render(self):
        """
        Draws all game elements onto the screen, creating the visual output of the game.
        """
        self.screen.fill((0, 0, 0))  # Clear the screen with black background
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.draw_score()
        pygame.display.update()
    
    def draw_score(self):
        """
        Displays the current score and high score on the screen.
        """
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        high_score_text = font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 50))
    
    def render_game_over(self):
        """
        Displays the game over message and waits for the player's input to restart or exit.
        """
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.screen_width // 4, self.screen_height // 3))
        
        font = pygame.font.Font(None, 36)
        restart_text = font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))
        self.screen.blit(restart_text, (self.screen_width // 4, self.screen_height // 2))
        
        pygame.display.update()

    def wait_for_restart_or_exit(self):
        """
        Waits for the player to press R to restart or Q to quit the game.
        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.screen_width, self.screen_height, self.grid_size)  # Reset the game
                        waiting = False
                    elif event.key == pygame.K_q:
                        self.game_over = True
                        waiting = False

    def run(self):
        """
        The main game loop that keeps the game running, continuously processing events, updating the game state, and rendering the screen.
        """
        while not self.game_over:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(10 + self.difficulty_level)  # Control the frame rate, increasing with difficulty
            self.check_game_over()
        
        pygame.quit()

if __name__ == "__main__":
    game = AdvancedGame()
    game.run()