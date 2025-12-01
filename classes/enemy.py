#TODO: add animations

#enemy classes

import pygame, random, math
from classes.animation import Animation
from classes.bullet import Bullet, Missile

MAX_LEVEL = 200 #not actually a hard level cap, just a point of reference
VELOCITY_THRESHOLD = 0.0001
DEFAULT_FRICTION = 0.7
DEFAULT_SF = 100

LEFT: bool = 0
RIGHT: bool = 1

load = pygame.image.load
vec2 = pygame.math.Vector2
get_ticks = pygame.time.get_ticks
lerp = pygame.math.lerp

#enemy parent class
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, start_pos: tuple, walk_animation : list, walk_milliseconds: int, max_health : int, move_speed: float, current_level : int = 1):
        super().__init__() 
        self.MAX_HP = max_health
        self.lv = current_level
        self.hp = int(lerp(1, self.MAX_HP, self.lv/MAX_LEVEL))

        self.walk = [Animation, Animation]
        self.walk[RIGHT] = Animation(walk_animation, walk_milliseconds).set_colorkey_all("#ffffff")
        self.walk[LEFT] = self.walk[RIGHT].flip_frames(True)

        self.image: pygame.surface.Surface = self.walk[RIGHT].update()
        self.turn = RIGHT

        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        self.bullet_group = pygame.sprite.Group()

        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)
        self.speed_mult = move_speed
        self.ticks = pygame.time.get_ticks()
        self.step_frequency = DEFAULT_SF
        self.stopped = False #will be used to make boss stop during attacks and also freeze enemies

    def update(self, player_position: tuple, surface_friction : float = DEFAULT_FRICTION):
        self.velocity = vec2(player_position[0]-self.rect.center[0], player_position[1]-self.rect.center[1]) * (not self.stopped)
        self.turn = bool(self.rect.centerx - player_position[0] > 0)

        if not self.stopped and self.velocity.magnitude() > 0:
            self.velocity = self.velocity.normalize() * self.speed_mult
            self.image = self.walk[self.turn].update()

        #if self.velocity.magnitude() < VELOCITY_THRESHOLD:
        #    self.velocity = vec2(0, 0)

        #self.acceleration -= self.velocity * surface_friction
        #self.velocity = self.acceleration
        now = get_ticks()
        if now - self.ticks > self.walk[RIGHT].get_frame_speed():
            self.ticks = now
            self.rect.topleft += self.velocity #+ (0.5 * self.acceleration)


    def level_up(self, level_modifier : int = 1):
        self.lv += level_modifier
        self.hp = int(lerp(1, self.MAX_HP, self.lv/MAX_LEVEL))

    def is_killing_blow(self, damage):
        self.hp -= damage
        if self.hp < 1:
            self.kill()
            return True
        return False

#child classes

DOG_HP = 250
DOG_SPEED = 5
DOG_WALK_FRAMES = 4
DOG_ANIM_MILLISECONDS = 100

AIR_HP = 200
AIR_SPEED = 5
AIR_BULLET_SPEED = 3
AIR_WALK_FRAMES = 4
AIR_ANIM_MILLISECONDS = 300
AIR_FIRE_RATE = 5000

BIG_HP = 500000
BIG_SPEED = 5

BIG_WALK_FRAMES = 8
BIG_PUNCH_FRAMES = 8
BIG_BARRAGE_FRAMES = 8
BIG_WALK_MILLISECONDS = 200
BIG_PUNCH_MILLISECONDS = 200
BIG_BARRAGE_MILLISECONDS = 5000
BIG_MISSILE_DELAY = 500
BIG_MISSILE_COUNT = 10


class Hound(Enemy):
    def __init__(self, starting_pos, level = 1):
        walk_anim = [load(f"assets/HOUND/hound-run-frame-{i}.png").convert() for i in range(DOG_WALK_FRAMES)]
        super().__init__(starting_pos, walk_anim, DOG_ANIM_MILLISECONDS, DOG_HP, DOG_SPEED, level)
        
class Drone(Enemy):
    def __init__(self, starting_pos, level = 20):
        walk_anim = [load(f"assets/DRONE/drone_run_{i}.png").convert() for i in range(AIR_WALK_FRAMES)]
        self.fire_rate = AIR_FIRE_RATE
        self.shot_ticks = pygame.time.get_ticks()
        super().__init__(starting_pos, walk_anim, AIR_ANIM_MILLISECONDS, AIR_HP, AIR_SPEED, level)

    def update(self, player_position, surface_friction = DEFAULT_FRICTION):
        super().update(player_position, surface_friction)
        self.shoot(player_position)
        
    def shoot(self, target):
        now = pygame.time.get_ticks()
        if now - self.shot_ticks > self.fire_rate:
            self.shot_ticks = now
            self.bullet_group.add(Bullet(AIR_BULLET_SPEED, 200, self.rect.center, target, False))

#will have far more animations than the basic enemies
class Boss(Enemy):
    def __init__(self, starting_pos, level = 50):
        walk_anim = [load(f"assets/BOSS/boss_walk-{i}.png").convert() for i in range(BIG_WALK_FRAMES)]
        super().__init__(starting_pos, walk_anim, BIG_WALK_MILLISECONDS, BIG_HP, BIG_SPEED, level)

        barg = [load(f"assets/BOSS/boss_barrage-{i}.png").convert() for i in range(BIG_BARRAGE_FRAMES)]
        self.barrage_anim = [Animation, Animation]

        self.barrage_anim[RIGHT] = Animation(barg, 200).set_colorkey_all("#ffffff")
        self.barrage_anim[LEFT] = self.barrage_anim[RIGHT].flip_frames(True)

        panch = [load(f"assets/BOSS/boss_punch-{i}.png").convert() for i in range(BIG_BARRAGE_FRAMES)]
        self.punch_anim = [Animation, Animation]

        self.punch_anim[RIGHT] = Animation(panch, 300).set_colorkey_all("#ffffff")
        self.punch_anim[LEFT] = self.punch_anim[RIGHT].flip_frames(True)

        self.missile_cap = 0
        self.attack_ticks = pygame.time.get_ticks()

        self.punching = False
        

    def update(self, player_position, surface_friction = DEFAULT_FRICTION):
        super().update(player_position, surface_friction)
        if not self.punching and (self.stopped or not random.randint(0, 500)):
            self.barrage(player_position)
        if not self.stopped and (self.punching or not random.randint(0, 500)): 
            self.punch()

    def punch(self):
        now = pygame.time.get_ticks()
        self.punching = True
        self.image = self.punch_anim[self.turn].update()
        if now - self.attack_ticks > 10000:
            self.attack_ticks = now
            self.speed_mult = BIG_SPEED
            self.punching = False
            return False
        self.speed_mult = BIG_SPEED * 3
        return True

    def barrage(self, player_pos: tuple):
        now = pygame.time.get_ticks()
        self.stopped = True
        self.image = self.barrage_anim[self.turn].update()
        if self.missile_cap >= BIG_MISSILE_COUNT:
            self.missile_cap = 0
            self.stopped = False
            return False

        elif now - self.attack_ticks > BIG_MISSILE_DELAY:
            self.attack_ticks = now
            self.missile_cap += 1
            self.bullet_group.add(Missile(self.rect.center, player_pos))
        return True