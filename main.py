# SEPTIC SAVIOR
# By Rose Hernandez and Sadie Ocasio
#    840-XX-XXXX        840-24-6574

import pygame, random, sys
from classes.player import Player

pygame.init()

bg_img = pygame.image.load("assets/background.png")
screen_rect = pygame.rect.Rect(0, 0, 640, 480)
screen = pygame.display.set_mode(screen_rect.bottomright, 0, 32)

player = Player(screen_rect.center)

FPS = 60
clock = pygame.time.Clock()


player_group = pygame.sprite.Group()
player_group.add(player)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.blit(bg_img, screen_rect)

    player_group.update()
    player_group.draw(screen)


    pygame.display.update()
    clock.tick(FPS)

