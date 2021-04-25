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
RED = '#ed0b0e'
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = '#252527'
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
FONT_BUTTON = 'segoeuisemibold'
FONT_NAME_GAME = 'mistral'


def new_ball(r):
    coord = (randint(0, WIDTH - 2*r), randint(0, HEIGHT - 2*r))
    surf = pygame.Surface((r*2, r*2))
    surf.set_colorkey(BLACK)
    surf.fill(BLACK)
    color = COLORS[randint(0, 5)]
    circle(surf, color, (r, r), r)
    ball = (surf, coord)
    return ball


def check_score():
    global lvl
    global game_over
    global game
    if score < 0:
        game_over = True
        game = False
    elif 0 <= score < 1000:
        lvl = 1
    elif 1000 <= score < 3000:
        lvl = 2
    elif 3000 <= score < 5000:
        lvl = 3
    elif 5000 <= score < 8000:
        lvl = 4
    elif score > 8000:
        lvl = 5


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
    r = pygame.Surface.get_width(ball[0])/2
    angle = randint(0, 360) * (np.pi / 180)
    move_x_1 = np.sin(angle) * speed
    move_y_1 = np.cos(angle) * speed

    if x >= WIDTH - 2*r:
        dx = -abs(move_x_1)
        dy = move_y_1
    elif x <= 0:
        dx = abs(move_x_1)
        dy = move_y_1

    if y >= HEIGHT - 2*r:
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
    r = pygame.Surface.get_width(ball[0])/2
    mouse = event.pos

    print(ball[1])



    if np.sqrt(( abs(r + x) - abs(mouse[0]) )**2 + ( abs(r + y) - abs(mouse[1]) )**2) <= r:

        print(mouse)
        return True
    return False


def incr_score(score, points):

    return score + points


def draw_const_text(surf, text, size, font_name, coord):
    font_name = pygame.font.match_font(font_name)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()

    text_rect.center = coord

    surf.blit(text_surface, text_rect)


def draw_button(text, size, coord, color):
    """
    Функция рисует кнопку по заданным паратметрам
    (тест в кнопке всегда белый)
    Координата X по центру копки.
    :param text: Текст на кнопке
    :param size: размер прямоугольника
    :param coord: координаты центра по x и наивысшей точки по y
    :param color: Цвет заливки
    :return:
    """
    surf = pygame.Surface(size)
    surf.set_colorkey(BLACK)
    surf.fill(color)

    rect_button = surf.get_rect()

    rect(surf, (0, 0, 0), rect_button, 5)
    rect_button.midtop = coord

    draw_const_text(surf, text, int(rect_button.height * 0.65),
                    FONT_BUTTON, (rect_button.width/2, rect_button.height/2-8))
    screen.blit(surf, rect_button)


def check_push_button(event, button_coord, size_button):
    mouse = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_coord[0] - size_button[0] / 2 <= mouse[0] <= button_coord[0] + size_button[0] / 2 and \
                button_coord[1] <= mouse[1] <= button_coord[1] + size_button[1]:
            print("Кнопка нажата!")
            return True
    else:
        return False


def render_start(start_button_coord, exit_button_coord, size_button):
    start_color_light = '#35a76e'
    start_color_dark = '#21935a'

    exit_color_light = '#F6464B'
    exit_color_dark = '#ed0b0e'

    mouse = pygame.mouse.get_pos()

    # отрисовка кнопок
    if start_button_coord[0] - size_button[0]/2 <= mouse[0] <= start_button_coord[0] + size_button[0]/2 and \
       start_button_coord[1] <= mouse[1] <= start_button_coord[1] + size_button[1]:
        draw_button('Начать игру', size_button, start_button_coord, start_color_light)
    else:
        draw_button('Начать игру', size_button, start_button_coord,  start_color_dark)

    if exit_button_coord[0] - size_button[0]/2 <= mouse[0] <= exit_button_coord[0] + size_button[0]/2 and \
       exit_button_coord[1] <= mouse[1] <= exit_button_coord[1] + size_button[1]:
        draw_button('Выход', size_button, exit_button_coord, exit_color_light)
    else:
        draw_button('Выход', size_button, exit_button_coord,  exit_color_dark)

    # отрисовка названия игры
    font_name = pygame.font.match_font(FONT_NAME_GAME)
    font = pygame.font.Font(font_name, 200)
    text_white = font.render('AIM', True, WHITE)
    text_red = font.render('TRAINER', True, RED)
    width_surf = text_white.get_width() + text_red.get_width()
    height_surf = text_white.get_height() + text_red.get_height()
    surf = pygame.Surface((width_surf, height_surf))
    surf.set_colorkey(BLACK)
    surf.fill(BLACK)
    surf.blit(text_white, (0, 0))
    surf.blit(text_red, (text_white.get_width(), 0))
    text_rect = surf.get_rect()
    text_rect.midtop = (WIDTH / 2, HEIGHT / 6)
    screen.blit(surf, text_rect)


def check_figure_timer(shape, timer_shape):
    global score
    for i in range(len(shape)):
        seconds = (pygame.time.get_ticks() - timer_shape[i]) / 1000
        if seconds >= 5:
            score = incr_score(score, -100)
            text.append((("-100", 35, shape[i][1]), pygame.time.get_ticks()))
            shape[i] = new_ball(r)
            param[i] = speed_lvl(2)
            timer_shape[i] = pygame.time.get_ticks()

        shape[i], param[i] = move_ball(shape[i], param[i])


def render_game_over():
    draw_const_text(screen, "GAMEOVER ", 150, FONT_BUTTON, (WIDTH / 2, HEIGHT / 10))


clock = pygame.time.Clock()

start_button_coord = (WIDTH / 2, HEIGHT / 2)
exit_button_coord = (WIDTH / 2, 4*HEIGHT / 6)
size_button = (500, 100)

rect(screen, GREEN, (WIDTH / 2, HEIGHT / 2, 500, 100))

start_menu = True
game = False
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

start_timer_text = pygame.time.get_ticks()

while not finished:
    clock.tick(FPS)
    screen.fill(BLACK)
    check_score()

    if start_menu:
        render_start(start_button_coord, exit_button_coord, size_button)

    if game_over:
        render_game_over()



    for i in range(num_balls - len(shape)):
        param.append(speed_lvl(lvl))
        shape.append(new_ball(r))
        timer_shape.append(pygame.time.get_ticks())

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            finished = True

        elif start_menu:
            if check_push_button(event, start_button_coord, size_button):
                start_menu = False
                game = True
                print('Кнопка Старт нажата!')
            if check_push_button(event, exit_button_coord, size_button):
                start_menu = False
                finished = True
                print('Кнопка Выход нажата!')

        elif event.type == pygame.MOUSEBUTTONDOWN:

            for i in range(num_balls):
                flag = click(event, shape[i])

                if flag:
                    score = incr_score(score, 100)
                    shape[i] = new_ball(r)
                    param[i] = speed_lvl(2)
                    timer_shape[i] = pygame.time.get_ticks()
                    text.append((("+100", 25, event.pos), pygame.time.get_ticks()))

    if game:
        param_lvl = (r, num_balls) = set_lvl(lvl)
        if num_balls != len(shape):
            param_lvl = (r, num_balls) = set_lvl(lvl)
            shape = []
            param = []
            timer_shape = []


        text.append((("Уровень: " + str(lvl), 100, (WIDTH/2, HEIGHT/2)), pygame.time.get_ticks()))

        check_figure_timer(shape, timer_shape)

        new_list = []
        for i in range(len(text)):
            seconds = (pygame.time.get_ticks() - text[i][1]) / 1000
            if seconds < 1:
                draw_text(screen, *text[i][0])
                new_list.append(text[i])
        text = new_list

        for i in range(len(shape)):
            draw_ball(shape[i])

        draw_const_text(screen, "Очков: " + str(score), 50, FONT_BUTTON, (WIDTH / 2, HEIGHT / 20))
        draw_const_text(screen, "Уровень: " + str(lvl), 50, FONT_BUTTON, (WIDTH / 7, HEIGHT / 20))
        draw_const_text(screen, "♡♡♡♡♡", 50, FONT_BUTTON, (8 * WIDTH / 9, HEIGHT / 20))



    pygame.display.update()

pygame.quit()
