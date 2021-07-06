# music: 'Journey to the East Rocks.ogg', Alexandr Zhelanov, <https://soundcloud.com/alexandr-zhelanov>, licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

import time
import random
import numpy as np
import pygame
import webbrowser
from os import path
from pygame.draw import *
from random import randint
from datetime import datetime

FPS = 60
pygame.init()
clock = pygame.time.Clock()

data_dir = path.join(path.dirname(__file__), 'data')

snd_dir = path.join(path.dirname(__file__), 'snd')
music_menu = pygame.mixer.Sound(path.join(snd_dir, 'Journey to the East Rocks.ogg'))
music_menu.set_volume(0.3)
music_menu.play(-1)
sound_button = pygame.mixer.Sound(path.join(snd_dir, 'click_button.mp3'))
sound_button_space = pygame.mixer.Sound(path.join(snd_dir, 'button_space.mp3'))
sound_button_seal = pygame.mixer.Sound(path.join(snd_dir, 'button_all.mp3'))
sound_name_end = pygame.mixer.Sound(path.join(snd_dir, 'name_end.mp3'))
sound_click_ball = pygame.mixer.Sound(path.join(snd_dir, 'click_ball.mp3'))
sound_click_heart = pygame.mixer.Sound(path.join(snd_dir, 'click_heart.mp3'))
sound_miss = pygame.mixer.Sound(path.join(snd_dir, 'miss.mp3'))
sound_time_end = pygame.mixer.Sound(path.join(snd_dir, 'poof.mp3'))
sound_game_over = pygame.mixer.Sound(path.join(snd_dir, 'game_over.mp3'))
sound_record = pygame.mixer.Sound(path.join(snd_dir, 'record.mp3'))
sound_new_record = pygame.mixer.Sound(path.join(snd_dir, 'record_top_1.mp3'))


f = open(path.join(data_dir, 'about_game.txt'), 'r', encoding="utf8")
text_about_game = ""
for line in f:
    text_about_game += line
text_about_game = text_about_game.split('\n')

pygame.display.set_caption("AIMTRAINER")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SIZE_DEFAULT = (int(pygame.display.Info().current_w/1.3), int(pygame.display.Info().current_h/1.3))
SIZE = WIDTH, HEIGHT = SIZE_DEFAULT

WHITE = (255, 255, 255)

RED = '#ed0b0e'
GREEN = '#21935a'
ORANGE = '#FECB42'
BLACK = '#252527'
COLORS = ['#FF7373', '#FF9D73', '#A62525', '#FFFFFF', '#BFBFBF', '#A65353', '#A67853']

FONT_BUTTON = 'segoeuisemibold'
FONT_NAME_GAME = 'mistral'
RADIUS_BALL_MIN = 20
RADIUS_BALL_MAX = 60
color_tick = []


def set_fullscreen():
    global screen
    global SIZE
    global WIDTH
    global HEIGHT
    if settings['fullscreen']:
        screen = pygame.display.set_mode(MONITOR_SIZE, pygame.DOUBLEBUF)
        pygame.display.toggle_fullscreen()
    else:
        pygame.display.toggle_fullscreen()
        screen = pygame.display.set_mode(SIZE_DEFAULT)
    SIZE = WIDTH, HEIGHT = screen.get_size()


def timer():
    size_font = round(0.06024 * HEIGHT)
    str_flag = ""
    if pause:
        time = time_pause - timer_start - sum_time_pause
    elif start_game:
        time = 3000-(pygame.time.get_ticks() - timer_start)
        str_flag = "-"
    elif pre_game_over:
        time = statistics_dict["duration"]
    else:
        time = pygame.time.get_ticks() - timer_start - sum_time_pause
    if time <= 0:
        time = 0
    minute = int(time / 1000 // 60)
    second = int(time / 1000 % 60)
    ms = time % 1000
    text = str_flag + str(minute).zfill(2) + ":" + str(second).zfill(2) + "." + str(ms).zfill(3)
    font_name = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font_name, size_font)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midleft = (0.9458 * WIDTH - 0.271*HEIGHT, RECT_FIELD[1] / 2)
    screen.blit(text_surface, text_rect)


def new_ball():
    coord = (randint(int(RECT_FIELD[0] + RADIUS_BALL_MAX), int(WIDTH - RECT_FIELD[0] - RADIUS_BALL_MAX)),
             randint(int(RADIUS_BALL_MAX + RECT_FIELD[1]), int(HEIGHT - RECT_FIELD[1] - RADIUS_BALL_MAX)))
    if int(settings["select_ball"]) == 0 or start_menu:
        color = COLORS[randint(0, len(COLORS)-1)]
    else:
        color = COLORS[int(settings["select_ball"])-1]

    start_time = pygame.time.get_ticks()
    param = speed_lvl()
    ball = {
            'radius': RADIUS_BALL_MIN,
            'color': color,
            'coordinate': coord,
            'start_life': start_time
            }
    ball = ball | param
    return ball


def speed_lvl():
    speed = 4
    angle = randint(0, 360) * (np.pi / 180)
    dx = np.sin(angle) * speed
    dy = np.cos(angle) * speed
    return {'speed': speed,
            'dx': dx,
            'dy': dy}


def modification_bal(ball):
    speed = (RADIUS_BALL_MAX - RADIUS_BALL_MIN) / 3000
    time = (pygame.time.get_ticks() - ball['start_life'])
    if time/1000 <= 3:
        ball['radius'] = RADIUS_BALL_MIN + speed * time
    elif 3 < time/1000 <= 6:
        time = 6000 - time
        ball['radius'] = RADIUS_BALL_MIN + speed * time
    elif time/1000 > 6 and (start_menu or statistics):
        ball['start_life'] = pygame.time.get_ticks()


def draw_heart(heart):
    for i in range(len(heart)):
        screen.blit(heart[i]["surf"], heart[i]['rect'])


def check_time_heart(heart):
    global text
    list_del_heart = []
    for i in range(len(heart)):
        sec = (pygame.time.get_ticks() - heart[i]["time"]) / 1000
        if sec > 3:
            if statistics_dict["score"] >= 0:
                statistics_dict["score"] += -50
                statistics_dict["loss"] += 1
                text.append((('-50', round(0.02 * HEIGHT), (heart[i]['rect'].x + 65/2, heart[i]['rect'].y + 65/2), RED), pygame.time.get_ticks()))
                sound_time_end.play()
                list_del_heart.append(heart[i])
    for i in range(len(list_del_heart)):
        heart.remove(list_del_heart[i])


def move_heart(heart):
    (x, y) = (heart['rect'].x, heart['rect'].y)
    angle = randint(0, 360) * (np.pi / 180)
    move_x_1 = np.sin(angle) * heart['speed']
    move_y_1 = np.cos(angle) * heart['speed']
    if x >= WIDTH - RECT_FIELD[0] - heart['rect'].w:
        heart['dx'] = -abs(move_x_1)
        heart['dy'] = move_y_1
    elif x <= RECT_FIELD[0]:
        heart['dx'] = abs(move_x_1)
        heart['dy'] = move_y_1
    if y >= HEIGHT - RECT_FIELD[1] - heart['rect'].h:
        heart['dy'] = -abs(move_y_1)
        heart['dx'] = move_x_1
    elif y <= RECT_FIELD[1]:
        heart['dy'] = abs(move_y_1)
        heart['dx'] = move_x_1
    x += heart['dx']
    y += heart['dy']
    (heart['rect'].x, heart['rect'].y) = (x, y)


def heart():
    w = 65
    h = w - w / 13
    surf = pygame.Surface((w, h))
    surf.set_colorkey(BLACK)
    surf.fill(BLACK)
    # радиус окружностей
    r = w/3.25
    # вычесление центра второй окружности
    x_0 = 2*r + 1/4*r
    # вычесление синуса и косинуса угла касания
    sin_a = np.sin(np.radians(180 + 45))
    cos_a = np.cos(np.radians(180 + 45))
    # координаты точки касания на окружности
    X = r + cos_a * r + 2
    Y = r - sin_a * r
    # треугольник
    p1 = (w / 2, h)
    p2 = (X, Y)
    p3 = (x_0 + r - X, Y)
    polygon(surf, RED, (p1, p2, p3))
    # две окружности
    circle(surf, RED, (r, r), r)
    circle(surf, RED, (x_0, r), r)

    coord = (randint(int(RECT_FIELD[0]), int(WIDTH - RECT_FIELD[0] - w)),
             randint(int(RECT_FIELD[1]), int(HEIGHT - RECT_FIELD[1] - h)))

    rect_heart = pygame.Rect(coord[0], coord[1], w, h)

    speed = 6
    angle = randint(0, 360) * (np.pi / 180)
    dx = np.sin(angle) * speed
    dy = np.cos(angle) * speed
    heart = {
        "surf": surf,
        "rect": rect_heart,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "r": r,
        "x_0": x_0,
        "time": pygame.time.get_ticks(),
        "speed": speed,
        "dx": dx,
        "dy": dy,
    }
    return heart


def check_score():
    global last_game_stat_norm
    global last_game_stat_hard
    global render_statistics_list
    global top_hard_list
    global top_norm_list
    global lvl
    global pre_game_over
    global game
    global num_balls
    global index_text_pre_game_over
    index_text_pre_game_over = -1
    if statistics_dict['score'] < 0 or health <= 0:
        music_menu.set_volume(0.05)
        sound_game_over.play()
        pre_game_over = True
        render_statistics_list = []
        game = False
        settings["num_game"] += 1
        statistics_dict["lvl"] = lvl
        time = pygame.time.get_ticks() - timer_start - sum_time_pause
        statistics_dict["duration"] = time
        time_re = statistics_dict["time"]
        if statistics_dict["hit"] == 0:
            statistics_dict["time"] = 0
        else:
            statistics_dict["time"] = round(statistics_dict["time"] / statistics_dict["hit"])
        if difficulty_master:
            sorted_top_list(top_hard_list)
            write_file_top_list("top_hard.txt", top_hard_list)
            top_hard_list = read_list_game("top_hard.txt")
            write_last_game_stat("last_game_hard.txt", statistics_dict)
            last_game_stat_hard = read_last_game_stat("last_game_hard.txt")
        else:
            sorted_top_list(top_norm_list)
            write_file_top_list("top_norm.txt", top_norm_list)
            top_norm_list = read_list_game("top_norm.txt")
            write_last_game_stat("last_game_norm.txt", statistics_dict)
            last_game_stat_norm = read_last_game_stat("last_game_norm.txt")
        all_game_list.append(statistics_dict)
        write_file_end("all_game.txt")
        statistics_dict["time"] = time_re
        write_settings()
        read_settings()
    elif statistics_dict['score'] > lvl * 1.5 * 1000 + (lvl*10)**2 - 1:
        lvl += 1


def set_lvl(lvl):
    num_balls = 1 + lvl
    return num_balls


def draw_text(surf, text, size, coord, color=WHITE):
    font_name = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = coord
    surf.blit(text_surface, text_rect)


def draw_ball(ball):
    circle(screen, ball['color'], ball['coordinate'], ball['radius'])


def move_ball(ball):
    (x, y) = ball['coordinate']
    angle = randint(0, 360) * (np.pi / 180)
    move_x_1 = np.sin(angle) * ball['speed']
    move_y_1 = np.cos(angle) * ball['speed']

    if x + ball['dx'] >= WIDTH - RECT_FIELD[0] - ball['radius']:
        ball['dx'] = -abs(move_x_1)
        ball['dy'] = move_y_1
    elif x + ball['dx'] <= RECT_FIELD[0] + ball['radius']:
        ball['dx'] = abs(move_x_1)
        ball['dy'] = move_y_1

    if y + ball['dy'] >= HEIGHT - RECT_FIELD[1] - ball['radius']:
        ball['dy'] = -abs(move_y_1)
        ball['dx'] = move_x_1
    elif y + ball['dy'] <= ball['radius'] + RECT_FIELD[1]:
        ball['dy'] = abs(move_y_1)
        ball['dx'] = move_x_1

    x += ball['dx']
    y += ball['dy']
    ball['coordinate'] = (x, y)


def click(balls, heart, text):
    global health
    global statistics_dict
    miss_flag = True
    mouse = pygame.mouse.get_pos()

    for i in reversed(range(len(balls))):
        (x, y) = balls[i]['coordinate']
        if np.sqrt((x - mouse[0]) ** 2 + (y - mouse[1]) ** 2) <= balls[i]['radius']:
            miss_flag = False
            statistics_dict["hit"] += 1
            statistics_dict["score"] += 100
            if statistics_dict["min_time"] >= pygame.time.get_ticks() - shape["Balls"][i]['start_life'] or statistics_dict["min_time"] == 0:
                statistics_dict["min_time"] = pygame.time.get_ticks() - shape["Balls"][i]['start_life']
            if statistics_dict["max_time"] <= pygame.time.get_ticks() - shape["Balls"][i]['start_life']:
                statistics_dict["max_time"] = pygame.time.get_ticks() - shape["Balls"][i]['start_life']
            statistics_dict["time"] += pygame.time.get_ticks() - shape["Balls"][i]['start_life']

            text.append(((str(pygame.time.get_ticks() - shape["Balls"][i]['start_life']) + 'ms', round(0.02 * HEIGHT), mouse, GREEN),
                         pygame.time.get_ticks()))
            balls[i] = new_ball()
            sound_click_ball.play()
            return

    heart_del = []
    for i in range(len(heart)):
        if heart[i]["rect"].collidepoint(mouse):
            # координаты центров окружностей
            x_circle = heart[i]["rect"].x + heart[i]["r"]
            y_circle = heart[i]["rect"].y + heart[i]["r"]
            x_circle_0 = heart[i]["rect"].x + heart[i]["x_0"]
            # координаты мыши на плоскости сердца
            x = mouse[0] - heart[i]["rect"].x
            y = mouse[1] - heart[i]["rect"].y

            # Вычисляет положение точки (x_0, y_0) относительно прямой
            def point(xa, ya, xb, yb, x_0, y_0):
                return (xa - x_0) * (yb - ya) - (xb - xa) * (ya - y_0)

            alpha = point(*heart[i]['p1'], *heart[i]['p2'], x, y)
            betta = point(*heart[i]['p2'], *heart[i]['p3'], x, y)
            gamma = point(*heart[i]['p3'], *heart[i]['p1'], x, y)

            if np.sqrt((x_circle - mouse[0])**2 + (y_circle - mouse[1])**2) <= heart[i]["r"] or \
               np.sqrt((x_circle_0 - mouse[0])**2 + (y_circle - mouse[1])**2) <= heart[i]["r"] or \
               (alpha >= 0 and betta >= 0 and gamma >= 0) or (alpha <= 0 and betta <= 0 and gamma <= 0):
                statistics_dict["hit"] += 1
                statistics_dict["score"] += 50
                if statistics_dict["min_time"] >= pygame.time.get_ticks() - heart[i]['time'] or statistics_dict["min_time"] == 0:
                    statistics_dict["min_time"] = pygame.time.get_ticks() - heart[i]['time']
                if statistics_dict["max_time"] <= pygame.time.get_ticks() - heart[i]['time']:
                    statistics_dict["max_time"] = pygame.time.get_ticks() - heart[i]['time']
                statistics_dict["time"] += pygame.time.get_ticks() - heart[i]['time']
                if health != 5:
                    health += 1
                text.append((('♡', round(0.043*HEIGHT), mouse, RED), pygame.time.get_ticks()))
                heart_del.append(heart[i])
                sound_click_heart.play()
                miss_flag = False

    for i in range(len(heart_del)):
        heart.remove(heart_del[i])

    if miss_flag and (WIDTH * 0.02 < mouse[0] < WIDTH - (WIDTH * 0.02) and (HEIGHT / 10 < mouse[1] < HEIGHT - HEIGHT / 10)):
        if statistics_dict["score"] >= 0 and statistics_dict["hit"] != 0:
            statistics_dict["score"] += -10
        statistics_dict["miss"] += 1
        text.append((('Мимо!', round(0.02 * HEIGHT), mouse, RED), pygame.time.get_ticks()))
        sound_miss.play()



def draw_const_text(surf, text, size_font, font_name, coord, color=WHITE, center=True):
    font_name = pygame.font.match_font(font_name)
    font = pygame.font.Font(font_name, size_font)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = coord
        surf.blit(text_surface, text_rect)
    else:
        text_rect.midleft = coord
        surf.blit(text_surface, text_rect)


def draw_button(button_rect, text, color):
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
    rect(screen, color, button_rect, 0)
    rect(screen, (0, 0, 0), button_rect, 4)
    draw_const_text(screen, text, int(button_rect.height * 0.65),
                    FONT_BUTTON, (button_rect.centerx, button_rect.centery - 5))


def check_push_button(button_rect):
    mouse = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse):
        sound_button.play()
        return True
    else:
        return False


def render_start(button_start_rect, button_exit_rect, button_statistics_rect, button_standard, button_master, button_fullscreen, button_window, button_info):
    global settings
    global difficulty_master
    global about_game
    global input_name

    start_color_light = '#35a76e'
    start_color_dark = '#21935a'

    exit_color_light = '#F6464B'
    exit_color_dark = '#ed0b0e'

    statistics_color_light = '#FED974'
    statistics_color_dark = '#FECB42'

    mouse = pygame.mouse.get_pos()
    # отрисовка кнопок
    if button_start_rect.collidepoint(mouse) and not about_game and not input_name:
        draw_button(button_start_rect.copy(), 'Начать игру', start_color_light)
    else:
        draw_button(button_start_rect.copy(), 'Начать игру', start_color_dark)

    if button_statistics_rect.collidepoint(mouse) and not about_game and not input_name:
        draw_button(button_statistics_rect.copy(), 'Статистика', statistics_color_light)
    else:
        draw_button(button_statistics_rect.copy(), 'Статистика', statistics_color_dark)

    if button_exit_rect.collidepoint(mouse) and not about_game and not input_name:
        draw_button(button_exit_rect.copy(), 'Выход', exit_color_light)
    else:
        draw_button(button_exit_rect.copy(), 'Выход', exit_color_dark)

    font = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font, 25)
    # Отрисовка кнопки Об игре
    if button_info.collidepoint(mouse) and not about_game and not input_name:
        text = font.render('Об игре (I)', True, WHITE)  # навели курсор на активную
        screen.blit(text, button_info)
    else:
        text = font.render('Об игре (I)', True, '#D7D7D7')  # клавиша активна
        screen.blit(text, button_info)

    # отрисовка кнопки рижима экрана
    font = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font, 25)

    if settings['fullscreen']:
        if button_window.collidepoint(mouse) and not about_game and not input_name:
            text = font.render('В окне (F)', True, WHITE)  # навели курсор на активную
            screen.blit(text, button_window)
        else:
            text = font.render('В окне (F)', True, '#D7D7D7')  # клавиша активна
            screen.blit(text, button_window)
    else:
        if button_fullscreen.collidepoint(mouse) and not about_game and not input_name:
            text = font.render('На весь экран (F)', True, WHITE)  # навели курсор на активную
            screen.blit(text, button_fullscreen)
        else:
            text = font.render('На весь экран (F)', True, '#D7D7D7')  # клавиша активна
            screen.blit(text, button_fullscreen)

    # отрисовка сложности
    # Стандарт и Про
    # difficulty
    font = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font, round(0.02777 * HEIGHT))
    if not difficulty_master:
        text = font.render('Стандарт', True, '#848484')  # клавиша не активна
        screen.blit(text, button_standard)
    else:
        if button_standard.collidepoint(mouse):
            text = font.render('Стандарт', True, WHITE)  # навели курсор на активную
            screen.blit(text, button_standard)
        else:
            text = font.render('Стандарт', True, '#D7D7D7')   # клавиша активна
            screen.blit(text, button_standard)

    if difficulty_master:
        text = font.render('Мастер', True, '#848484')  # клавиша не активна
        screen.blit(text, button_master)
    else:
        if button_master.collidepoint(mouse):
            '#D7D7D7'
            text= font.render('Мастер', True, WHITE)  # навели курсор на активную
            screen.blit(text, button_master)
        else:
            text = font.render('Мастер', True, '#D7D7D7')  # клавиша активна
            screen.blit(text, button_master)
    # отрисовка названия игры
    font_name = pygame.font.match_font(FONT_NAME_GAME)
    if settings['fullscreen']:
        font = pygame.font.Font(font_name, 300)
    else:
        font = pygame.font.Font(font_name, int(300/1.3))
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
    text_rect.midtop = (WIDTH / 2, HEIGHT / 6 - 50)
    screen.blit(surf, text_rect)


def check_figure_timer(balls, text):
    global statistics_dict
    global health
    mouse = pygame.mouse.get_pos()
    for i in range(len(balls)):
        seconds = (pygame.time.get_ticks() - balls[i]['start_life']) / 1000
        if seconds >= 6:
            if statistics_dict["score"] >= 0:
                statistics_dict["score"] += -100
                statistics_dict["loss"] += 1
                health += -1
                text.append((('Мимо!', round(0.02 * HEIGHT), mouse, RED), pygame.time.get_ticks()))
                text.append((('-100', round(0.02 * HEIGHT), balls[i]["coordinate"], RED), pygame.time.get_ticks()))
                text.append((('-100', round(0.02 * HEIGHT), balls[i]["coordinate"], RED), pygame.time.get_ticks()))
                sound_time_end.play()
                balls[i] = new_ball()


def sorted_top_list(list_top):
    list_top.append(statistics_dict)
    def keyFunc(item):
        return int(item["score"])
    list_top.sort(key=keyFunc, reverse = True)
    return list_top


def render_game_over(button_menu, button_new_game):
    start_color_light = '#35a76e'
    start_color_dark = '#21935a'

    statistics_color_light = '#FED974'
    statistics_color_dark = '#FECB42'

    mouse = pygame.mouse.get_pos()
    # отрисовка кнопок
    if button_new_game.collidepoint(mouse):
        draw_button(button_new_game.copy(), 'Новая игра', start_color_light)
    else:
        draw_button(button_new_game.copy(), 'Новая игра', start_color_dark)

    if button_menu.collidepoint(mouse):
        draw_button(button_menu.copy(), 'Главное меню', statistics_color_light)
    else:
        draw_button(button_menu.copy(), 'Главное меню', statistics_color_dark)

    for dict_table in render_statistics_list:
        draw_statistics(dict_table)


def render_about_game(button):
    global rect_egg
    surf = pygame.Surface((int(WIDTH / 1.5), int(HEIGHT / 1.5)))
    surf.fill(BLACK)
    rect(surf, (0, 0, 0), (0, 0, WIDTH / 1.5, HEIGHT / 1.5), 8)

    font = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font, int(WIDTH * 0.068))
    text = font.render("ОБ ИГРЕ", True, WHITE)
    rect_text = text.get_rect()
    rect_text.midtop = (surf.get_width() / 2, surf.get_height() * 0.02)
    surf.blit(text, rect_text)

    i = 0
    font = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font, int(0.0203 * WIDTH))
    for line in text_about_game:
        if i == 1:
            font = pygame.font.match_font(FONT_BUTTON)
            font = pygame.font.Font(font, int(0.01355 * WIDTH))
        if line.find('Автор') >= 0:
            font = pygame.font.match_font(FONT_BUTTON)
            font = pygame.font.Font(font, int(0.0169 * WIDTH))
        text = font.render(line, True, WHITE)
        rect_text = text.get_rect()

        rect_text.midtop = (surf.get_width() / 2, surf.get_height() * 0.3 + i*int(0.0203 * WIDTH))
        if line.find('Автор') >= 0:
            i += 0.5
        if line.find('GitHub') >= 0:
            rect_egg = rect_text
        surf.blit(text, rect_text)
        i += 1

    screen.blit(surf, ((WIDTH - WIDTH / 1.5) / 2, (HEIGHT - HEIGHT / 1.5) / 2))

    color_light = '#FED974'
    color_dark = '#FECB42'
    mouse = pygame.mouse.get_pos()
    if button.collidepoint(mouse):
        draw_button(button, "Назад", color_light)
    else:
        draw_button(button, "Назад", color_dark)


def render_input_name(button_back, button_start, list_rect_balls, color_tick):
    mouse = pygame.mouse.get_pos()
    surf = pygame.Surface((int(WIDTH / 1.5), int(HEIGHT / 1.5)))
    surf.fill(BLACK)
    rect(surf, (0, 0, 0), (0, 0, WIDTH / 1.5, HEIGHT / 1.5), 8)

    draw_const_text(surf, "Введите имя", int(WIDTH * 0.068), FONT_BUTTON,
                    (surf.get_width() / 2, surf.get_height() * 0.15))

    polygon(surf, WHITE, ((surf.get_width()/5, surf.get_height()/2), (4*surf.get_width()/5, surf.get_height()/2)), 3)

    if len(statistics_dict["name"]) == 0:
        draw_const_text(surf, "(имя не должно быть пустым)", round(WIDTH * 0.012), FONT_BUTTON,
                        (surf.get_width() / 2, surf.get_height() / 2 + 0.025 * surf.get_height()), '#F6464B')
    else:
        draw_const_text(surf, "(максимально 12 букв и пробелов)", round(WIDTH * 0.012), FONT_BUTTON,
                        (surf.get_width() / 2, surf.get_height() / 2 + 0.025 * surf.get_height()), '#F6464B')

    if (pygame.time.get_ticks()) % 1000 < 500:
        draw_const_text(surf, " " + statistics_dict["name"] + " ", int(WIDTH * 0.04), FONT_BUTTON, (surf.get_width()/2, surf.get_height() / 2 - 0.08 * surf.get_height()))
    else:
        draw_const_text(surf, " " + statistics_dict["name"] + "|", int(WIDTH * 0.04), FONT_BUTTON,
                        (surf.get_width() / 2, surf.get_height() / 2 - 0.08 * surf.get_height()))
    screen.blit(surf, ((WIDTH - WIDTH / 1.5) / 2, (HEIGHT - HEIGHT / 1.5) / 2))

    surf_circle = pygame.Surface((radius_ball * 2, radius_ball * 2))
    surf_circle.set_alpha(100)
    surf_circle.set_colorkey(BLACK)
    surf_circle.fill(BLACK)
    select_ball = int(settings["select_ball"])
    color_balls = [color_tick]
    color_balls.extend(COLORS)
    i = 0
    for rect_ball in list_rect_balls:
        if select_ball == i:
            surf_circle.set_alpha(255)
            polygon(screen, WHITE, ((rect_ball.x, rect_ball.y + 2.5 * radius_ball),
                                    (rect_ball.x + 2*radius_ball, rect_ball.y + 2.5 * radius_ball)), 3)
        elif rect_ball.collidepoint(mouse):
            surf_circle.set_alpha(255 / 2)
        else:
            surf_circle.set_alpha(255 / 3)
        circle(surf_circle, color_balls[i], (rect_ball.w / 2, rect_ball.w / 2), rect_ball.w / 2)
        i += 1
        screen.blit(surf_circle, rect_ball)

    color_light = '#FED974'
    color_dark = '#FECB42'
    start_color_light = '#35a76e'
    start_color_dark = '#21935a'
    if button_back.collidepoint(mouse):
        draw_button(button_back, "Назад", color_light)
    else:
        draw_button(button_back, "Назад", color_dark)

    if len(statistics_dict["name"]) == 0:
        draw_button(button_start, "Начать игру", '#0B6034')
    else:
        if button_start.collidepoint(mouse):
            draw_button(button_start, "Начать игру", start_color_light)
        else:
            draw_button(button_start, "Начать игру", start_color_dark)


def draw_health():
    text = "♡♡♡♡♡"[:health]
    size_font = round(0.072289 * HEIGHT)
    font_name = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font_name, size_font)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midleft = (0.9458 * WIDTH - text_rect.w, HEIGHT - RECT_FIELD[1] / 2)
    screen.blit(text_surface, text_rect)


def render_game_text():
    global lvl
    global statistics_dict
    size_font = round(0.06024 * HEIGHT)
    draw_const_text(screen, "Очков: " + str(statistics_dict["score"]), size_font, FONT_BUTTON, (WIDTH / 2, RECT_FIELD[1] / 2))
    draw_const_text(screen, "Уровень: " + str(lvl), size_font, FONT_BUTTON, (0.0542 * WIDTH, RECT_FIELD[1] / 2), WHITE, False)
    size_font_1 = int(0.024 * HEIGHT) + 1
    size_font_2 = int(0.018 * HEIGHT) + 1

    size_font = round(0.026 * HEIGHT)

    draw_const_text(screen, "Сложность: " + statistics_dict["diff"], size_font, FONT_BUTTON,
                    (0.0542 * WIDTH, HEIGHT - RECT_FIELD[1] / 3), WHITE, False)

    draw_const_text(screen, "Имя: " + statistics_dict["name"], size_font, FONT_BUTTON,
                    (0.0542 * WIDTH, HEIGHT - 2 * RECT_FIELD[1] / 3), WHITE, False)

    draw_const_text(screen, "Статистика:", size_font_1, FONT_BUTTON,
                    (0.24 * WIDTH, HEIGHT - RECT_FIELD[1] / 2), WHITE, False)
    draw_const_text(screen, "Попаданий: " + str(statistics_dict["hit"]), size_font_2, FONT_BUTTON,
                    (0.33 * WIDTH, HEIGHT - 3 * RECT_FIELD[1] / 4), WHITE, False)
    draw_const_text(screen, "Пропущено: " + str(statistics_dict["loss"]), size_font_2, FONT_BUTTON,
                    (0.33 * WIDTH, HEIGHT - 2 * RECT_FIELD[1] / 4), WHITE, False)
    draw_const_text(screen, "Мимо: " + str(statistics_dict["miss"]), size_font_2, FONT_BUTTON,
                    (0.33 * WIDTH, HEIGHT - 1 * RECT_FIELD[1] / 4), WHITE, False)

    draw_const_text(screen, "Время реакции: ", size_font_1, FONT_BUTTON,
                    (0.44 * WIDTH + 5, HEIGHT - RECT_FIELD[1] / 2), WHITE, False)
    if statistics_dict["time"] == 0:
        aim = 0
    else:
        aim = round(int(statistics_dict["time"]) / int(statistics_dict["hit"]))
    draw_const_text(screen, "Среднее: " + str(aim) +
                    "ms (≈" + str(round(aim/1000, 1)) + "сек)", size_font_2, FONT_BUTTON,
                    (0.56 * WIDTH, HEIGHT - 3 * RECT_FIELD[1] / 4), WHITE, False)
    draw_const_text(screen, "Минимальное: " + str(statistics_dict["min_time"]) +
                    "ms (≈" + str(round(statistics_dict["min_time"]/1000, 1)) + "сек)", size_font_2, FONT_BUTTON,
                    (0.56 * WIDTH, HEIGHT - 2 * RECT_FIELD[1] / 4), WHITE, False)
    draw_const_text(screen, "Максимальное: " + str(statistics_dict["max_time"]) +
                    "ms (≈" + str(round(statistics_dict["max_time"]/1000, 1)) + "сек)", size_font_2, FONT_BUTTON,
                    (0.56 * WIDTH, HEIGHT - 1 * RECT_FIELD[1] / 4), WHITE, False)

    polygon(screen, WHITE, ((0.223 * WIDTH, HEIGHT - RECT_FIELD[1] / 6),
                            (0.223 * WIDTH, HEIGHT - 5 * RECT_FIELD[1] / 6)), 3)

    rect(screen, WHITE, RECT_FIELD, 5)
    draw_health()
    timer()


def render_pre_game_over(button_return, list_index):
    color_light = '#FED974'
    color_dark = '#FECB42'
    mouse = pygame.mouse.get_pos()
    if health <= 0:
        list_str = [
            "А жизни-то закончились...",
            "А сердечек-то не осталось...",
            "Ты убит, пупсик.",
            "Лови больше сердец!",
            "Жизни имеют свойство заканчиваться.",
            "Ты потерял все свои жизни!",
            "Просто повторяй это, раз за разом!",
            "Если долго мучиться, что-нибудь получится!",
            "Попробуй еще раз...",
            "Ничего... Я в тебя верю!",
            "Качай палец!",
            "Засмотрелся на красивые шарики?",
            "Проигрыш - это временная передышка.",
            "Проигрыш - первый шаг к победе!",
        ]
    elif int(statistics_dict["score"]) < 0:
        list_str = [
            "Целься точнее!",
            "Кликай мышкой!",
            "Где тебя учили кликать, дружок?",
            "А когда играть начнёшь?",
            "Тук! Тук!",
            "Ты ушел в минус!",
            "Это вообще возможно?",
            "Ниразу не попал, но зато ты красивый...",
        ]
    if list_index == -1:
        list_index = randint(0, len(list_str)-1)
    draw_const_text(screen, list_str[list_index], round(HEIGHT * 0.07), FONT_BUTTON, (WIDTH / 2, HEIGHT / 2), RED)

    if button_return.collidepoint(mouse):
        draw_button(button_return, "Далее", color_light)
    else:
        draw_button(button_return, "Далее", color_dark)
    render_game_text()
    return list_index


def read_last_game_stat(file):
    last_game_stat = {}
    with open(path.join(data_dir, file), "r", encoding='utf-8') as f:
        for i in f.readlines():
            key, val = i.strip().split(':')
            last_game_stat[key] = val
    return last_game_stat


def write_last_game_stat(file, dict_last_game):
    with open(path.join(data_dir, file), "w", encoding='utf-8') as f:
        for key, val in dict_last_game.items():
            f.write('{}:{}\n'.format(key, val))


def write_file_top_list(file, list_top):
    with open(path.join(data_dir, file), "w", encoding='utf-8') as f:
        if len(list_top) > 10:
            range_list = 10
        else:
            range_list = len(list_top)
        for i in range(range_list):
            for key, val in list_top[i].items():
                f.write('{}:{}\n'.format(key, val))


def write_file_end(file):
    with open(path.join(data_dir, file), "a", encoding='utf-8') as f:
        for key, val in statistics_dict.items():
            f.write('{}:{}\n'.format(key, val))


def render_pause(button_menu, button_restart):
    start_color_light = '#35a76e'
    start_color_dark = '#21935a'
    color_light = '#FED974'
    color_dark = '#FECB42'
    mouse = pygame.mouse.get_pos()
    if button_restart.collidepoint(mouse):
        draw_button(button_restart, "Новая игра", start_color_light)
    else:
        draw_button(button_restart, "Новая игра", start_color_dark)

    if button_menu.collidepoint(mouse):
        draw_button(button_menu, "Главное меню", color_light)
    else:
        draw_button(button_menu, "Главное меню", color_dark)
    render_game_text()
    draw_const_text(screen, "Пауза", round(0.120 * HEIGHT), FONT_BUTTON, (WIDTH / 2, HEIGHT / 3), WHITE)
    draw_const_text(screen, "Нажмите SPACE, что бы продолжить", round(0.023148 * HEIGHT), FONT_BUTTON,
                    (WIDTH / 2, HEIGHT / 2.2), WHITE)


def set_time_heart():
    global timer_start
    sec_20 = (pygame.time.get_ticks() - timer_start - sum_time_pause) // 10000  # какая по счету 10-я секунда
    rand_sec = random.randint(0, 9)  # случайная секунда
    heart_generation_time = (sec_20 + 1) * 10000 + rand_sec * 1000 # генерация случайного появления сердца
    return heart_generation_time


def render_table_statistics(name_table, y, num_lines, list_text, flag_num=False, line_selection=-1):
    size_font = round(0.017 * WIDTH)
    s = pygame.Surface(screen.get_size())
    s.set_colorkey(BLACK)
    s.fill(BLACK)
    draw_const_text(s, name_table, size_font, FONT_BUTTON, (WIDTH / 25, y), WHITE, False)

    table_rect = pygame.Rect(WIDTH / 25, y + size_font, WIDTH - 2 * WIDTH / 25, 0)
    if flag_num:
        indent = round(0.0271 * WIDTH)
    else:
        indent = 0

    table_blit_dict = {}
    color_white_dark = '#D0D0D0'  # серый
    color_white_light = '#D7D7D7'  # светло серый
    color_light_green = '#35a76e'
    color_light_red = '#F6464B'
    table_blit_dict[s] = (0,0,0,0)

    table_header = {
        "date": ["Дата", table_rect.w * 0.12],
        "name": ["Имя", table_rect.w * 0.15],
        "lvl": ["Уровень", table_rect.w * 0.08],
        "score": ["Очков", table_rect.w * 0.08],
        "diff": ["Сложность", table_rect.w * 0.1],
        "duration": ["Время", table_rect.w * 0.08],
        "hit": ["Попад.", table_rect.w * 0.06],
        "loss": ["Пропущ.", table_rect.w * 0.06],
        "miss": ["Мимо", table_rect.w * 0.06],
        "time": ["Сред.", table_rect.w * 0.07],
        "max_time": ["Макс.", table_rect.w * 0.07],
        "min_time": ["Мин.", table_rect.w * 0.07],
    }

    def draw_line(color, x, y, w, h, dict_draw):
        s = pygame.Surface((w, h))
        s.set_alpha(128)
        s.fill(color)
        rect_line = pygame.Rect(x, y, 0, 0)
        dict_draw[s] = rect_line

    def draw_num_lines(i, x, y, dict_draw):
        font_name = pygame.font.match_font(FONT_BUTTON)
        font = pygame.font.Font(font_name, round(0.012 * WIDTH))
        surf = (font.render(str(i + 1), True, color_white_light))
        text_rect = surf.get_rect()
        text_rect.center = (x, y)
        dict_draw[surf] = text_rect

    font_name = pygame.font.match_font(FONT_BUTTON)
    font = pygame.font.Font(font_name, round(0.010 * WIDTH))
    surf = (font.render(table_header["date"][0], True, color_white_light))
    text_rect = surf.get_rect()

    draw_line('#606060', table_rect.x - indent, table_rect.y, table_rect.w + indent, text_rect.h, table_blit_dict)

    coord_x_text = table_rect.x
    for key, val in table_header.items():
        font_name = pygame.font.match_font(FONT_BUTTON)
        font = pygame.font.Font(font_name, round(0.010 * WIDTH))
        surf = (font.render(val[0], True, color_white_light))
        text_rect = surf.get_rect()
        text_rect.midtop = (val[1] / 2, table_rect.y)
        text_rect.x += coord_x_text
        table_blit_dict[surf] = text_rect
        coord_x_text += val[1]

    coord_y_lines = table_rect.y + 2 * text_rect.h
    if len(list_text) > num_lines:
        len_list = num_lines
    else:
        len_list = len(list_text)

    for i in range(num_lines):
        if line_selection == i:
            draw_line('#BFA255', table_rect.x - indent, coord_y_lines - text_rect.h, table_rect.w + indent,
                      2 * text_rect.h, table_blit_dict)
        elif (i%2 == 0):
            draw_line('#363636', table_rect.x - indent, coord_y_lines-text_rect.h, table_rect.w + indent, 2*text_rect.h, table_blit_dict)
        else:
            draw_line('#484848', table_rect.x - indent, coord_y_lines - text_rect.h, table_rect.w + indent, 2 * text_rect.h, table_blit_dict)
        if flag_num:
            draw_num_lines(i, table_rect.x - indent/2, coord_y_lines, table_blit_dict)
        coord_y_lines += text_rect.h + text_rect.h
    coord_y_text = table_rect.y + text_rect.h
    for i in range(len_list):
        coord_x_text = table_rect.x
        for key, val in table_header.items():
            font_name = pygame.font.match_font("segoeuisemilight")
            font = pygame.font.Font(font_name, round(0.010 * WIDTH))
            color = color_white_dark
            text = str(list_text[i][key])
            if key == "duration":
                time_int = int(list_text[i]["duration"])
                minute = int(time_int / 1000 // 60)
                second = int(time_int / 1000 % 60)
                text = (str(minute).zfill(2) + ":" + str(second).zfill(2))
            elif key == "name":
                color = WHITE
            elif key == "date":
                color = '#D0D0D0'
                date_time = datetime.fromtimestamp(float(list_text[i]["date"]))
                text = date_time.strftime("%d.%m.%Y    %H:%M")
            elif key == "loss":
                color = color_light_red

            elif key == "hit":
                color = color_light_green
            elif key == "score":
                color = color_light_green
            elif key == "time" or key == "min_time" or key == "max_time":
                if key == "time":
                    color = color_light_green
                text += "ms"
            surf = font.render(text, True, color)
            text_rect = surf.get_rect()
            text_rect.center = (val[1] / 2, coord_y_text + text_rect.h)
            text_rect.x += coord_x_text
            table_blit_dict[surf] = text_rect
            coord_x_text += val[1]
        coord_y_text += 2 * text_rect.h
    return table_blit_dict


def draw_statistics(dict_draw):
    for surf, text_rect in dict_draw.items():
        screen.blit(surf, text_rect)


def check_entry_dict_in_list(dict_stat, list_stat):
    for i in range(len(list_stat)):
        if int(list_stat[i]["num_game"]) == int(dict_stat["num_game"]):
            return i
    return -1


def render_statistics(list_table_render, button_back, button_all, button_top_norm, button_top_hard):
    button_stat_color_dark = '#363636'
    button_stat_color_light = '#484848'
    button_stat_color_super_light = '#606060'

    statistics_color_light = '#FED974'
    statistics_color_dark = '#FECB42'

    draw_const_text(screen, "Статистика", round(0.05 * WIDTH), FONT_BUTTON, (WIDTH/2, HEIGHT/18), statistics_color_dark)
    if stat_all:
        all_page = len(all_game_list) // 10
        if len(all_game_list) % 10 > 0:
            all_page += 1

    for dict_table in list_table_render:
        draw_statistics(dict_table)

    mouse = pygame.mouse.get_pos()

    def draw_button_stat(button_rect, text, color):
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
        rect(screen, color, button_rect, 0)
        draw_const_text(screen, text, int(button_rect.height * 0.5),
                        FONT_BUTTON, (button_rect.centerx, button_rect.centery - 3))

    def draw_button_page(button_rect, text, color):
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
        rect(screen, color, button_rect, 0)
        draw_const_text(screen, text, int(button_rect.height * 1),
                        FONT_BUTTON, (button_rect.centerx, button_rect.centery - 9))

    if button_back.collidepoint(mouse):
        draw_button(button_back, "Назад", statistics_color_light)
    else:
        draw_button(button_back, "Назад", statistics_color_dark)
    if stat_all:
        draw_button_stat(button_all, "Все тренировки", button_stat_color_dark)
    elif button_all.collidepoint(mouse):
        draw_button_stat(button_all, "Все тренировки",  button_stat_color_super_light)
    else:
        draw_button_stat(button_all, "Все тренировки", button_stat_color_light)

    if stat_all:
        if page <= 0:
            draw_button_page(button_stat_all_back, "←", button_stat_color_dark)
        elif button_stat_all_back.collidepoint(mouse):
            draw_button_page(button_stat_all_back, "←", button_stat_color_super_light)
        else:
            draw_button_page(button_stat_all_back, "←", button_stat_color_light)
        if page == all_page - 1:
            draw_button_page(button_stat_all_next, "→", button_stat_color_dark)
        elif button_stat_all_next.collidepoint(mouse):
            draw_button_page(button_stat_all_next, "→", button_stat_color_super_light)
        else:
            draw_button_page(button_stat_all_next, "→", button_stat_color_light)

    if stat_norm:
        draw_button_stat(button_top_norm, "Топ 10 (Стандарт)", button_stat_color_dark)
    elif button_top_norm.collidepoint(mouse):
        draw_button_stat(button_top_norm, "Топ 10 (Стандарт)",  button_stat_color_super_light)
    else:
        draw_button_stat(button_top_norm, "Топ 10 (Стандарт)", button_stat_color_light)

    if stat_hard:
        draw_button_stat(button_top_hard, "Топ 10 (Мастер)", button_stat_color_dark)
    elif button_top_hard.collidepoint(mouse):
        draw_button_stat(button_top_hard, "Топ 10 (Мастер)",  button_stat_color_super_light)
    else:
        draw_button_stat(button_top_hard, "Топ 10 (Мастер)", button_stat_color_light)


def read_list_game(file):
    list_game = []
    line_dict = {}
    with open(path.join(data_dir, file), "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) != 0:
                key, val = line.split(':')
                if key == "num_game":
                    val = int(val)
                elif val == "True":
                    val = True
                elif val == "False":
                    val = False
                line_dict[key] = val
                if key == "lvl":
                    if len(line_dict) == 13:
                        list_game.append(line_dict)
                        line_dict = {}
                    else:
                        line_dict = {}
    return list_game


def read_settings():
    global settings
    with open("settings.txt", "r") as f:
        for i in f.readlines():
            i = i.strip()
            if len(i) != 0:
                key, val = i.split(':')
                if key == "num_game":
                    val = int(val)
                elif val == "True":
                    val = True
                elif val == "False":
                    val = False

                settings[key] = val


def write_settings():
    global settings
    with open("settings.txt", "w") as f:
        for key, val in settings.items():
            f.write('{}:{}\n'.format(key, val))


def set_new_game():
    global health
    global statistics_dict
    global last_game_stat_norm
    global last_game_stat_hard
    global timer_start
    global time_pause
    global sum_time_pause
    global lvl
    global shape
    global text
    global time_heart
    health = 5
    last_game_stat = {}
    if len(last_game_stat_hard) != 0 and len(last_game_stat_norm) != 0:
        if int(last_game_stat_norm["num_game"]) > int(last_game_stat_hard["num_game"]):
            last_game_stat = last_game_stat_norm
        else:
            last_game_stat = last_game_stat_hard
    elif len(last_game_stat_hard) != 0 and len(last_game_stat_norm) == 0:
        last_game_stat = last_game_stat_hard
    elif len(last_game_stat_hard) == 0 and len(last_game_stat_norm) != 0:
        last_game_stat = last_game_stat_norm


    if len(statistics_dict) == 0:
        if len(last_game_stat) == 0:
            name = ""
            diff = "Стандарт"
            num_game = 1
        else:
            name = last_game_stat["name"]
            diff = last_game_stat["diff"]
            num_game = settings["num_game"]
    else:
        name = statistics_dict["name"]
        if difficulty_master:
            diff = "Мастер"
        else:
            diff = "Стандарт"
        num_game = settings["num_game"]

    statistics_dict = {
        "date": time.time(),
        "duration": 0,
        "num_game": num_game,
        "name": name,
        "diff": diff,
        "score": 0,
        "hit": 0,
        "loss": 0,
        "miss": 0,
        "time": 0,
        "min_time": 0,
        "max_time": 0,
    }
    shape = {'Balls': [],
             'Heart': []}
    time_heart = 10000
    time_pause = 0
    sum_time_pause = 0
    lvl = 1
    text = []


last_game_stat_norm = read_last_game_stat("last_game_norm.txt")
last_game_stat_hard = read_last_game_stat("last_game_hard.txt")

statistics_dict = {}
top_norm_list = read_list_game("top_norm.txt")
top_hard_list = read_list_game("top_hard.txt")
all_game_list = read_list_game("all_game.txt")

render_statistics_list = []

RECT_FIELD = (0, 0, 0, 0)

health = 5

timer_start = 0
time_heart = 0  # рандомное время появления сердец
time_pause = 0  # время конкретной паузы
sum_time_pause = 0  # сумма всех промежутков пауз

difficulty_master = False  # сложность

balls_in_menu = []
start_menu = True
input_name = False
start_game = False
game = False
pre_game_over = False
game_over = False
finished = False
statistics = False
about_game = False
pause = False
stat_all = True
stat_norm = False
stat_hard = False
rect_egg = pygame.Rect(0,0,0,0)
click_egg = 0

settings = {}


shape = {'Balls': [],
         'Heart': []}
lvl = 1
text = []

read_settings()
screen = pygame.display.set_mode(SIZE_DEFAULT)
if settings['fullscreen']:
    set_fullscreen()

set_new_game()
time_balls_in_name_tick = pygame.time.get_ticks()
color_tick = COLORS[randint(0, len(COLORS) - 1)]
page = 0
firework = []

while not finished:
    SIZE = WIDTH, HEIGHT = screen.get_size()
    clock.tick(FPS)
    screen.fill(BLACK)
    if game:
        check_score()
    if start_menu:
        num_balls_in_menu = set_lvl(40)
        if len(balls_in_menu) == 0:
            for i in range(num_balls_in_menu):
                balls_in_menu.append(new_ball())
        for i in range(num_balls_in_menu):
            if difficulty_master:
                move_ball(balls_in_menu[i])
            draw_ball(balls_in_menu[i])
            modification_bal(balls_in_menu[i])

        width_button = round(0.463 * HEIGHT)
        height_button = round(0.0926 * HEIGHT)
        button_start_rect = pygame.Rect(WIDTH/2, HEIGHT/2 - height_button/2, width_button, height_button)
        button_statistics_rect = pygame.Rect(WIDTH / 2, button_start_rect.y + height_button*1.9, width_button,  height_button)
        button_exit_rect = pygame.Rect(WIDTH / 2, button_start_rect.y + height_button*3, width_button,
                                       height_button)
        button_statistics_rect.midtop = (button_statistics_rect.x, button_statistics_rect.y)
        button_start_rect.midtop = (button_start_rect.x, button_start_rect.y)
        button_exit_rect.midtop = (button_exit_rect.x, button_exit_rect.y)

        draw_const_text(screen, "Сложность:", round(0.02777 * HEIGHT), FONT_BUTTON, (button_start_rect.centerx,
                                                                button_start_rect.centery + height_button * 0.7))
        font = pygame.font.match_font(FONT_BUTTON)
        font = pygame.font.Font(font, round(0.02777 * HEIGHT))
        text_menu = font.render('Стандарт', True, '#D7D7D7')
        button_standard = pygame.Rect(text_menu.get_rect())
        button_standard.midtop = (WIDTH/2 - button_start_rect.w/5, button_start_rect.centery + height_button * 0.85)
        text_menu = font.render('Мастер', True, '#848484')
        button_master = pygame.Rect(text_menu.get_rect())
        button_master.midtop = (WIDTH/2 + button_start_rect.w/5, button_start_rect.centery + height_button * 0.85)

        font = pygame.font.match_font(FONT_BUTTON)
        font = pygame.font.Font(font, 25)
        text_menu = font.render('На весь экран (F)', True, '#D7D7D7')
        button_fullscreen = pygame.Rect(text_menu.get_rect())
        button_fullscreen.midtop = (WIDTH-button_fullscreen.w/2 - 10, HEIGHT - button_fullscreen.h - 10)
        text_menu = font.render('В окне (F)', True, '#848484')
        button_window = pygame.Rect(text_menu.get_rect())
        button_window.midtop = (WIDTH - button_window.w/2 - 10, HEIGHT - button_window.h - 10)

        text_menu = font.render('Об игре (I)', True, '#D7D7D7')
        button_info = pygame.Rect(text_menu.get_rect())
        button_info.midtop = (button_info.w / 2 + 10, HEIGHT - button_window.h - 10)

        render_start(button_start_rect, button_exit_rect, button_statistics_rect, button_standard, button_master, button_fullscreen, button_window, button_info)
    if about_game:
        button_about_game = pygame.Rect(WIDTH / 2 - 0.237127 * WIDTH / 2, HEIGHT / 2 + 0.2048 * HEIGHT, 0.237127 * WIDTH,
                                        0.237127 * WIDTH / 5)
        render_about_game(button_about_game)
        rect_egg.x += (WIDTH - WIDTH / 1.5) / 2
        rect_egg.y += (HEIGHT - HEIGHT / 1.5) / 2
    if input_name:
        button_back_in_name = pygame.Rect(WIDTH / 3 - 0.237127 * WIDTH / 2, HEIGHT / 2 + 0.2048 * HEIGHT, 0.237127 * WIDTH,
                                        0.237127 * WIDTH / 5)

        button_start_in_name = pygame.Rect(2 * WIDTH / 3 - 0.237127 * WIDTH / 2, HEIGHT / 2 + 0.2048 * HEIGHT,
                                        0.237127 * WIDTH,
                                        0.237127 * WIDTH / 5)

        radius_ball = round(0.0370 * HEIGHT)
        coord_x = (WIDTH - 23 * radius_ball) / 2
        coord_y = 4 * HEIGHT / 7
        list_button_balls = []
        for color in range(len(COLORS) + 1):
            list_button_balls.append(pygame.Rect(coord_x, coord_y, radius_ball * 2, radius_ball * 2))
            coord_x += 3 * radius_ball

        if (pygame.time.get_ticks() - time_balls_in_name_tick) % 1600 < 800 or len(color_tick) == 0:
            time_balls_in_name_tick += 800 + (pygame.time.get_ticks() - time_balls_in_name_tick) % 1600
            color_1 = color_tick
            color_tick = COLORS[randint(0, len(COLORS) - 1)]
            if color_1 == color_tick:
                color_tick = COLORS[randint(0, len(COLORS) - 1)]
        else:
            color_tick = color_tick
        render_input_name(button_back_in_name, button_start_in_name, list_button_balls, color_tick)
    if statistics:
        for i in range(num_balls_in_menu):
            move_ball(balls_in_menu[i])
            draw_ball(balls_in_menu[i])
            modification_bal(balls_in_menu[i])
        if len(render_statistics_list) == 0:
            if stat_all:
                all_page = len(all_game_list) // 10
                if len(all_game_list) % 10 > 0:
                    all_page += 1
                if page >= all_page:
                    page = all_page - 1
                a = -1 - (10 * page)
                b = -11 - (10 * page)
                render_statistics_list.append(render_table_statistics("Страница " + str(page + 1) + " из " + str(all_page), 3.8 * HEIGHT / 20, 10,
                                        all_game_list[a:b:-1], False))

            elif stat_norm:
                k = check_entry_dict_in_list(last_game_stat_norm, top_norm_list)
                render_statistics_list.append(render_table_statistics("Топ 10 (Стандарт)", 6.6 * HEIGHT / 20, 10, top_norm_list, True, k))

                if k > 0:
                    k = 0
                if len(last_game_stat_norm) == 0:
                    render_statistics_list.append(
                        render_table_statistics("Последняя тренировка", 3.8 * HEIGHT / 20, 1, [], False, k))
                else:
                    render_statistics_list.append(
                        render_table_statistics("Последняя тренировка", 3.8 * HEIGHT / 20, 1, [last_game_stat_norm],
                                                False, k))

            elif stat_hard:
                k = check_entry_dict_in_list(last_game_stat_hard, top_hard_list)
                render_statistics_list.append(render_table_statistics("Топ 10 (Мастер)", 6.6 * HEIGHT / 20, 10, top_hard_list, True, k))
                if k > 0:
                    k = 0
                if len(last_game_stat_hard) == 0:
                    render_statistics_list.append(
                        render_table_statistics("Последняя тренировка", 3.8 * HEIGHT / 20, 1, [], False, k))
                else:
                    render_statistics_list.append(
                        render_table_statistics("Последняя тренировка", 3.8 * HEIGHT / 20, 1, [last_game_stat_hard],
                                                False, k))

        button_back_statistics = pygame.Rect(WIDTH / 2, 17.8 * HEIGHT / 20, 0.237127 * WIDTH, 0.237127 * WIDTH / 5)
        button_back_statistics.midtop = (button_back_statistics.x, button_back_statistics.y)

        button_all_statistics = pygame.Rect(WIDTH/2 - 1.5*(0.12 * WIDTH), HEIGHT / 8, 0.12 * WIDTH, 0.12 * WIDTH / 5)
        button_top_norm_statistics = pygame.Rect(button_all_statistics.x + button_all_statistics.w, button_all_statistics.y, 0.12 * WIDTH, 0.12 * WIDTH / 5)
        button_top_hard_statistics = pygame.Rect(button_top_norm_statistics.x + button_top_norm_statistics.w, button_all_statistics.y, 0.12 * WIDTH, 0.12 * WIDTH / 5)
        if stat_all:
            button_stat_all_next = pygame.Rect(WIDTH / 2, 15.2 * HEIGHT / 20, 0.09 * WIDTH, 0.05 * WIDTH)
            button_stat_all_back = pygame.Rect(WIDTH / 2 - button_stat_all_next.w, 15.2 * HEIGHT / 20, 0.09 * WIDTH, 0.05 * WIDTH)
        render_statistics(render_statistics_list, button_back_statistics, button_all_statistics, button_top_norm_statistics, button_top_hard_statistics)
    if pre_game_over:
        for i in range(len(shape["Balls"])):
            draw_ball(shape["Balls"][i])
        draw_heart(shape["Heart"])
        for i in range(len(text)):
            draw_text(screen, *text[i][0])
        button_per_end_return = pygame.Rect(WIDTH / 2 - 0.237127 * WIDTH / 2,3*HEIGHT /5,
                                              0.237127 * WIDTH,
                                              0.237127 * WIDTH / 5)
        index_text_pre_game_over = render_pre_game_over(button_per_end_return, index_text_pre_game_over )
    if game_over:
        num_balls_in_menu = set_lvl(lvl)
        if len(balls_in_menu) == 0:
            for i in range(num_balls_in_menu):
                balls_in_menu.append(new_ball())
        for i in range(num_balls_in_menu):
            move_ball(balls_in_menu[i])
            draw_ball(balls_in_menu[i])
            modification_bal(balls_in_menu[i])

        button_menu_game_over = pygame.Rect(2*WIDTH / 3, 17.8 * HEIGHT / 20, 0.237127 * WIDTH, 0.237127 * WIDTH / 5)
        button_menu_game_over.midtop = (button_menu_game_over.x, button_menu_game_over.y)

        button_new_game_over = pygame.Rect(WIDTH / 3, 17.8 * HEIGHT / 20, 0.237127 * WIDTH, 0.237127 * WIDTH / 5)
        button_new_game_over.midtop = (button_new_game_over.x, button_new_game_over.y)

        if len(render_statistics_list) == 0:
            if not difficulty_master:
                k = check_entry_dict_in_list(last_game_stat_norm, top_norm_list)
                render_statistics_list.append(render_table_statistics("Топ 10 (Стандарт)", 6.4 * HEIGHT / 20, 10, top_norm_list, True, k))
                if k > 0:
                    line = 0
                if len(last_game_stat_norm) == 0:
                    render_statistics_list.append(
                        render_table_statistics("Тренировка", 3.2 * HEIGHT / 20, 1, [], False, line))
                else:
                    render_statistics_list.append(
                        render_table_statistics("Тренировка", 3.2 * HEIGHT / 20, 1, [last_game_stat_norm],
                                                False, line))
            else:
                k = check_entry_dict_in_list(last_game_stat_hard, top_hard_list)
                render_statistics_list.append(render_table_statistics("Топ 10 (Мастер)", 6.4 * HEIGHT / 20, 10, top_hard_list, True, k))
                if k > 0:
                    line = 0
                if len(last_game_stat_hard) == 0:
                    render_statistics_list.append(
                        render_table_statistics("Тренировка", 3.2 * HEIGHT / 20, 1, [], False, line))
                else:
                    render_statistics_list.append(
                        render_table_statistics("Тренировка", 3.2 * HEIGHT / 20, 1, [last_game_stat_hard],
                                                False, line))
            s = pygame.Surface(screen.get_size())
            s.set_colorkey(BLACK)
            s.fill(BLACK)


            if k == 0:
                sound_new_record.play()
                draw_const_text(s, "Новый рекорд!", round(0.05 * WIDTH), FONT_BUTTON, (WIDTH / 2, HEIGHT / 15),
                                GREEN)
            elif 0 < k < 5:
                sound_record.play()
                draw_const_text(s, "Неплохо, ты в ТОП 5!", round(0.05 * WIDTH), FONT_BUTTON,
                                (WIDTH / 2, HEIGHT / 15),
                                ORANGE)
            elif 5 <= k < 10:
                sound_record.play()
                draw_const_text(s, "Неплохо, ты в ТОП 10!", round(0.05 * WIDTH), FONT_BUTTON,
                                (WIDTH / 2, HEIGHT / 15),
                                ORANGE)
            else:
                draw_const_text(s, "Тренируйся лучше!", round(0.05 * WIDTH), FONT_BUTTON, (WIDTH / 2, HEIGHT / 15),
                                RED)
            render_statistics_list.append({s: (0, 0, 0, 0)})
        if k == 0:
            time_chek = 5
        elif 0 < k < 10:
            time_chek = 3
        else:
            time_chek = 0
        if (pygame.time.get_ticks() - time_music_menu) / 1000 > time_chek:
            music_menu.set_volume(0.3)
        render_game_over(button_menu_game_over, button_new_game_over)
    for event in pygame.event.get():
        if input_name:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if len(statistics_dict['name']) < 12:
                        sound_button_seal.play()
                        statistics_dict['name'] += event.unicode
                    else:
                        sound_name_end.play()
                elif event.key == pygame.K_BACKSPACE:
                    if len(statistics_dict["name"]) == 0:
                        sound_name_end.play()
                    else:
                        sound_button_space.play()
                    statistics_dict['name'] = statistics_dict['name'][:-1]
                elif event.key == pygame.K_SPACE:
                    sound_button_seal.play()
                    statistics_dict['name'] += "_"
                elif event.key == pygame.K_RETURN and len(statistics_dict["name"]) > 0:
                    music_menu.set_volume(0.1)
                    sound_button.play()
                    timer_start = pygame.time.get_ticks()
                    start_game = True
                    input_name = False
                    start_menu = False
                elif event.key == pygame.K_ESCAPE:
                    sound_button.play()
                    input_name = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_ball in list_button_balls:
                    if check_push_button(button_ball):
                        settings["select_ball"] = list_button_balls.index(button_ball)
                if check_push_button(button_back_in_name):
                    input_name = False
                if len(statistics_dict["name"]) > 0:
                    if check_push_button(button_start_in_name):
                        music_menu.set_volume(0.1)
                        timer_start = pygame.time.get_ticks()
                        start_game = True
                        input_name = False
                        start_menu = False
        elif start_menu and not about_game and not input_name:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_push_button(button_start_rect):
                    set_new_game()
                    input_name = True
                if check_push_button(button_statistics_rect):
                    page = 0
                    start_menu = False
                    statistics = True
                if check_push_button(button_exit_rect):
                    start_menu = False
                    finished = True
                if not difficulty_master:
                    if check_push_button(button_master):
                        difficulty_master = True
                else:
                     if check_push_button(button_standard):
                        difficulty_master = False
                if check_push_button(button_window) and settings['fullscreen']:
                    settings['fullscreen'] = not settings['fullscreen']
                    write_settings()
                    set_fullscreen()
                    balls_in_menu = []
                elif check_push_button(button_fullscreen) and not settings['fullscreen']:
                    settings['fullscreen'] = not settings['fullscreen']
                    write_settings()
                    set_fullscreen()
                    balls_in_menu = []
                if check_push_button(button_info):
                    about_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    sound_button.play()
                    about_game = not about_game
                if event.key == pygame.K_f:
                    sound_button.play()
                    if start_menu:
                        balls_in_menu = []
                    settings['fullscreen'] = not settings['fullscreen']
                    write_settings()
                    if settings['fullscreen']:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        pygame.display.toggle_fullscreen()
                        screen = pygame.display.set_mode(SIZE_DEFAULT, pygame.DOUBLEBUF)
                if event.key == pygame.K_RETURN:
                    sound_button.play()
                    set_new_game()
                    input_name = True
        elif pre_game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_push_button(button_per_end_return):
                    time_music_menu = pygame.time.get_ticks()
                    pre_game_over = False
                    game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    time_music_menu = pygame.time.get_ticks()
                    sound_button.play()
                    pre_game_over = False
                    game_over = True
        elif game_over:
            RECT_FIELD = (0, 0, 0, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_push_button(button_menu_game_over):
                    render_statistics_list = []
                    balls_in_menu = []
                    game_over = False
                    start_menu = True
                    set_new_game()
                if check_push_button(button_new_game_over):
                    music_menu.set_volume(0.1)
                    render_statistics_list = []
                    game_over = False
                    start_game = True
                    set_new_game()
                    timer_start = pygame.time.get_ticks()
        elif statistics:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if stat_all:
                    if page != all_page - 1:
                        if check_push_button(button_stat_all_next):
                            page += 1
                            render_statistics_list = []
                    if page > 0:
                        if check_push_button(button_stat_all_back):
                            if page > 0:
                                page -= 1
                            render_statistics_list = []

                if check_push_button(button_back_statistics):
                    render_statistics_list = []
                    stat_norm = stat_hard = False
                    stat_all = True
                    statistics = not statistics
                    start_menu = not start_menu
                if check_push_button(button_all_statistics) and not stat_all:
                    page = 0
                    stat_all = True
                    stat_norm = False
                    stat_hard = False
                    render_statistics_list = []
                elif check_push_button(button_top_norm_statistics) and not stat_norm:
                    stat_all = False
                    stat_norm = True
                    stat_hard = False
                    render_statistics_list = []
                elif check_push_button(button_top_hard_statistics) and not stat_hard:
                    stat_all = False
                    stat_norm = False
                    stat_hard = True
                    render_statistics_list = []

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound_button.play()
                    stat_norm = stat_hard = False
                    stat_all = True
                    statistics = not statistics
                    start_menu = not start_menu
        elif game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(shape["Balls"], shape["Heart"], text)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    sound_button.play()
                    game = not game
                    pause = not pause
                    time_pause = pygame.time.get_ticks()
        elif pause:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    sound_button.play()
                    game = not game
                    pause = not pause
                    sum_time_pause += pygame.time.get_ticks() - time_pause
                    for i in range(len(shape["Balls"])):
                        shape["Balls"][i]['start_life'] += pygame.time.get_ticks() - time_pause
                    for i in range(len(shape["Heart"])):
                        shape["Heart"][i]['time'] += pygame.time.get_ticks() - time_pause
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_push_button(button_menu_in_pause):
                    music_menu.set_volume(0.3)
                    set_new_game()
                    start_menu = True
                    pause = False
                    game = False
                if check_push_button(button_restart_in_pause):
                    timer_start = pygame.time.get_ticks()
                    pause = False
                    start_game = True
                    set_new_game()
        elif about_game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_push_button(button_about_game):
                    about_game = False
                    click_egg = 0
                if check_push_button(rect_egg):
                    if click_egg == 13:
                        click_egg = 0
                        webbrowser.open_new_tab('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                    else:
                        webbrowser.open_new_tab('https://github.com/satisataka')
                        click_egg += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    click_egg = 0
                    sound_button.play()
                    about_game = not about_game

        if event.type == pygame.QUIT:
            finished = True
    if start_game:
        RECT_FIELD = (WIDTH * 0.02, HEIGHT / 10, WIDTH - 2 * (WIDTH * 0.02), HEIGHT - 2 * (HEIGHT / 10))
        time_start = (pygame.time.get_ticks() - timer_start) / 1000
        render_game_text()
        if time_start > 3:
            timer_start = pygame.time.get_ticks()
            game = True
            start_game = False
            set_new_game()
        else:
            time_start = 3 - round(time_start)
            if time_start == 0:
                draw_const_text(screen, "Старт!", round(0.2 * HEIGHT), FONT_BUTTON, (WIDTH / 2, HEIGHT / 2.2), WHITE)
            else:
                draw_const_text(screen, str(time_start), round(0.2 * HEIGHT), FONT_BUTTON, (WIDTH / 2, HEIGHT / 2.2), WHITE)
            draw_const_text(screen, "Подсказка: Нажмите ESC или SPACE для паузы", round(0.025 * HEIGHT), FONT_BUTTON, (WIDTH / 2, HEIGHT / 1.5), '#21935a')

    if pause:
        mouse = pygame.mouse.get_pos()
        button_menu_in_pause = pygame.Rect(WIDTH / 2 - 0.237127 * WIDTH / 2, HEIGHT / 2.5 + 0.2048 * HEIGHT,
                                        0.237127 * WIDTH,
                                        0.237127 * WIDTH / 5)
        button_restart_in_pause = pygame.Rect(WIDTH / 2 - 0.237127 * WIDTH / 2, HEIGHT / 3.5 + 0.2048 * HEIGHT,
                             0.237127 * WIDTH,
                             0.237127 * WIDTH / 5)
        render_pause(button_menu_in_pause, button_restart_in_pause)

    if game:
        RECT_FIELD = (WIDTH * 0.02, HEIGHT / 10, WIDTH - 2 * (WIDTH * 0.02), HEIGHT - 2 * (HEIGHT / 10))

        num_balls = set_lvl(lvl)

        new_list = []
        for i in range(len(text)):
            seconds = (pygame.time.get_ticks() - text[i][1]) / 1000
            if seconds < 1:
                draw_text(screen, *text[i][0])
                new_list.append(text[i])
        text = new_list

        if num_balls != len(shape["Balls"]):
            text.append((("Уровень: " + str(lvl), 100, (WIDTH / 2, HEIGHT / 2)), pygame.time.get_ticks(), WHITE))
            for i in range(num_balls - len(shape["Balls"])):
                shape["Balls"].append(new_ball())

        check_figure_timer(shape["Balls"], text)
        for i in range(len(shape["Balls"])):
            modification_bal(shape["Balls"][i])
            if difficulty_master:
                move_ball(shape["Balls"][i])
            draw_ball(shape["Balls"][i])

        if pygame.time.get_ticks() - timer_start - sum_time_pause > time_heart:
            time_heart = set_time_heart()
            shape["Heart"].append(heart())
        check_time_heart(shape["Heart"])
        draw_heart(shape["Heart"])
        for i in range(len(shape["Heart"])):
            move_heart(shape["Heart"][i])
        render_game_text()

    pygame.display.update()
pygame.quit()
