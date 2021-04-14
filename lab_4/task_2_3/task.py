"""
Выполнены все задания lab_4, а так же рефакторинг lab_5
"""

import numpy as np
import random
import pygame
from pygame.draw import *

# константы
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


def main():
    display_width = 800
    display_height = 1000
    screen = pygame.display.set_mode((display_width, display_height))

    # фон
    bg = [
            ([800, 500], [33, 33, 120], 0, 0),
            ([800, 50], [150, 100, 200, 200], 0, 100),
            ([800, 100], [200, 100, 200, 210], 0, 150),
            ([800, 150], [220, 135, 170, 220], 0, 250),
            ([800, 100], [255, 155, 85, 230], 0, 400),
            ([800, 500], [0, 102, 128, 255], 0, 500),
         ]
    for i in range(len(bg)):
        draw_background(screen, *bg[i])

    # рыбы
    fish_length = 200
    fish_coord = [
        (100, 950, True),
        (500, 900),
        (580, 750),
    ]
    for coord in fish_coord:
        draw_fish(screen, fish_length, *coord)

    # чайки в рандомных местах, выше моря
    for i in range(12):
        gull_length = 80
        draw_gull(screen, WHITE, random.randint(0, display_width - gull_length), random.randint(0, 350), gull_length, 1)
    for i in range(4):
        gull_length = 150
        draw_gull(screen, WHITE, random.randint(0, display_width - gull_length), random.randint(0, 350), gull_length, 2)
    for i in range(3):
        gull_length = 200
        draw_gull(screen, WHITE, random.randint(0, display_width - gull_length), random.randint(0, 350), gull_length, 3)

    # большие птицы
    draw_bird(screen, 555, 0, 550)
    draw_bird(screen, 200, 550, 550, True)
    draw_bird(screen, 150, 350, 500)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
    pygame.quit()


def draw_bird(surface, bird_length, x, y, x_bool=False):
    """
    Функция рисует птицу
    :param surface: объект pygame.Surface
    :param bird_length: ширина объекта
    :param x: координаты верхнего левого угла объекта
    :param y: координаты верхнего левого угла объекта
    :param x_bool: отразить по горизонтали
    :return:
    """
    def draw_wing() -> pygame.Surface:
        """
        Функция рисует крыло птицы
        :return: pygame.Surface
        """
        surf = pygame.Surface((330, 200))
        surf.fill(GREEN)
        surf.set_colorkey(GREEN)

        mntn = [[255, 200]]

        mntn_1 = []
        for i in range(31, 255):
            a = 130 + (i - 140) ** 3/20000
            mntn_1.append([i, a])
        mntn_1.reverse()
        mntn.extend(mntn_1)

        for i in range(31, 100):
            a = 40 + 10 * ((650 / i) ** 3) / 5000
            mntn.append([i, a])

        for i in range(105, 280):
            a = 80 - (i - 280) ** 2 / 800
            mntn.append([i, a])

        for i in range(280, 330):
            a = 80 + (i - 280) ** 3/1000
            mntn.append([i, a])

        polygon(surf, WHITE, mntn, 0)
        polygon(surf, BLACK, mntn, 1)
        return surf

    def draw_body() -> pygame.Surface:
        """
        Функция рисует тело птицы
        :return: pygame.Surface
        """
        surf = pygame.Surface((340, 200))
        surf.fill(GREEN)
        surf.set_colorkey(GREEN)

        ellipse(surf, WHITE, ((0, 35), (220, 100)), 0)
        ellipse(surf, WHITE, ((190, 50), (100, 40)), 0)
        ellipse(surf, WHITE, ((260, 20), (80, 50)), 0)
        ellipse(surf, BLACK, ((310, 35), (15, 10)), 0)

        return surf

    def draw_beak() -> pygame.Surface:
        """
        Функция рисует клюв птицы
        :return: pygame.Surface
        """
        surf = pygame.Surface((50, 40))
        surf.fill(GREEN)
        surf.set_colorkey(GREEN)

        polygon(surf, (225, 221, 85), ([0, 10], [40, 15], [30, 15], [50, 10], [40, 30], [0, 25]), 0)
        polygon(surf, BLACK, ([0, 10], [40, 15], [30, 15], [50, 10], [40, 30], [0, 25]), 1)
        polygon(surf, (225, 221, 85), ([0, 10], [40, 0], [50, 10], [40, 15], [30, 15]), 0)
        polygon(surf, BLACK, ([0, 10], [40, 0], [50, 10], [40, 15], [30, 15]), 1)
        return surf

    def draw_feet() -> pygame.Surface:
        """
        Функция рисует ноги птицы
        :return: pygame.Surface
        """
        surf = pygame.Surface((150, 100))
        surf.fill(GREEN)
        surf.set_colorkey(GREEN)

        surf_feet = pygame.Surface((340, 400))
        surf_feet.fill(GREEN)
        surf_feet.set_colorkey(GREEN)

        ellipse(surf, WHITE, ((0, 0), (100, 50)), 0)
        surf = pygame.transform.rotate(surf, 120)
        surf_feet.blit(surf, (0, 0))

        surf.fill(GREEN)
        ellipse(surf, WHITE, ((0, 0), (110, 30)), 0)
        surf = pygame.transform.rotate(surf, -20)
        surf_feet.blit(surf, (10, 140))

        surf = pygame.Surface((70, 70))
        surf.fill(GREEN)
        surf.set_colorkey(GREEN)

        polygon(surf, (225, 230, 128), ([0, 10],  [40, 0], [60, 5], [70, 20], [50, 10],  [35, 20],
                                        [50, 20], [70, 30], [50, 25], [45, 25], [65, 45], [30, 25],
                                        [28, 23], [20, 20], [15, 25], [15, 40], [10, 60], [0, 50]), 0)
        polygon(surf, BLACK, ([0, 10], [40, 0], [60, 5], [70, 20], [50, 10], [35, 20],
                                       [50, 20], [70, 30], [50, 25], [45, 25], [65, 45], [30, 25],
                                       [28, 23], [20, 20], [15, 25], [15, 40], [10, 60], [0, 50]), 1)
        polygon(surf, GREEN, ([0, 20], [20, 0], [0, 0]), 0)

        surf_feet.blit(surf, (150, 175))
        return surf_feet

    def draw_tail_bird() -> pygame.Surface:
        """
        Функция рисует хвост птицы
        :return: pygame.Surface
        """
        surf = pygame.Surface((100, 100))
        surf.fill(GREEN)
        surf.set_colorkey(GREEN)
        # pygame.draw.rect(surf, BLACK, ([0, 0], [100, 100]))

        polygon(surf, WHITE, ([100, 60], [40, 0], [0, 80], [100, 100]), 0)
        polygon(surf, BLACK, ([100, 60], [40, 0], [0, 80], [100, 100]), 1)

        return surf

    surf_bird = pygame.Surface((555, 365))
    surf_bird.fill(GREEN)
    surf_bird.set_colorkey(GREEN)
    blit_list = []

    tail = draw_tail_bird()
    wing_1 = draw_wing()
    wing_2 = draw_wing()
    wing_2 = pygame.transform.rotate(wing_2, 20)
    beak = draw_beak()
    body = draw_body()
    feet_1 = draw_feet()
    feet_2 = draw_feet()

    blit_list.append((tail, (90, 115)))
    blit_list.append((wing_1, (0, -40)))
    blit_list.append((wing_2, (-50, -20)))
    blit_list.append((beak, (505, 135)))
    blit_list.append((body, (170, 110)))
    blit_list.append((feet_1, (230, 110)))
    blit_list.append((feet_2, (190, 130)))

    for sur, dest in blit_list:
        surf_bird.blit(sur, dest)

    # так как птица нарисована в конкретных значения изменяем размер до заданного на входе
    ratio = bird_length/555
    surf_bird = pygame.transform.flip(surf_bird, x_bool, False)
    surf_bird = pygame.transform.scale(surf_bird, [bird_length, int(365*ratio)])

    surface.blit(surf_bird, (x, y))
    return


def draw_gull(surface, color, x, y, gull_length, width_line):
    """
    Функция рисования чаек
    Рандомно выбирает наклон от -20 до +20 градусов

    :param surface: объект pygame.Surface
    :param color: цвет чайки, подходящем для pygame.Color
    :param x: координата X
    :param y: координата Y
    :param gull_length: Длина чайки
    :param width_line: Толщина линии
    :return:
    """
    surf_length = gull_length/4 * 5
    surf_width = surf_length/10
    gull_surf = pygame.Surface((surf_length, surf_width))
    gull_surf.set_colorkey(BLACK)
    pygame.draw.arc(gull_surf, color, [0, 0, surf_length/3*2, surf_length/3*2],
                    np.pi/3, 3*np.pi/4, width_line)
    pygame.draw.arc(gull_surf, color, [surf_length/3, 0, surf_length/3*2, surf_length/3*2],
                    np.pi/4, 2*np.pi/3, width_line)
    gull_surf = pygame.transform.rotate(gull_surf, random.randint(-20, 20))
    surface.blit(gull_surf, (x-surf_width, y))
    return


def draw_background(surface, size: tuple[int, int], color: tuple[int, int, int, int], x, y):
    """
    Функция рисует фоны: море, небо
    :param surface: объект pygame.Surface
    :param size: размер
    :param color: цвет и прозрачность, подходящем для pygame.Color
    :param x: координата X вставки
    :param y: координата Y вставки
    """
    surf = pygame.Surface(size)
    surf.fill(color)
    surface.blit(surf, (x, y))
    return


def draw_fish(surface, fish_length, x, y, x_bool=False):
    """
    Функция рисует рыбу по заданным координатам
    fish_length > 0
    :param surface: объект pygame.Surface
    :param fish_length: ширина рыбы
    :param x: координата x
    :param y: кордината y, середина рыбы
    :param x_bool: отразить по горизонтали
    :return:
    """
    tail_width = fish_length/4
    body_width = 3*fish_length/4
    body_depth = 2 * body_width*(1 - np.sqrt(3)/2)

    def draw_fish_fin(body_width, body_depth) -> pygame.Surface:
        """
        Функция рисует плавники рыбы
        :param body_width: ширина тела рыбы
        :param body_depth: высота тела рыбы
        :return: поверхность размером с тело рыбы
        """
        surf = pygame.Surface((body_width, body_width))
        surf.fill((255, 255, 255))
        surf.set_colorkey((255, 255, 255))

        # верхний плавник
        polygon(surf, (102, 99, 112), [(body_width/2, body_width/2),
                                       (3/4 * body_width, body_width/2 - 4/5 * body_depth),
                                       (body_width/5, body_width/2 - 9/10 * body_depth)], 0)
        polygon(surf, BLACK, [(body_width / 2, body_width / 2),
                              (3 / 4 * body_width, body_width / 2 - 4 / 5 * body_depth),
                              (body_width / 5, body_width / 2 - 9 / 10 * body_depth)], 1)
        # нижний левый плавник
        polygon(surf, (102, 99, 112), [(body_width / 2, body_width/2),
                                       (body_width / 4, body_width/2 + 5 * body_depth / 6),
                                       (body_width / 10, body_width/2 + 4 * body_depth / 6)], 0)
        polygon(surf, (0, 0, 0), [(body_width / 2, body_width/2),
                                  (body_width / 4, body_width/2 + 5 * body_depth / 6),
                                  (body_width / 10, body_width/2 + 4 * body_depth / 6)], 1)
        # нижний правый плавник
        polygon(surf, (102, 99, 112), [(body_width / 2, body_width/2),
                                       (3 * body_width / 4, body_width/2 + 5 * body_depth / 6),
                                       (9 * body_width / 10, body_width/2 + 4 * body_depth / 6)], 0)
        polygon(surf, (0, 0, 0), [(body_width / 2, body_width/2),
                                  (3 * body_width / 4, body_width/2 + 5 * body_depth / 6),
                                  (9 * body_width / 10, body_width/2 + 4 * body_depth / 6)], 1)
        return surf

    def draw_fish_tail(tail_width, body_depth) -> pygame.Surface:
        """
        Функция рисует хвост рыбы
        :param tail_width: ширина хвоста
        :param body_depth: толщина тела рыбы
        :return: поверхность
        """
        surf = pygame.Surface((tail_width,  5/4 * body_depth + 1))
        surf.fill(WHITE)
        surf.set_colorkey(WHITE)

        polygon(surf, (71, 136, 147), [(tail_width, body_depth/2), (2/3 * tail_width, body_depth/2),
                                       (0, body_depth/4), (tail_width/4, 5/4 * body_depth)])
        polygon(surf, BLACK, [(tail_width, body_depth/2), (2/3 * tail_width, body_depth/2),
                              (0, body_depth/4), (tail_width / 4, 5/4 * body_depth)], 1)
        return surf

    def draw_fish_body(body_width, body_depth) -> pygame.Surface:
        """
        Функция рисует тело рыбы
        :param body_width: ширина тела
        :param body_depth: толщина тела
        :return: поверхность
        """
        surf_body = pygame.Surface((body_width, body_depth))
        surf_body.fill(WHITE)
        surf_body.set_colorkey(WHITE)

        surf = pygame.Surface((body_width, body_depth))
        surf.fill(WHITE)
        surf.set_colorkey(WHITE)

        circle(surf, (71, 136, 147), [body_width / 2, body_width], body_width, 0)
        circle(surf, BLACK, [body_width / 2, body_width], body_width, 1)
        rect(surf, WHITE, (0, body_depth / 2, 1000, 1000))
        surf_body.blit(surf, (0, 0))

        circle(surf, (71, 136, 147), [body_width / 2, body_width * (1 - np.sqrt(3))], body_width, 0)
        circle(surf, BLACK, [body_width / 2, body_width * (1 - np.sqrt(3))], body_width, 1)
        rect(surf, WHITE, (0, body_width * (1 - np.sqrt(3)), 1000, np.sqrt(3) / 2 * body_width))
        surf_body.blit(surf, (0, 0))

        circle(surf_body, (0, 53, 189), [3/4 * body_width, body_depth/2], body_width/20, 0)
        circle(surf_body, (0, 0, 0), [3/4 * body_width, body_depth/2], body_width/60, 0)

        return surf_body

    surf_fish = pygame.Surface((fish_length, fish_length))
    surf_fish.fill(WHITE)
    surf_fish.set_colorkey(WHITE)

    surf_body = draw_fish_body(body_width, body_depth + 1)
    surf_tail = draw_fish_tail(tail_width, body_depth + 1)
    surf_fin = draw_fish_fin(body_width, body_depth)

    surf_fish.blit(surf_fin, (tail_width, fish_length / 2 - body_width / 2))
    surf_fish.blit(surf_body, (tail_width, fish_length/2-body_depth/2))
    surf_fish.blit(surf_tail, (0, fish_length / 2 - body_depth / 2))

    surf_fish = pygame.transform.flip(surf_fish, x_bool, False)

    surface.blit(surf_fish, (x, y - fish_length / 2))
    return


main()
