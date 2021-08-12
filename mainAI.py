import os
import pygame
from Environment import Environment
from Agent import Agent


if __name__ == '__main__':

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    agent = Agent()
    game = Environment(agent)
    game.run()
    pygame.quit()
