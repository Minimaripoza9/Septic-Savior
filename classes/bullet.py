import pygame
from classes.animation import Animation

load = pygame.image.load
vec2 = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed: float, fire_rate: int, starting_pos: tuple, target: tuple, is_friendly: bool):
        super().__init__()
        self.image = load(f"assets/bullets/bullet-{int(is_friendly)}.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = starting_pos
        self.rof = fire_rate
        self.ticks = pygame.time.get_ticks()
        try:
            self.velocity = vec2(target[0]-starting_pos[0],target[1]-starting_pos[1]).normalize() * speed
        except:
            self.velocity = vec2(1, 1)

    def update(self):
        self.rect.center += self.velocity

class Missile(pygame.sprite.Sprite):
    def __init__(self, starting_pos: tuple, target: tuple):
        super().__init__()
        self.target = target
        sprites = [load(f"assets/MISSILE/missile-{i}.png").convert() for i in range(4)]
        self.anim = Animation(sprites)
        self.anim.set_colorkey_all("#000000")
        self.image: pygame.surface.Surface = self.anim.update()
        self.rect = self.image.get_rect()
        self.rect.center = starting_pos
        self.velocity :vec2= vec2(target[0]-starting_pos[0],target[1]-starting_pos[1]).normalize() * 5

    def update(self):
        self.rect.center += self.velocity
        _, angle = self.velocity.as_polar()
        self.image = pygame.transform.rotate(self.anim.update(), -angle+45)
