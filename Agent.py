import torch
import random
import numpy as np
from collections import deque
from Model import DeepQNetwork


class Agent:

    def __init__(self):
        self._memory_size = 100000
        self._batch_size = 1000
        self.lr = 0.001
        self.n_games = 0
        self.epsilon = 0  # Randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=self._memory_size)
        self.model = DeepQNetwork(11, self.lr, self.gamma)

    @staticmethod
    def get_state(snake, food, boundaries):
        # Actual state of the snake
        # state -> [danger_straight, danger_right, danger_left,
        #           direction_left, direction_right, direction_up, direction_down,
        #           food_left, food_right, food_up, food_down]

        head = snake.snake_[0]
        above_head = (head[0], head[1] - 10)
        below_head = (head[0], head[1] + 10)
        right_head = (head[0] + 10, head[1])
        left_head = (head[0] - 10, head[1])

        dir_up = snake.direction == "UP"
        dir_down = snake.direction == "DOWN"
        dir_left = snake.direction == "LEFT"
        dir_right = snake.direction == "RIGHT"

        state = [

            # Danger ahead
            (dir_up and snake.isCollision(boundaries, point=above_head) or
             dir_down and snake.isCollision(boundaries, point=below_head) or
             dir_right and snake.isCollision(boundaries, point=right_head) or
             dir_left and snake.isCollision(boundaries, point=left_head)),

            # Danger right
            (dir_up and snake.isCollision(boundaries, point=right_head) or
             dir_down and snake.isCollision(boundaries, point=left_head) or
             dir_right and snake.isCollision(boundaries, point=below_head) or
             dir_left and snake.isCollision(boundaries, point=above_head)),

            # Danger left
            (dir_up and snake.isCollision(boundaries, point=left_head) or
             dir_down and snake.isCollision(boundaries, point=right_head) or
             dir_right and snake.isCollision(boundaries, point=above_head) or
             dir_left and snake.isCollision(boundaries, point=below_head)),

            # Current direction
            dir_left,
            dir_right,
            dir_up,
            dir_down,

            # Food relative location
            food[0] < head[0],
            food[0] > head[0],
            food[1] < head[1],
            food[1] > head[1]
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, future_state, done):
        # Saves crucial information in the memory for training
        self.memory.append((state, action, reward, future_state, done))

    def train_short_memory(self, state, action, reward, future_state, done):
        self.model.DeepQTrainer(state, action, reward, future_state, done)

    def train_replay_memory(self):
        # Act as a long-term memory for the model
        if len(self.memory) > self._batch_size:
            sample = random.sample(self.memory, self._batch_size)

        else:
            sample = self.memory

        states, actions, rewards, future_states, done = zip(*sample)

        self.model.DeepQTrainer(states, actions, rewards, future_states, done)

    def get_action(self, state):
        # Define the Exploration / Exploitation tradeoff
        self.epsilon = 150 - self.n_games
        action = [0, 0, 0]

        if random.randint(0, 100) < self.epsilon:
            random_action = random.randint(0, 2)
            action[random_action] = 1

        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            move = torch.argmax(prediction).item()
            action[move] = 1

        return action

    def train(self):
        pass  # Maybe it doesnt belong here
