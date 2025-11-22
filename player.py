import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, item1, item2, health: int = 100):
        super().__init__()
        self.image = pygame.image.load("placehold_p.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.MAXFALL = 6
        self.velocity = 0
        self.MAXHP = 100
        self.hp = health

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
