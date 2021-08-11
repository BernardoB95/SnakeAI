import os
import pygame
from Environment import Environment


if __name__ == '__main__':

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    game = Environment()
    game.run()
    pygame.quit()