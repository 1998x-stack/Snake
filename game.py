import pygame
from snake import Snake
from food import Food
from utils import draw_text, initialize_game
from advanced import Obstacle
from sound import SoundManager  # Import the SoundManager class

class Game:
    def __init__(self, screen_width=600, screen_height=400, grid_size=20):
        """
        Initializes the game by creating the necessary game objects and setting up the environment.
        
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        :param grid_size: Size of the grid units.
        """
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        
        self.screen, self.clock, self.snake, self.food = initialize_game(screen_width, screen_height, grid_size)
        self.obstacles = Obstacle(screen_width, screen_height, grid_size)
        self.score = 0
        self.game_over = False
        
        # Initialize sound manager
        # self.sound_manager = SoundManager()

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
        
        if self.snake.body[0] in self.obstacles.positions:
            print(f"Collision detected with obstacle at {self.snake.body[0]}")
            self.game_over = True
        
        # Check for collisions with walls, self, or obstacles
        if self.snake.check_collision(self.screen.get_width(), self.screen.get_height()) or \
                any(pos == self.snake.body[0] for pos in self.obstacles.positions):
            self.game_over = True
            
        
        # Check if the snake eats the food
        if self.snake.body[0] == self.food.position:
            print("Food eaten!")
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 1
            print(f"Score updated: {self.score}")
    
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
        Displays the current score on the screen.
        """
        draw_text(self.screen, f'Score: {self.score}', (10, 10), 36)

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
                        self.__init__(self.screen.get_width(), self.screen.get_height(), self.snake.grid_size)  # Reset the game
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
            self.clock.tick(10)  # Control the frame rate to 10 FPS
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()