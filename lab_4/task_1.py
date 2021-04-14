import numpy as np
import pygame
from pygame.draw import *


def main():
    FPS = 30
    bg_color = (230, 230, 230)
    screen.fill(bg_color)

    center_face_x = 200
    center_face_y = 200
    face_radius = 150

    center_eye_right_x = 275
    center_eye_right_y = 150
    center_eye_left_x = 125
    center_eye_left_y = 150
    eye_right_radius = 20
    eye_left_radius = 30

    width_eyebrow = 100
    angle_eyebrow = 60

    mouth_x = 100
    mouth_y = 240
    mouth_width = 200
    mouth_height = 50

    draw_face(center_face_x, center_face_y, face_radius)

    draw_eyebrow(angle_eyebrow, eye_left_radius, center_eye_left_x, center_eye_left_y, width_eyebrow)
    draw_eyebrow(180 - angle_eyebrow, eye_right_radius, center_eye_right_x, center_eye_right_y, - width_eyebrow)

    draw_eye(eye_right_radius, center_eye_right_x, center_eye_right_y)
    draw_eye(eye_left_radius, center_eye_left_x, center_eye_left_y)

    draw_mouth(mouth_x, mouth_y, mouth_width, mouth_height)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
    pygame.quit()


def draw_face(center_face_x, center_face_y, face_radius):
    circle(screen, (255, 255, 0), (center_face_x, center_face_y), face_radius)


def draw_eye(eye_radius, center_eye_x, center_eye_y):
    circle(screen, (255, 0, 0), (center_eye_x, center_eye_y), eye_radius)
    circle(screen, (0, 0, 0), (center_eye_x, center_eye_y), 10)


def draw_mouth(mouth_x, mouth_y, mouth_width, mouth_height):
    rect(screen, (0, 0, 0), (mouth_x, mouth_y, mouth_width, mouth_height))

    teeth_n = 10
    color = (255, 255, 255)
    rect(screen, color, (mouth_x, mouth_y, mouth_width, mouth_height), 2)
    line(screen, color, (mouth_x, mouth_y+mouth_height/2), (mouth_x + mouth_width, mouth_y+mouth_height/2))
    teeth_width = mouth_width / (teeth_n)
    X = mouth_x
    for i in range(teeth_n-1):
        # берем начало рта и двигаемся отрисовывая каждый зуб
        X += teeth_width
        line(screen, color, (X, mouth_y), (X, mouth_y + mouth_height))


def draw_eyebrow(angle_a, circle_radius, circle_x, circle_y, width_rectangle, height_rectangle=10):
    """
    (Брови смайлику)
    Функция: Построение прямоугольника по касательной к окружности
    ширина прямоугольника делится в отношении 1 к 4,
    если передать отрицательное значение ширины, то прямоугольник (бровь) можно перевернуть
    высота прямоугольника - по умолччанию 10

    :param angle_a: Угол под каторым касательная касается окружности
    :param circle_radius: Радиус окружности
    :param circle_x: Координаты центра по оси X
    :param circle_y: Координаты центра по оси Y
    :param width_rectangle: Длина/ширина стороны которая касается окружности
    :param height_rectangle: Высота прямоугольника
    :return: None
    """

    sin_a = np.sin(np.radians(angle_a))
    cos_a = np.cos(np.radians(angle_a))

    # координаты точки касания на окружности
    X = circle_x + cos_a*circle_radius
    Y = circle_y - sin_a*circle_radius
    # координаты первой точки прямоугольника
    a_x = X - sin_a * 0.8*width_rectangle
    a_y = Y - cos_a * 0.8*width_rectangle
    # координаты второй точки прямоугольника
    a_x_2 = X + sin_a * 0.2*width_rectangle
    a_y_2 = Y + cos_a * 0.2*width_rectangle
    # точки для смещения ширины
    st_x = cos_a * height_rectangle
    st_y = sin_a * height_rectangle

    polygon(screen, (0, 0, 0), [(a_x, a_y), (a_x_2, a_y_2),
                                (a_x_2 + st_x, a_y_2 - st_y),
                                (a_x + st_x, a_y - st_y)], 0)


screen = pygame.display.set_mode((400, 400), pygame.NOFRAME)
main()












