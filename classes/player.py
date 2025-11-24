import pygame

V_THRESHOLD = 0.1
ACCELERATION = 0.2
class Player(pygame.sprite.Sprite):
    def __init__(self, starting_pos = (0, 0), move_speed : float = 1, starting_items: list = [], starting_health: int = 3):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = starting_pos

        self.direction_x = True #0 for left, 1 for right

        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.speed_mult = move_speed

        self.MAXHP = 3
        self.hp = starting_health
        self.items = starting_items

    def update(self, surface_friction: float = 0.2):

        #movment
        self.acceleration = pygame.math.Vector2(0,0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = ACCELERATION
        if keys[pygame.K_UP]:
            self.acceleration.y = -ACCELERATION
        if keys[pygame.K_DOWN]:
            self.acceleration.y = ACCELERATION

        if self.acceleration.magnitude() > 0:
            self.acceleration = self.acceleration.normalize() * self.speed_mult
        
        if self.velocity.magnitude() < V_THRESHOLD:
            self.velocity = pygame.math.Vector2(0, 0)

        self.acceleration -= self.velocity * surface_friction
        self.velocity += self.acceleration
        self.rect.topleft += self.velocity + (0.5 * self.acceleration)
    
