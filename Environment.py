import pygame
from IGame import IGame
from Snake import Snake
from Food import Food


class Environment(IGame):
    def __init__(self, agent):
        super().__init__()
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 20)
        self.agent = agent
        self.reward = 0
        self.score = 0
        self.record = 0
        self.frame_iteration = 0
        self.state = []
        self.action = []

    def processInput(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

        # frame_iteration will work as an stop condition
        self.frame_iteration += 1

        # Process input will be the model prediction
        self.state = self.agent.get_state(self.snake, self.food_position, self.boundaries)
        self.action = self.agent.get_action(self.state)
        # Transform action into direction
        clockwise_pivot = ["RIGHT", "DOWN", "LEFT", "UP"]
        index = clockwise_pivot.index(self.snake.direction)
        direction = None

        # If right turn
        if self.action == [0, 0, 1]:
            direction = clockwise_pivot[(index + 5) % 4]

        # If left turn
        elif self.action == [1, 0, 0]:
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
        self.reward = 0
        self.snake.applyMovementInertia()

        if self.snake.foodWasEaten(self.food_position):
            self.food_position = self.food.generate_food(self.boundaries)
            self.snake.grow()
            self.score += 1
            self.reward = 10

        if self.snake.isCollision(self.boundaries) or self.frame_iteration > 150 * len(self.snake.snake_):
            self.running = False
            self.reward = -10

        # Train short memory after each iteration
        new_state = self.agent.get_state(self.snake, self.food_position, self.boundaries)
        done = not self.running

        self.agent.train_short_memory(self.state, self.action, self.reward, new_state, done)
        self.agent.remember(self.state, self.action, self.reward, new_state, done)

    def render(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, self.PURPLE, (5, 5, 630, 5))
        pygame.draw.rect(self.window, self.PURPLE, (5, 5, 5, 470))
        pygame.draw.rect(self.window, self.PURPLE, (5, 470, 630, 5))
        pygame.draw.rect(self.window, self.PURPLE, (630, 5, 5, 470))

        self.snake.display_long_snake(self.window, self.PURPLE)
        self.food.display(self.window, self.LIGHT_ORANGE)
        score = self.font.render(f"Score: {self.score}", False, self.PURPLE)
        score_surface = score.get_rect(topleft=(15, 10))
        self.window.blit(score, score_surface)
        pygame.display.update()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.food_position = self.food.generate_food(self.boundaries)
        self.score = 0
        self.frame_iteration = 0

    def run(self):

        while True:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(30)

            # TODO: Fix this loop
            if not self.running:

                # Train long memory
                self.agent.train_replay_memory()
                self.agent.n_games += 1

                if self.score > self.record:
                    self.record = self.score
                    self.agent.model.save()

                print(f"Game #{self.agent.n_games} | Score: {self.score} | Record: {self.record}")
                self.reset()

                self.running = True
