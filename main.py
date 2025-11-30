# SEPTIC SAVIOR
# By Rose Hernandez and Sadie Ocasio
#    840-22-7356        840-24-6574

#TODO: implement basic enemies      

import pygame, random, sys
from classes.player import Player
from classes.enemy import Boss, Hound, Drone

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
seconds = 0
minutes = 0

stringbean = Player(screen_rect.center, FPS)

player_group = pygame.sprite.Group()
player_group.add(stringbean)

enemy_group = pygame.sprite.Group()

def generate_random_outside(width, height):
    p = random.randint(0, (2 * width) + (2 * height))
    if p < (width + height):
        if p < width:
            x = p
            y = 0
        else:
            x = width
            y = p - width
    else:
        p = p - (width + height)
        if p < width:
            x = width - p
            y = height
        else:
            x = 0
            y = height - (p - width)
    return (x, y)

def spawn_wave(enemy_class, level, ammount):
    for enemy in range(ammount):
        pos = generate_random_outside(screen_rect.width, screen_rect.height)
        enemy_group.add(enemy_class(pos, level))

spawn_wave(Hound, 1, 4)

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
        stringbean.hit()

    enemy_hit = pygame.sprite.groupcollide(enemy_group, stringbean.bullet_group, False, True)

    for enemy in enemy_hit:
        enemy.hit(stringbean.damage)


    stringbean.bullet_group.update()
    stringbean.bullet_group.draw(screen)

    enemy_group.update(stringbean.rect.center)
    enemy_group.draw(screen)

    enemy_level = int(pygame.math.lerp(1, 50, (minutes+(seconds/60))/7))

    #defining waves
    if (not seconds%5) and minutes < 5 and metronome == 0:
        spawn_wave(Hound, enemy_level, 5)
    if seconds == 30 and minutes > 2 and minutes < 7 and metronome == 0:
        spawn_wave(Drone, enemy_level, 5)
    if (not seconds%15) and minutes > 1 and minutes < 7 and metronome == 0:
        spawn_wave(Hound, enemy_level, 10)
    if (not seconds%30) and minutes > 4 and minutes < 7 and metronome == 0:
        spawn_wave(Drone, enemy_level, 15)
    if minutes == 7 and seconds == 30 and metronome == 0:
        spawn_wave(Boss, enemy_level, 1)


    #testing stuffs
    text = font.render(f"velX: {stringbean.velocity.x}", True, GREEN)
    screen.blit(text, (0, 0))
    text = font.render(f"velY: {stringbean.velocity.y}", True, GREEN)
    screen.blit(text, (0, 20))
    text = font.render(f"accX: {stringbean.acceleration.x}", True, RED)
    screen.blit(text, (250, 0))
    text = font.render(f"accY: {stringbean.acceleration.y}", True, RED)
    screen.blit(text, (250, 20))
    text = font.render(f"Time: {minutes}:{seconds}:{metronome}", True, BLUE)
    screen.blit(text, (400, 0))
    text = font.render(f"HEALTH: {stringbean.hp}", True, RED)
    screen.blit(text, (250, 40))

    text = font.render(f"enemy count: {enemy_group.__len__()}", True, GREEN)
    screen.blit(text, (0, 400))
    text = font.render(f"enemy level: {enemy_level}", True, GREEN)
    screen.blit(text, (0, 420))

    #/testing stuffs

    pygame.display.update()
    clock.tick(FPS)
    metronome += 1
    if metronome > FPS:
        metronome = 0
        seconds += 1
        if seconds > 60:
            seconds = 0
            minutes += 1

