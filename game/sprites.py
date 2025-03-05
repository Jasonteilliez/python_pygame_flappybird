import pygame, sys
from settings import *
from random import randint

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('graphics/environment/background.png').convert()

        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() *scale_factor
        full_sized_image = pygame.transform.scale(bg_image,(full_width, full_height))
        # full_sized_image = pygame.transform.scale(bg_image,pygame.math.Vector2(bg_image.get_size()) * scale_factor)

        self.image = pygame.Surface((full_width*2, full_height))
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 200 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
        

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor, obstacle_sprites):
        super().__init__(groups)
        self.import_frames(scale_factor)
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midleft = (WIDTH/20, HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.animation_speed = 5

        self.gravity = 500
        self.direction = 0

        self.obstacle_sprites = obstacle_sprites

        self.mask = pygame.mask.from_surface(self.image)


    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(4):
            surf = pygame.image.load(f'graphics/player/owl{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)


    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
        self.collision()


    def collision(self):
        if pygame.sprite.spritecollide(self, self.obstacle_sprites, False, pygame.sprite.collide_mask)\
        or self.rect.bottom <= 0 or self.rect.top >= HEIGHT:
            pygame.quit()
            sys.exit()


    def jump(self):
        self.direction = -300


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()


    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.input()
        self.apply_gravity(dt)
        self.animate(dt)

    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor, side, gap_size, gap_height, offset):
        super().__init__(groups)

        surf = pygame.image.load('graphics/obstacles/colonne.png').convert_alpha()
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)

        if side == "bottom" :
            y = int(gap_height + gap_size/2)
            self.rect = self.image.get_rect(midtop = (offset, y))
            
        if side == "top" :
            self.image = pygame.transform.flip(self.image,False,True)
            y = int(gap_height - gap_size/2)
            self.rect = self.image.get_rect(midbottom = (offset , y))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 400*dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
