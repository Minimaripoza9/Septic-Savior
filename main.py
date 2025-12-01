# SEPTIC SAVIOR
# By Rose Hernandez and Sadie Ocasio
#    840-22-7356        840-24-6574

#TODO: implement basic enemies      

import pygame, random, sys
from classes.player import Player
from classes.enemy import Boss, Hound, Drone
from classes.button import Button

pygame.init()

RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"

bg_img = pygame.image.load("assets/background.png")
screen_rect = pygame.rect.Rect(0, 0, 640, 480)
screen = pygame.display.set_mode(screen_rect.bottomright, 0, 32)

title_font = pygame.font.SysFont("Phosphate", 40)
font = pygame.font.SysFont("Phospate", 15)

FPS = 60
clock = pygame.time.Clock()

mixer = pygame.mixer.music.load()


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
    enemy_group = pygame.sprite.Group()
    for e in range(ammount):
        pos = generate_random_outside(screen_rect.width, screen_rect.height)
        enemy_group.add(enemy_class(pos, level))
    return enemy_group

def exit_game():
    pygame.quit()
    sys.exit()

def game_over():

    over = True

    lose_buttons = [Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+100, 400, 50), 
                    __main__, title_font, "M A I N   M E N U", ("#1c4d09","#508016","#041a07")),

                    Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+175, 400, 50), 
                    exit_game, title_font, "Q U I T   G A M E", ("#1c4d09","#508016","#041a07"))]

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        screen.fill(("#27063b"))
        
        for button in lose_buttons:
            screen.blit(button.process(), button.buttonRect)
        
        pygame.display.flip()
        clock.tick(FPS)

def game_loop(time_limit):
    metronome = 0
    seconds = 0
    minutes = 0

    stringbean = Player(screen_rect.center, FPS)

    player_group = pygame.sprite.Group()
    player_group.add(stringbean)

    enemy_group = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
                
        screen.blit(bg_img, screen_rect)

        player_group.update(screen_rect)
        stringbean.bullet_group.update()

        enemy_group.update(stringbean.rect.center)

        player_hit = pygame.sprite.spritecollide(stringbean, enemy_group, False)
        enemy_hit = pygame.sprite.groupcollide(enemy_group, stringbean.bullet_group, False, True)

        if player_hit.__len__():
            stringbean.hit()

        for enemy in enemy_hit:
            stringbean.xp += 10 * enemy.is_killing_blow(stringbean.damage)

        enemy_level = int(pygame.math.lerp(1, 50, (minutes+(seconds/60))/7))

        #defining waves
        if minutes < time_limit:
            if (not seconds % 5) and metronome == 0:
                enemy_group.add(spawn_wave(Hound, enemy_level, 5))

            if seconds == 30 and minutes > 2 and metronome == 0:
                enemy_group.add(spawn_wave(Drone, enemy_level, 5))

            if (not seconds%15) and minutes > 1 and metronome == 0:
                enemy_group.add(spawn_wave(Hound, enemy_level, 3 * minutes))

            if (not seconds%30) and minutes > 4 and metronome == 0:
                enemy_group.add(spawn_wave(Drone, enemy_level, 3 * minutes))
                
        if (not minutes % 5) and seconds == 00 and metronome == 0:
            enemy_group.add(spawn_wave(Boss, enemy_level, minutes//5))


        #testing stuffs
        text = font.render(f"score: {stringbean.xp}", True, GREEN)
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

        enemy_group.draw(screen)
        stringbean.bullet_group.draw(screen)
        player_group.draw(screen)

        if not player_group.__len__():
            return game_over()
        if (not enemy_group.__len__()) and minutes > time_limit:
            return you_win()

        pygame.display.update()
        clock.tick(FPS)
        metronome += 1
        if metronome > FPS:
            metronome = 0
            seconds += 1
            if seconds > 60:
                seconds = 0
                minutes += 1

def you_win():
    over = True

    win_buttons = [Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+100, 400, 50), 
                    __main__, title_font, "M A I N   M E N U", ("#277f04","#769e46","#0a4e12")),

                    Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+175, 400, 50), 
                    exit_game, title_font, "Q U I T  G A M E", ("#277f04","#769e46","#0a4e12"))]
    text = title_font.render

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        screen.fill(("#b3f81e"))
        
        screen.blit(text, screen_rect.center)
        for button in win_buttons:
            screen.blit(button.process(), button.buttonRect)
        
        pygame.display.flip()
        clock.tick(FPS)

def normal_mode():
    game_loop(5)

def endless_mode():
    game_loop(sys.maxsize)

def __main__():
    start_button = Button(pygame.rect.Rect(25, 25, 200, 50),
                        normal_mode, title_font, "S  T  A  R  T",
                        ("#277f04","#769e46","#0a4e12"))
    endless_button = (Button(pygame.rect.Rect(25, 100, 200, 50), 
                               endless_mode, title_font, "E N D L E S S",
                               ("#277f04","#769e46","#0a4e12")))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        screen.blit(start_button.process(), start_button.buttonRect)
        screen.blit(endless_button.process(), endless_button.buttonRect)

        pygame.display.flip()
        clock.tick(FPS)

__main__()