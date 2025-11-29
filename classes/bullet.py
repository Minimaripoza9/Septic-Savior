import pygame
from classes.animation import Animation

load = pygame.image.load
vec2 = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed: float, starting_pos: tuple, target: tuple, is_friendly: bool):
        super().__init__()
        self.image = load(f"assets/bullet{int(is_friendly)}.png").convert()
        self.rect = self.image.get_rect()
        self.velocity = vec2(target[0]-starting_pos[0],target[1]-starting_pos[1]).normalize_ip() * speed
        


class Missile(pygame.sprite.Sprite):
    def __init__(self, starting_pos: tuple, target: tuple, is_friendly: bool):
        super().__init__()
        self.target = target
        self.image = load(f"assets/bullet{int(is_friendly)}.png").convert()
        self.velocity = vec2(target[0]-starting_pos[0],target[1]-starting_pos[1]).normalize_ip()

    def update(self):
        self.rec