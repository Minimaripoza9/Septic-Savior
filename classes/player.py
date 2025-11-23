import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, starting_pos = (0, 0), move_speed = 1, starting_items: list = [], starting_health: int = 3):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = starting_pos

        self.direction_x = True #0 for left, 1 for right
        self.direction_y = True #0 for up, 1 for down
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.speed = 10

        self.MAXHP = 3
        self.hp = starting_health
        self.items = starting_items

    def update(self, surface_friction: float = 0.2):

        self.acceleration = pygame.math.Vector2(0,0)
        current_acceleration = self.speed/10

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -current_acceleration
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = current_acceleration
        if keys[pygame.K_UP]:
            self.acceleration.y = -current_acceleration
        if keys[pygame.K_DOWN]:
            self.acceleration.y = current_acceleration

        self.acceleration -= self.velocity * surface_friction
        self.velocity += self.acceleration
        self.rect.topleft += self.velocity + (0.5 * self.acceleration)
