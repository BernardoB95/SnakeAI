import pygame
from Snake import Snake
from Food import Food


class Game:
    """
    This class will use the Game Loop Pattern
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.PURPLE = (255, 0, 255)
        self.LIGHT_ORANGE = (255, 226, 149)
        self.boundaries = (10, 470, 10, 630)
        self.snake = Snake()
        self.food = Food()
        self.food_position = self.food.generate_food(self.boundaries)
        self.running = True

    def processInput(self):

        self.snake.moveCommandX = 0
        self.snake.moveCommandY = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            # TODO REFACTOR THIS CODE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break

                elif event.key == pygame.K_UP:
                    self.snake.pivotBehaviourY(-10, "UP")

                elif event.key == pygame.K_DOWN:
                    self.snake.pivotBehaviourY(10, "DOWN")

                elif event.key == pygame.K_LEFT:
                    self.snake.pivotBehaviourX(-10, "LEFT")

                elif event.key == pygame.K_RIGHT:
                    self.snake.pivotBehaviourX(10, "RIGHT")

    def update(self):
        self.snake.applyMovementInertia()

        if self.snake.foodWasEaten(self.food_position):
            self.food_position = self.food.generate_food(self.boundaries)
            self.snake.grow()

        if self.snake.isCollision(self.boundaries):
            self.running = False

    def render(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, self.PURPLE, (5, 5, 630, 5))
        pygame.draw.rect(self.window, self.PURPLE, (5, 5, 5, 470))
        pygame.draw.rect(self.window, self.PURPLE, (5, 470, 630, 5))
        pygame.draw.rect(self.window, self.PURPLE, (630, 5, 5, 470))

        self.snake.display_long_snake(self.window, self.PURPLE)
        self.food.display(self.window, self.LIGHT_ORANGE)
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(30)
