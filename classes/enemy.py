#enemy classes

import pygame

MAX_LEVEL = 100

def lerp(a, b, weight) -> float:
    return a + (b - a) * weight

#enemy parent class
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, start_pos: tuple, rect : pygame.rect.Rect, max_health : int, move_speed: float, current_level : int = 1):
        super().__init__()
        self.hp = max_health
        self.lv = current_level
        self.stopped = False
        self.rect = rect
        self.rect.topleft = start_pos

        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.speed_mult = move_speed

    def update(self, player_position: tuple):
        if not self.stopped:
            player_position

    def hit(self, damage):
        self.hp -= damage * resistance:


#child classes

DOG_SPEED = 10
AIR_SPEED = 5
BIG_SPEED = 1

DOG_HP = 1000
AIR_HP = 750
BIG_HP = 500000

class Hound(Enemy):
    def __init__(self, starting_pos, level = 1):
        self.image = pygame.image.load("dog.png")
        super().__init__(starting_pos, self.image.get_rect(), DOG_HP, DOG_SPEED, level)
        

class AirTurret(Enemy):
    def __init__(self, starting_pos, level = 20):
        self.image = pygame.image.load("turret.png")
        super().__init__(starting_pos, self.image.get_rect(), AIR_HP, AIR_SPEED, level)

#will have far more animations than the basic enemies
class DeathBot(Enemy):
    def __init__(self, starting_pos, level = 50):
        self.image = pygame.image.load("boss.png")
        super().__init__(starting_pos, self.image.get_rect(), BIG_HP, BIG_SPEED, level)
        