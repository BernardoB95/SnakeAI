import pygame
from IGame import IGame
from Agent import Agent


class Environment(IGame):
    def __init__(self):
        super().__init__()
        self.agent = Agent()

    def processInput(self):
        # Process input will be the model prediction
        state = self.agent.get_state(self.snake, self.food_position, self.boundaries)
        action = self.agent.get_action(state)
        # Transform action into direction
        clockwise_pivot = ["RIGHT", "DOWN", "LEFT", "UP"]
        index = clockwise_pivot.index(self.snake.direction)
        direction = None

        # If right turn
        if action == [0, 0, 1]:
            direction = clockwise_pivot[(index + 5) % 4]

        # If left turn
        elif action == [1, 0, 0]:
            direction = clockwise_pivot[(index + 3) % 4]

        if direction is not None:
            if direction == "UP":
                self.snake.pivotBehaviourY(-10, direction)
            elif direction == "DOWN":
                self.snake.pivotBehaviourY(10, direction)
            elif direction == "LEFT":
                self.snake.pivotBehaviourX(-10, direction)
            elif direction == "RIGHT":
                self.snake.pivotBehaviourX(10, direction)

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
