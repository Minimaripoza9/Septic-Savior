# SEPTIC SAVIOR
# By Rose Hernandez and Sadie Ocasio
#    840-22-7356        840-24-6574

import pygame, random, sys
from classes.player import Player
from classes.enemy import Boss#, Drone, Hound

pygame.init()

RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"

bg_img = pygame.image.load("assets/background.png")
screen_rect = pygame.rect.Rect(0, 0, 640, 480)
screen = pygame.display.set_mode(screen_rect.bottomright, 0, 32)

font = pygame.font.SysFont("Arial", 10)

FPS = 60
clock = pygame.time.Clock()
metronome = 0

stringbean = Player(screen_rect.center, FPS)

player_group = pygame.sprite.Group()
player_group.add(stringbean)

enemy_group = pygame.sprite.Group()
enemy_group.add(Boss((0, 0)))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.blit(bg_img, screen_rect)

    player_group.update()
    player_group.draw(screen)

    player_hit = pygame.sprite.spritecollide(stringbean, enemy_group, False)
    if player_hit.__len__():
        stringbean.hp -=1
        invincibility_timer = 5



    stringbean.bullet_group.update()
    stringbean.bullet_group.draw(screen)

    enemy_group.update(stringbean.rect.center)
    enemy_group.draw(screen)

    text = font.render(f"velX: {stringbean.velocity.x}", True, GREEN)
    screen.blit(text, (0, 0))
    text = font.render(f"velY: {stringbean.velocity.y}", True, GREEN)
    screen.blit(text, (0, 20))
    text = font.render(f"accX: {stringbean.acceleration.x}", True, RED)
    screen.blit(text, (250, 0))
    text = font.render(f"accY: {stringbean.acceleration.y}", True, RED)
    screen.blit(text, (250, 20))
    text = font.render(f"Frame: {metronome}", True, BLUE)
    screen.blit(text, (400, 0))
    text = font.render(f"accY: {stringbean.hp}", True, RED)
    screen.blit(text, (250, 40))

    for enemy in enemy_group:
        text = font.render(f"velX: {enemy.velocity.x}", True, GREEN)
        screen.blit(text, (0, 400))
        text = font.render(f"velY: {enemy.velocity.y}", True, GREEN)
        screen.blit(text, (0, 420))
        text = font.render(f"velM: {enemy.velocity.magnitude()}", True, GREEN)
        screen.blit(text, (0, 440))
        text = font.render(f"accX: {enemy.acceleration.x}", True, RED)
        screen.blit(text, (250, 400))
        text = font.render(f"accY: {enemy.acceleration.y}", True, RED)
        screen.blit(text, (250, 420))

    pygame.display.update()
    clock.tick(FPS)
    metronome += 1
    if metronome > FPS:
        metronome = 0

