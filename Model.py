import torch
import torch.nn as nn
import torch.optim as optim
import os


class DeepQNetwork(nn.Module):
    def __init__(self, inputs, lr, gamma):
        super().__init__()
        self.fcn = nn.Sequential(nn.Linear(inputs, 256),
                                 nn.ReLU(),
                                 nn.Linear(256, 120),
                                 nn.Dropout(p=0.1),
                                 nn.ReLU(),
                                 nn.Linear(120, 3),
                                 nn.Dropout(p=0.15))

        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(self.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def forward(self, x):
        return self.fcn(x)

    def save(self, file_name='model.pth'):
        directory = './model'
        if not os.path.exists(directory):
            os.mkdir(directory)

        full_path = os.path.join(directory, file_name)
        torch.save(self.state_dict(), full_path)

    def DeepQTrainer(self, state, action, reward, future_state, done):
        # Self is the model
        """
        This function will be responsible for the short term and long term training of the model.
        :param state: Its the current state of the agent -> contains an array of eleven indicators
        :type state: list / list(list)
        :param action: Its the action taken given the state -> contains an array of 3 indicators
        :type action: list / list(list)
        :param reward: Its the reward given to the agent based on the action it took
        :type reward: int / list(int)
        :param future_state: Its the prediction of the model based on the other parameters -> array of eleven indicators
        :type future_state: list / list(list)
        :param done:
        :type done:
        :return:
        :rtype:
        """

        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        future_state = torch.tensor(future_state, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, dim=0)
            action = torch.unsqueeze(action, dim=0)
            reward = torch.unsqueeze(reward, dim=0)
            future_state = torch.unsqueeze(future_state, dim=0)
            done = (done, )

        # Implementation of Bellman's Equation
        #  1 - Predicted Q values with the current state
        pred = self(state)

        # 2 - Reward + (gamma * max(future predicted Q values)) -> if not done (for short memory)
        target = pred.clone()

        for i, item in enumerate(done):
            # This reward is the one used when the agent looses
            future_Q = reward[i]

            if not done[i]:
                future_Q = reward[i] + (self.gamma * torch.max(self(future_state[i])))

            target[i][torch.argmax(action).item()] = future_Q


        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
