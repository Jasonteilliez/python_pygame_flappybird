import pygame, sys, time
from settings import *

from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Flappy Olw')
        self.clock = pygame.time.Clock()

        self.level = Level()


    def run(self):
        while True:

            self.quit_game()
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

    
    def quit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.level.obsacle_timer:
                self.level.spawn_obstacles()


if __name__ == "__main__":
    game = Game()
    game.run()