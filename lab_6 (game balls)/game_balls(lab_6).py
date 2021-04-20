import numpy as np
import pygame
from pygame.draw import *
from random import randint


pygame.init()
FPS = 100
SIZE = WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode(SIZE)
WHITE = (255, 255, 255)
SPEED = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball(r):
    coord = (randint(100, 1100), randint(100, 800))
    surf = pygame.Surface((r*2, r*2))
    surf.set_colorkey(BLACK)
    surf.fill(BLACK)
    color = COLORS[randint(0, 5)]
    circle(surf, color, (r, r), r)
    ball = (surf, coord)
    return ball

def set_lvl(lvl):
    if lvl == 1:
        num_balls = 1
        r = 50
    elif lvl == 2:
        num_balls = 2
        r = 40
    elif lvl == 3:
        num_balls = 3
        r = 30
    elif lvl == 4:
        num_balls = 4
        r = 20
    elif lvl == 5:
        num_balls = 5
        r = 10
    else:
        print("Ошибка: сложность не задана!!!")
        return

    param_lvl = (r, num_balls)
    return param_lvl


def speed_lvl(lvl):
    if lvl == 1:
        speed = 5
    elif lvl == 2:
        speed = 7
    elif lvl == 3:
        speed = 9
    elif lvl == 4:
        speed = 11
    elif lvl == 5:
        speed = 13
    else:
        print("Ошибка: сложность не задана!!!")
        return

    angle = randint(0, 360) * (np.pi / 180)
    dx = np.sin(angle) * speed
    dy = np.cos(angle) * speed
    param = (speed, dx, dy)

    return param


def draw_text(surf, text, size, coord):
    font_name = pygame.font.match_font('blackarial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = coord
    surf.blit(text_surface, text_rect)


def draw_ball(ball):
    screen.blit(*ball)


def move_ball(ball, param):

    (x, y) = ball[1]
    (speed, dx, dy) = param
    r = pygame.Surface.get_width(ball[0])
    angle = randint(0, 360) * (np.pi / 180)
    move_x_1 = np.sin(angle) * speed
    move_y_1 = np.cos(angle) * speed

    if x >= WIDTH-r:
        dx = -abs(move_x_1)
        dy = move_y_1
    elif x <= 0:
        dx = abs(move_x_1)
        dy = move_y_1

    if y >= HEIGHT-r:
        dy = -abs(move_y_1)
        dx = move_x_1
    elif y <= 0:
        dy = abs(move_y_1)
        dx = move_x_1

    x += dx
    y += dy
    coord = (x, y)
    ball = (ball[0], coord)
    param = (speed, dx, dy)

    return ball, param



def click(event, ball):
    (x, y) = ball[1]
    r = pygame.Surface.get_width(ball[0])
    cord = event.pos
    if np.sqrt(abs(x - cord[0])**2 + (y - cord[1])**2) < r:
        print("Попал!")
        return True
    return False


def incr_score(score, points):

    return score + points


def draw_const_text(surf, text, size, coord):
    font_name = pygame.font.match_font('blackarial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = coord
    surf.blit(text_surface, text_rect)


clock = pygame.time.Clock()
game_over = False

finished = False
flag = False

lvl = 1
score = 0
shape = []
param = []
timer_shape = []
text = []
param_lvl = (r, num_balls) = set_lvl(lvl)

for i in range(num_balls):
    param.append(speed_lvl(lvl))
    shape.append(new_ball(r))
    timer_shape.append(pygame.time.get_ticks())




start_timer_text = pygame.time.get_ticks()
while not finished:
    clock.tick(FPS)
    screen.fill(BLACK)
    
    if game_over:
        draw_const_text(screen, "GAMEOVER ", 150, (WIDTH / 2, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        pygame.display.update()

    else:
        if score < 0:
            game_over = True
        elif score >= 0 and score <= 1000:
            lvl = 1
        elif score > 1000 and score <= 3000:
            lvl = 2
        elif score > 3000 and score <= 5000:
            lvl = 3
        elif score > 5000 and score <= 8000:
            lvl = 4
        elif score > 8000:
            lvl = 5

        param_lvl = (r, num_balls) = set_lvl(lvl)
        if num_balls != len(shape):
            shape = []
            param = []
            timer_shape = []
            text.append((("УРОВЕНЬ " + str(lvl), 100, (WIDTH/2, HEIGHT/2)), pygame.time.get_ticks()))

        for i in range(num_balls - len(shape)):
            param.append(speed_lvl(lvl))
            shape.append(new_ball(r))
            timer_shape.append(pygame.time.get_ticks())

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(num_balls):
                    flag = click(event, shape[i])
                    if flag:
                        score = incr_score(score, 100)

                        shape[i] = new_ball(r)
                        param[i] = speed_lvl(2)
                        timer_shape[i] = pygame.time.get_ticks()

                        text.append((("+100", 25, event.pos), pygame.time.get_ticks()))

        for i in range(len(shape)):
            seconds = (pygame.time.get_ticks() - timer_shape[i]) / 1000
            if seconds >= 5:
                score = incr_score(score, -100)
                text.append((("-100", 35, shape[i][1]), pygame.time.get_ticks()))
                shape[i] = new_ball(r)
                param[i] = speed_lvl(2)
                timer_shape[i] = pygame.time.get_ticks()

        for i in range(len(shape)):
            seconds = (pygame.time.get_ticks() - timer_shape[i]) / 1000
            if seconds >= 5:
                score = incr_score(score, -200)
                text.append((("-100", 35, shape[i][1]), pygame.time.get_ticks()))
                shape[i] = new_ball(r)
                param[i] = speed_lvl(2)
                timer_shape[i] = pygame.time.get_ticks()

            shape[i], param[i] = move_ball(shape[i], param[i])

        new_list = []
        for i in range(len(text)):
            seconds = (pygame.time.get_ticks() - text[i][1]) / 1000
            if seconds < 1:
                draw_text(screen, *text[i][0])
                new_list.append(text[i])
        text = new_list

        for i in range(len(shape)):
            draw_ball(shape[i])


        draw_const_text(screen, "Очков: " + str(score), 50,(WIDTH/2, 10))
        draw_const_text(screen, "Уровень: " + str(lvl), 50, (WIDTH / 6, 10))


        pygame.display.update()

pygame.quit()
