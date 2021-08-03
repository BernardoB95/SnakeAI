import pygame
from random import  randint


class Food:

    def __init__(self):
        self._X = 600
        self._Y = 400
        self.food = None
        self.dimension = 10

    # region Getters & Setters

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, coordinate):
        self._X = coordinate

    @property
    def Y(self):
        return self._Y

    @Y.setter
    def Y(self, coordinate):
        self._Y = coordinate

    # endregion

    def display(self, surface, color):
        self.food = pygame.draw.rect(surface, color, (self.X, self.Y, self.dimension, self.dimension))

    def align_on_grid(self):
        self.X = self.X // 10 * 10
        self.Y = self.Y // 10 * 10

    def generate_food(self, boundaries):
        top_boundary = boundaries[0] + 10
        bottom_boundary = boundaries[1] - 10
        left_boundary = boundaries[2] + 10
        right_boundary = boundaries[3] - 10

        self.X = randint(left_boundary, right_boundary)
        self.Y = randint(top_boundary, bottom_boundary)

        self.align_on_grid()

        return self.X, self.Y
