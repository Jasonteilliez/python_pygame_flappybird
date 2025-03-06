import pygame, time, sys
from sprites import BG, Player, Obstacle
from settings import *
from random import randint

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.active = True
        self.last_time = time.time()

        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = HEIGHT / bg_height

        BG(self.visible_sprites, self.scale_factor)
        self.player = Player(self.visible_sprites, self.scale_factor)

        self.obsacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obsacle_timer, 1400)

        self.font = pygame.font.Font(UI_FONT,int(UI_FONT_SIZE*self.scale_factor))
        self.score = 0

        self.menu_surf = pygame.image.load('graphics/ui/menu.png').convert_alpha()
        self.menu_image = pygame.transform.scale(self.menu_surf,pygame.math.Vector2(self.menu_surf.get_size()) * self.scale_factor)
        self.menu_rect = self.menu_image.get_rect(center = (WIDTH/2, HEIGHT/2))

        self.start_offset = 0


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


    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000

        score_surf = self.font.render(str(self.score),True, TEXT_COLOR)
        score_rect = score_surf.get_rect(midtop = (WIDTH/2 ,HEIGHT/30))
        self.display_surface.blit(score_surf, score_rect)


    def collision(self):
        if pygame.sprite.spritecollide(self.player, self.obstacle_sprites, False, pygame.sprite.collide_mask)\
        or self.player.rect.bottom <= 0 or self.player.rect.top >= HEIGHT:
            for sprite in self.obstacle_sprites.sprites():
                sprite.kill()
            self.active = False
            self.player.kill()
        

    def restart(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.active = True
            self.player = Player(self.visible_sprites, self.scale_factor)
            self.start_offset = pygame.time.get_ticks()


    def run(self):
        dt = time.time() - self.last_time
        self.last_time = time.time()
        self.visible_sprites.update(dt)
        self.visible_sprites.draw(self.display_surface)
        self.display_score()

        if self.active :
            self.collision()
        else:
            self.display_surface.blit(self.menu_image, self.menu_rect)
            self.restart()
