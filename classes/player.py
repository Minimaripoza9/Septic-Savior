import pygame

VELOCITY_THRESHOLD = 0.1
class Player(pygame.sprite.Sprite):
    def __init__(self, starting_pos = (0, 0), speed_multiplier : float = 1, starting_items: list = [], starting_health: int = 3, starting_level: int = 1):
        super().__init__()

        #sprite management
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = starting_pos

        self.turn = True #0 for left, 1 for right

        #movement
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)

        #stats
        self.speed_mult = speed_multiplier
        self.MAXHP = 3
        self.hp = starting_health
        self.items = starting_items
        self.level = starting_level
        self.damage_mult = 1.0

    def update(self, acceleration: float = 0.2, surface_friction: float = 0.2):

        #reset acceleration vector
        self.acceleration = pygame.math.Vector2(0, 0)

        #check for player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -acceleration
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = acceleration
        if keys[pygame.K_UP]:
            self.acceleration.y = -acceleration
        if keys[pygame.K_DOWN]:
            self.acceleration.y = acceleration

        if self.acceleration.magnitude() > 0:
            self.acceleration = self.acceleration.normalize() * self.speed_mult
        
        elif self.velocity.magnitude() < VELOCITY_THRESHOLD:
            self.velocity = pygame.math.Vector2(0, 0)

        self.acceleration -= self.velocity * surface_friction
        self.velocity += self.acceleration
        self.rect.topleft += self.velocity + (0.5 * self.acceleration)
    
