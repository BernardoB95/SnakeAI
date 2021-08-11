import pygame
from IGame import IGame


class Game(IGame):
    """
    This class will use the Game Loop Pattern and implement IGame Abstract Class (Interface)
    """

    def __init__(self):
        super().__init__()

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
        super().run()
