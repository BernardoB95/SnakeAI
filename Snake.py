import pygame


class Snake:
    def __init__(self):
        self.dimension = 10
        self.snake_ = [[320, 240], [310, 240], [300, 240]]
        self._direction = "RIGHT"

    # region Getters & Setters

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, pivot):
        self._direction = pivot

    # endregion

    def pivotBehaviourY(self, value, pivot):
        reverse = (self.direction == "UP" and pivot == "DOWN") or (self.direction == "DOWN" and pivot == "UP")
        if not reverse:
            self.moveBody()
            self.snake_[0] = [self.snake_[0][0], self.snake_[0][1] + value]
            self.direction = pivot

    def pivotBehaviourX(self, value, pivot):
        reverse = (self.direction == "LEFT" and pivot == "RIGHT") or (self.direction == "RIGHT" and pivot == "LEFT")
        if not reverse:
            self.moveBody()
            self.snake_[0] = [self.snake_[0][0] + value, self.snake_[0][1]]
            self.direction = pivot

    def applyMovementInertia(self):
        self.moveBody()
        if self.direction == "UP":
            self.snake_[0] = [self.snake_[0][0], self.snake_[0][1] - 10]
        if self.direction == "RIGHT":
            self.snake_[0] = [self.snake_[0][0] + 10, self.snake_[0][1]]
        if self.direction == "DOWN":
            self.snake_[0] = [self.snake_[0][0], self.snake_[0][1] + 10]
        if self.direction == "LEFT":
            self.snake_[0] = [self.snake_[0][0] - 10, self.snake_[0][1]]

    def foodWasEaten(self, food):
        # food_x_range = food[0] + 10
        # food_y_range = food[1] + 10
        # if food[0] < self.snake_[0][0] < food_x_range and food[1] < self.snake_[0][1] < food_y_range:
        #     print('passou pela comida')
        return self.snake_[0] == list(food)

    def grow(self):
        self.snake_.append([0, 0])

    def display_long_snake(self, surface, color):
        for pixel in self.snake_:
            _X = pixel[0]
            _Y = pixel[1]

            pygame.draw.rect(surface, color, (_X, _Y, self.dimension, self.dimension))

    def moveBody(self):
        for i in range(len(self.snake_) - 1, 0, -1):
            self.snake_[i] = [self.snake_[i - 1][0], self.snake_[i - 1][1]]

    def outOfBoundaries(self, boundaries):

        outOfXL = self.snake_[0][0] - 10 < boundaries[2]
        outOfXR = self.snake_[0][0] + 15 > boundaries[3]
        outOfYU = self.snake_[0][1] - 5 < boundaries[0]
        outOfYD = self.snake_[0][1] + 15 > boundaries[1]

        return outOfXL or outOfXR or outOfYU or outOfYD

    def isCollision(self, boundaries, point=None):
        if point is None:
            point = self.snake_[0]

        if self.outOfBoundaries(boundaries):
            return True

        if point in self.snake_[1:]:
            return True

        return False
