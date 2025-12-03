import pygame
from classes.animation import Animation
from classes.bullet import Bullet

VELOCITY_THRESHOLD = 0.01
DEFAULT_FRICTION = 0.2

WALK_FRAMES = 4
IDLE_FRAMES = 8
DEATH_FRAMES = 4

MAX_STAMINA = 100

WALK_MILLISECONDS = 200
IDLE_MILLISECONDS = 400
DEATH_MILLISECONDS = 600

BULLET_SPEED = 5
FIRE_RATE = 200

LEFT: bool = 0
RIGHT: bool = 1

load = pygame.image.load
vec2 = pygame.math.Vector2

def clamp(val, min_value, max_value):
    return max(min(val, max_value), min_value)

def lerp(stat_min, stat_max, level_fraction: float) -> float: #will be used to calculate enemy stats depending on current level
    return stat_min + (stat_max - stat_min) * level_fraction
                                                           
class Player(pygame.sprite.Sprite):
    def __init__(self, starting_pos : tuple, FPS: int, speed_multiplier : float = 0.3, starting_items: list = [], starting_health: int = 3, starting_level: int = 1):
        super().__init__()

        #load sprites
        walk_frames = [load(f"assets/PLAYER/player_run-{i}.png").convert() for i in range(WALK_FRAMES)]
        idle_frames = [load(f"assets/PLAYER/player_idle-{i}.png").convert() for i in range(IDLE_FRAMES)]
        death_frames = [load(f"assets/PLAYER/player_death-{i}.png").convert() for i in range(DEATH_FRAMES)]

        #create animation objects
        self.walk = [Animation, Animation]
        self.walk[RIGHT] = Animation(walk_frames, WALK_MILLISECONDS).set_colorkey_all("#FFFFFF")
        self.walk[LEFT] = self.walk[RIGHT].flip_frames(True)

        self.idle = [Animation, Animation]
        self.idle[RIGHT] = Animation(idle_frames, IDLE_MILLISECONDS).set_colorkey_all("#000000")
        self.idle[LEFT] = self.idle[RIGHT].flip_frames(True)

        self.death = [Animation, Animation]
        self.death[RIGHT] = Animation(death_frames, DEATH_MILLISECONDS).set_colorkey_all("#FFFFFF")
        self.death[LEFT] = self.death[RIGHT].flip_frames(True)
        
        self.image: pygame.Surface = self.idle[RIGHT].update()

        self.stopwatch = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = starting_pos

        self.turn = True #1 for left, 0 for right
        self.FPS = FPS
        self.ticks = pygame.time.get_ticks()
        self.dead = False

        self.bullet_group = pygame.sprite.Group()
        #movement
        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)
        self.invincibility = 0
        self.stamina = MAX_STAMINA

        #stats
        self.speed_mult = speed_multiplier
        self.MAXHP = 3
        self.hp = starting_health
        self.items = starting_items
        self.level = starting_level
        self.xp = 0
        self.damage = 1.0
        self.rof = FIRE_RATE

    def update(self, screen_rect: pygame.rect.Rect, surface_friction: float = DEFAULT_FRICTION, acceleration: float = 0.2):
        """
        updates all variables depending on game state
        """

        self.stamina = clamp(self.stamina, 0, MAX_STAMINA)
        self.rect.x = clamp(self.rect.x, 0, screen_rect.w - self.rect.width)
        self.rect.y = clamp(self.rect.y, 0, screen_rect.h - self.rect.height)

        self.level = int(lerp(1, 100, self.xp/10000))
        self.damage = int(lerp(1, 400, self.level/100))
        self.rof = lerp(FIRE_RATE, 1, self.level/100)
        self.MAXHP = lerp(3, 10, self.level/100)
        self.regen = True
        if self.xp > 4000 and self.regen:
            self.hp = int(self.MAXHP)
            self.regen = False

        #reset acceleration vector
        self.acceleration = vec2(0, 0)

        if self.invincibility > 0:
            self.invincibility -= 1

        #check for player movement
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acceleration.x = -acceleration
            self.turn = LEFT
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acceleration.x = acceleration
            self.turn = RIGHT
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.acceleration.y = -acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.acceleration.y = acceleration

        #sprinting
        speed = self.speed_mult
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if (self.stamina > 10):
                speed = self.speed_mult * 1.5
            self.stamina -= 1
        else:
            self.stamina += 1

        #shooting
        if (keys[pygame.K_SPACE]) or (mouse_buttons[0]):
            self.shoot(pygame.mouse.get_pos())

        #normalize acceleration vector and update player image
        if self.acceleration.magnitude() > 0: #player is moving
            self.acceleration = self.acceleration.normalize() * speed
            self.image = self.walk[self.turn].update()
        
        #check if player is moving and play idle animation
        elif (self.velocity.magnitude() < VELOCITY_THRESHOLD): #player is not moving
            self.velocity = vec2(0, 0)
            self.image = self.idle[self.turn].update()

        #final movement calculations
        self.acceleration -= self.velocity * surface_friction
        self.velocity += self.acceleration
        self.rect.center += self.velocity + (0.5 * self.acceleration)

    def shoot(self, target):
        """
        creates a bullet object with a movement vector that\n
        points towards the given target.
        """
        now = pygame.time.get_ticks()
        if now - self.ticks > self.rof:
            self.ticks = now
            self.bullet_group.add(Bullet(BULLET_SPEED, 200, self.rect.center, target, True))

    def hit(self):
        """
        reduces player health by 1 and calls die() if hp reaches 0
        """
        if self.invincibility == 0:
            self.hp -=1
            self.invincibility = 100
        if self.hp < 1:
            self.die()
    
    def die(self):
        """
        plays a death animation and calls pygame.sprite.kill()\n
        once it's done
        """
        self.dead = True
        self.speed_mult = 0
        self.image = self.death[self.turn].update()
        if not self.death[self.turn].get_current_index():
            self.kill()