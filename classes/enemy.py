#enemy parent class
import pygame

class Enemy(pygame.sprite.Sprite): #enemy parent class
    def __init__(self, max_health : int, current_level : int = 1):
        super().__init__()
        self.hp = max_health
        self.lv = current_level
    
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

class Hound(Enemy):
    def __init__(self, level):
        super().__init__(1000, level)

class AirTurret(Enemy):
    def __init__(self, level):
        super().__init__(500, level)

class DeathBot(Enemy):
    def __init__(self, level):
        super().__init__(500, 100)
        