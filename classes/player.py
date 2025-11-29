import pygame
from classes.animation import Animation
from classes.bullet import Bullet

VELOCITY_THRESHOLD = 0.01
DEFAULT_FRICTION = 0.2

WALK_FRAMES = 4
IDLE_FRAMES = 8
DEATH_FRAMES = 8

WALK_MILLISECONDS = 200
IDLE_MILLISECONDS = 400
DEATH_MILLISECONDS = 600

BULLET_SPEED = 5

LEFT: bool = 0
RIGHT: bool = 1

load = pygame.image.load
vec2 = pygame.math.Vector2

def intlerp(a, b, weight) :
    return int(a + (a - b) * weight)
                                                           
class Player(pygame.sprite.Sprite):
    def __init__(self, starting_pos : tuple, FPS: int, speed_multiplier : float = 0.3, starting_items: list = [], starting_health: int = 3, starting_level: int = 1):
        super().__init__()

        #sprite management
        walk_frames = [load(f"assets/PLAYER/player_run-{i}.png").convert() for i in range(WALK_FRAMES)]
        idle_frames = [load(f"assets/PLAYER/player_idle-{i}.png").convert() for i in range(IDLE_FRAMES)]
        #death_frames = [load(f"assets/PLAYER/player_death-{i}.png").convert() for i in range(DEATH_FRAMES)]

        self.walk = [Animation, Animation]
        self.walk[RIGHT] = Animation(walk_frames, WALK_MILLISECONDS).set_colorkey_all("#FFFFFF")
        self.walk[LEFT] = self.walk[RIGHT].flip_frames(True)

        self.idle = [Animation, Animation]
        self.idle[RIGHT] = Animation(idle_frames, IDLE_MILLISECONDS).set_colorkey_all("#000000")
        self.idle[LEFT] = self.idle[RIGHT].flip_frames(True)

        #self.death = [Animation, Animation]
        #self.death[RIGHT] = Animation(death_frames, DEATH_MILLISECONDS).set_colorkey_all("#FFFFFF")
        #self.death[LEFT] = self.death[RIGHT].flip_frames(True)
        
        self.image: pygame.Surface = self.idle[RIGHT].update()

        self.stopwatch = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = starting_pos

        self.turn = True #1 for left, 0 for right
        self.FPS = FPS

        #movement
        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)
        self.bullet_group = pygame.sprite.Group()
        self.invincibility = 0

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

        #check for player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -acceleration
            self.turn = LEFT
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = acceleration
            self.turn = RIGHT
        if keys[pygame.K_UP]:
            self.acceleration.y = -acceleration
        if keys[pygame.K_DOWN]:
            self.acceleration.y = acceleration
        if (keys[pygame.K_SPACE]) or keys[pygame.MOUSEBUTTONDOWN]:
            self.shoot()


        if self.acceleration.magnitude() > 0: #player is moving
            self.acceleration = self.acceleration.normalize() * self.speed_mult
            self.image = self.walk[self.turn].update()
        
        elif self.velocity.magnitude() < VELOCITY_THRESHOLD: #player is not moving
            self.velocity = vec2(0, 0)
            self.image = self.idle[self.turn].update()

        

        self.acceleration -= self.velocity * surface_friction
        self.velocity += self.acceleration
        self.rect.center += self.velocity + (0.5 * self.acceleration)

    def shoot(self):
        self.bullet_group.add(Bullet(BULLET_SPEED, self.rect.center, pygame.mouse.get_pos(), True))

    def hit(self):
        if self.invincibility > 0:
            self.hp -=1
        if self.hp < 1:
            return True
        return False



    
    
