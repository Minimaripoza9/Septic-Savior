# SEPTIC SAVIOR
# By Rose Hernandez and Sadie Ocasio
#    840-22-7356        840-24-6574

#TODO: implement basic enemies      

import pygame, random, sys
from classes.player import Player
from classes.enemy import Boss, Hound, Drone
from classes.button import Button
from classes.collectible import Collectible

pygame.init()

RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"

bg_img = pygame.image.load("assets/background.png")
screen_rect = pygame.rect.Rect(0, 0, 640, 480)
screen = pygame.display.set_mode(screen_rect.bottomright, 0, 32)

button_font = pygame.font.SysFont("Phosphate", 40)
font = pygame.font.SysFont("Phospate", 15)

FPS = 60
clock = pygame.time.Clock()

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
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    img = pygame.image.load("assets/game_over.png").convert()

    over = True

    lose_buttons = [Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+100, 400, 50), 
                    __main__, button_font, "M A I N   M E N U", ("#8b0000","#FF0000","#2c0202")),

                    Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+175, 400, 50), 
                    exit_game, button_font, "Q U I T   G A M E", ("#8b0000","#FF0000","#2c0202"))]

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        screen.blit(img, screen_rect.topleft)
        
        for button in lose_buttons:
            screen.blit(button.process(), button.buttonRect)
        
        pygame.display.flip()
        clock.tick(FPS)

def you_win():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    pygame.mixer.music.load("assets/Music/ATOM-BOMB.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    over = True

    img = pygame.image.load("assets/you_win.png").convert()

    win_buttons = [Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+100, 400, 50), 
                    __main__, button_font, "M A I N   M E N U", ("#7f6604","#9b9e46","#4e0a0a")),

                    Button(pygame.rect.Rect(screen_rect.centerx - 200, screen_rect.centery+175, 400, 50), 
                    exit_game, button_font, "Q U I T  G A M E", ("#7f6604","#9b9e46","#4e0a0a"))]

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        screen.blit(img, screen_rect.topleft)

        for button in win_buttons:
            screen.blit(button.process(), button.buttonRect)
        
        pygame.display.flip()
        clock.tick(FPS)

def game_loop(time_limit):
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    pygame.mixer.music.load("assets/Music/CATACOMBS.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(256)

    bark = pygame.mixer.Sound("assets/Sounds/BARK.ogg")
    chop = pygame.mixer.Sound("assets/Sounds/DRONE.ogg")
    roar = pygame.mixer.Sound("assets/Sounds/BOSS_SCARY.ogg")
    oof = pygame.mixer.Sound("assets/Sounds/DEATH.ogg")

    metronome = 0
    seconds = 0
    minutes = 0

    stringbean = Player(screen_rect.center, FPS)

    player_group = pygame.sprite.Group()
    player_group.add(stringbean)

    enemy_group = pygame.sprite.Group()

    buff_list = ["health", "xp", "hp_buff", "fr_buff", "dm_buff"]
    collectible_group = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
                
        screen.blit(bg_img, screen_rect)

        player_group.update(screen_rect)
        stringbean.bullet_group.update()

        enemy_group.update(stringbean.rect.center)
        for enemy in enemy_group:
            enemy.bullet_group.update()
            enemy.bullet_group.draw(screen)
            player_hit = pygame.sprite.spritecollide(stringbean, enemy.bullet_group, True)
            if player_hit.__len__():
                if not stringbean.invincibility:
                    oof.play()
                stringbean.hit()

        player_hit = pygame.sprite.spritecollide(stringbean, enemy_group, False)
        enemy_hit = pygame.sprite.groupcollide(enemy_group, stringbean.bullet_group, False, True)

        if player_hit.__len__():
            if not stringbean.invincibility:
                oof.play()
            stringbean.hit()

        for enemy in enemy_hit:
            stringbean.xp += enemy.lv * enemy.is_killing_blow(stringbean.damage)
            if not random.randint(0, 100):
                collectible_group.add(buff_list[random.randint])

        enemy_level = int(pygame.math.lerp(1, 50, (minutes+(seconds/60))/7))

        #defining waves
        if minutes < time_limit:
            if (not seconds % 5) and metronome == 0:
                enemy_group.add(spawn_wave(Hound, enemy_level, 5))
                bark.play()

            if seconds == 30 and minutes > 0 and metronome == 0:
                enemy_group.add(spawn_wave(Drone, enemy_level, 5))
                chop.play()

            if (not seconds%15) and minutes > 1 and metronome == 0:
                enemy_group.add(spawn_wave(Hound, enemy_level, 3 * minutes))
                bark.play()

            if (not seconds%30) and minutes > 3 and metronome == 0:
                enemy_group.add(spawn_wave(Drone, enemy_level, 3 * minutes))
                chop.play()
                
        if (not minutes % 5) and seconds == 00 and metronome == 0:
            enemy_group.add(spawn_wave(Boss, enemy_level, minutes//5))
            roar.play()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            pygame.mixer.music.load("assets/Music/FACTORY-JAM-2.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(256)


        #testing stuffs
        text = font.render(f"xp: {stringbean.xp}", True, GREEN)
        screen.blit(text, (0, 0))
        text = font.render(f"level: {stringbean.level}", True, GREEN)
        screen.blit(text, (0, 20))
        text = font.render(f"damage: {stringbean.damage}", True, RED)
        screen.blit(text, (250, 0))
        text = font.render(f"Time: {minutes}:{seconds}:{metronome}", True, BLUE)
        screen.blit(text, (250, 20))
        text = font.render(f"HEALTH: {stringbean.hp}/{stringbean.MAXHP}", True, RED)
        screen.blit(text, (400, 0))
        text = font.render(f"STAMINA: {stringbean.stamina}/100", True, RED)
        screen.blit(text, (400, 20))

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
        if (not enemy_group.__len__()) and minutes >= time_limit:
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

def normal_mode():
    game_loop(5)

def endless_mode():
    game_loop(sys.maxsize)

pygame.mixer.init()

def __main__():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/Music/ATOM-BOMB.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(256)

    img = pygame.image.load("assets/title_screen.png").convert()

    start_button = Button(pygame.rect.Rect(25, screen_rect.bottom-150, 200, 50),
                        normal_mode, button_font, "S  T  A  R  T",
                        ("#047b7f","#469e92","#0a4e12"))
    endless_button = (Button(pygame.rect.Rect(25, screen_rect.bottom - 75, 200, 50), 
                               endless_mode, button_font, "E N D L E S S",
                               ("#047b7f","#469e92","#0a4e12")))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(img, screen_rect.topleft)
        screen.blit(start_button.process(), start_button.buttonRect)
        screen.blit(endless_button.process(), endless_button.buttonRect)

        pygame.display.flip()
        clock.tick(FPS)

__main__()