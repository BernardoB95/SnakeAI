import pygame
from Snake import Snake
from Food import Food
from abc import ABC, abstractmethod


class IGame(ABC):
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

    @abstractmethod
    def processInput(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def run(self):

        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(30)
