import pygame
from classes.animation import Animation

VELOCITY_THRESHOLD = 0.001
DEFAULT_FRICTION = 0.2
WALK_FRAMES = 4
IDLE_FRAMES = 8

load = pygame.image.load
vec2 = pygame.math.Vector2

def frame_index(metronome, total_fps,  desired_FPS, Frame_total, turn: bool) -> int:
    return int(metronome * total_fps/desired_FPS) % Frame_total + (Frame_total * turn)

def intlerp(a, b, weight) :
    return int(a + (a - b) * weight)
                                                           
class Player(pygame.sprite.Sprite):
    def __init__(self, starting_pos : tuple, FPS: int, speed_multiplier : float = 0.2, starting_items: list = [], starting_health: int = 3, starting_level: int = 1):
        super().__init__()

        #sprite management
        walk_right = [load(f"assets/player_run/pixil-frame-{i}.png").convert() for i in range(4)]
        walk_left = []

        self.walk_right = Animation("assets/player_run/pixil-frame-", "png", 8, 200)
        
        for frame in walk_right:
            frame.set_colorkey("#FFFFFF")
            walk_left.append(pygame.transform.flip(frame, True, False))

        idle_right = [load(f"assets/player_idle/pixil-frame-{i}.png").convert() for i in range(8)]
        idle_left = []

        for frame in idle_right:
            frame.set_colorkey("#FFFFFF") 
            idle_left.append(pygame.transform.flip(frame, True, False))
        
        self.image = self.idle_right[0]

        self.stopwatch = pygame.time.get_ticks()
        self.rect = self.walk_right[0].get_rect()
        self.rect.center = starting_pos

        self.turn = True #1 for left, 0 for right
        self.FPS = FPS

        #movement
        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)

        #stats
        self.speed_mult = speed_multiplier
        self.MAXHP = 3
        self.hp = starting_health
        self.items = starting_items
        self.level = starting_level
        self.damage_mult = 1.0

    def update(self, acceleration: float = 0.2, surface_friction: float = DEFAULT_FRICTION):

        #reset acceleration vector
        self.acceleration = vec2(0, 0)

        self.metronome %= self.FPS

        #check for player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -acceleration
            self.turn = True
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = acceleration
            self.turn = False
        if keys[pygame.K_UP]:
            self.acceleration.y = -acceleration
        if keys[pygame.K_DOWN]:
            self.acceleration.y = acceleration

        if self.acceleration.magnitude() > 0: #player is moving
            self.acceleration = self.acceleration.normalize() * self.speed_mult
            self.image = self.walk_right[intlerp(0, 8, self.metronome/self.FPS)]
        
        elif self.velocity.magnitude() < VELOCITY_THRESHOLD: #player is not moving
            self.velocity = vec2(0, 0)
            self.image = self.idle_right[intlerp(0, 4, self.metronome/self.FPS)]

        self.acceleration -= self.velocity * surface_friction
        self.velocity += self.acceleration
        self.rect.center += self.velocity + (0.5 * self.acceleration)
    
