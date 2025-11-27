#TODO: add animations

#enemy classes

import pygame

MAX_LEVEL = 50 #not actually a hard level cap, just a point of reference
VELOCITY_THRESHOLD = 0.1
DEFAULT_FRICTION = 0.2

load = pygame.image.load
vec2 = pygame.math.Vector2

#custom lerp function that can return numbers outside the [0, 1] range
def lerp(stat_min, stat_max, level_fraction: float) -> float: #will be used to calculate enemy stats depending on current level
    return stat_min + (stat_max - stat_min) * level_fraction

#enemy parent class
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, start_pos: tuple, rect : pygame.rect.Rect, max_health : int, move_speed: float, current_level : int = 1):
        super().__init__()
        self.MAX_HP = max_health
        self.lv = current_level
        self.hp = int(lerp(1, self.MAX_HP, self.lv/MAX_LEVEL))
        self.stopped = False #will be used to make boss stop during attacks and also freeze enemies
        self.rect = rect
        self.rect.center = start_pos

        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)
        self.speed_mult = move_speed

    def update(self, player_position: tuple, surface_friction : float = DEFAULT_FRICTION):
        self.acceleration = vec2(player_position[0]-self.rect.center[0],player_position[1]-self.rect.center[1]) * (not self.stopped)
        
        if self.acceleration.magnitude() > 0:
            self.acceleration = self.acceleration.normalize() * self.speed_mult

        elif self.velocity.magnitude() < VELOCITY_THRESHOLD:
            self.velocity = vec2(0, 0)

        self.acceleration -= self.velocity * surface_friction
        self.velocity += self.acceleration
        self.rect.topleft += self.velocity + (0.5 * self.acceleration)

    def level_up(self, level_modifier : int = 1):
        self.lv += level_modifier
        self.hp = int(lerp(1, self.MAX_HP, self.lv/MAX_LEVEL))


    def hit(self, damage):
        self.hp -= damage * self.armor_percent

#child classes

DOG_SPEED = 10
AIR_SPEED = 5
BIG_SPEED = 1

DOG_HP = 1000
AIR_HP = 750
BIG_HP = 500000

class Hound(Enemy):
    def __init__(self, starting_pos, level = 1):
        self.walk_anim = [load("dog.png")]
        super().__init__(starting_pos, self.walk_anim[0].get_rect(), DOG_HP, DOG_SPEED, level)
        

class AirTurret(Enemy):
    def __init__(self, starting_pos, level = 20):
        self.walk_anim = [load("turret.png")]
        super().__init__(starting_pos, self.walk_anim[0].get_rect(), AIR_HP, AIR_SPEED, level)

#will have far more animations than the basic enemies
class DeathBot(Enemy):
    def __init__(self, starting_pos, level = 50):
        self.walk_anim = [load("boss.png")]
        super().__init__(starting_pos, self.walk_anim[0].get_rect(), BIG_HP, BIG_SPEED, level)
        