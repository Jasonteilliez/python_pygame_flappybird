import pygame, time, sys
from sprites import BG, Player, Obstacle
from settings import *
from random import randint

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.last_time = time.time()

        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = HEIGHT / bg_height

        BG(self.visible_sprites, self.scale_factor)
        self.player = Player(self.visible_sprites, self.scale_factor, self.obstacle_sprites)

        self.obsacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obsacle_timer, 1400)


    def spawn_obstacles(self): 
        gap_size = randint(100,150)
        gap_height = HEIGHT/2 + randint(-100,100)
        offset = WIDTH + randint(40,100)

        Obstacle(
            groups=[self.visible_sprites, self.obstacle_sprites], 
            scale_factor=self.scale_factor, 
            side="bottom", 
            gap_size=gap_size, 
            gap_height=gap_height, 
            offset=offset
        )
        Obstacle(
            groups=[self.visible_sprites, self.obstacle_sprites], 
            scale_factor=self.scale_factor, 
            side="top", 
            gap_size=gap_size, 
            gap_height=gap_height, 
            offset=offset
        )


    def run(self):
        dt = time.time() - self.last_time
        self.last_time = time.time()

        self.visible_sprites.update(dt)
        self.visible_sprites.draw(self.display_surface)