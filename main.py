import os
import pygame
from Game import Game


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    game = Game()
    game.run()
    pygame.quit()
