"""
    ЗАДАЧА: (http://cs.mipt.ru/python/lessons/lab3.html#id17)
    При помощи подобного кода заставье черепах вести себя как идеальный газ в сосуде. 
"""
from random import randint
import math 
import turtle

turtle.tracer(0, 0)
turtle.setup(700, 700)

turtle.title("Molecules")
number_of_turtles = 50

# отрисовка стенок
border = turtle.Turtle()
border.up()
border.goto(300, 300)
border.down()
border.pensize(6)
border.hideturtle()
border.goto(300, -300)
border.goto(-300, -300)
border.goto(-300, 300)
border.goto(300, 300)
turtle.update()

# создание шариков
pool = [turtle.Turtle(shape='circle', visible=False) for i in range(number_of_turtles)]
for unit in pool:
    unit.penup()
    unit.shapesize(0.5)
    unit.speed(1)
    unit.setheading(randint(-180, 180))
    unit.goto(randint(-245, 245), randint(-245, 245))
    unit.showturtle()


def collision_walls(mol):
    """
    Функция проверяет коллизию стены и черепахи
    и меняет направление черепахи
    :param mol: turtle
    :return:
    """
    rad_mol = 5
    if 297 - mol.ycor() < rad_mol and 0 < mol.heading() < 180:                                    # верхняя стенка
        mol.setheading(-mol.heading())
    elif -297 - mol.ycor() > -rad_mol and 180 < mol.heading() < 360:                              # нижняя стенка
        mol.setheading(-mol.heading())
    elif 297 - mol.xcor() < rad_mol and (0 <= mol.heading() < 90 or 270 < mol.heading() < 360):   # правая стенка
        mol.setheading(180-mol.heading())
    elif -297 - mol.xcor() > -rad_mol and 90 < mol.heading() < 270:                               # левая стенка
        mol.setheading(180-mol.heading())
    return


def collision_mol(mol):
    """
    Функция проверяет коллизию между объектами turtle
    :param mol: turtle
    :return:
    """
    rad_mol = 15

    for unit in pool:
        if mol != unit:
            leng = math.sqrt((unit.xcor() - mol.xcor())**2 + (unit.ycor() - mol.ycor())**2)
            if leng < rad_mol:
                x = mol.heading()  
                mol.setheading(unit.heading())
                unit.setheading(x)
            while leng < rad_mol:
                mol.forward(1)
                leng = math.sqrt((unit.xcor() - mol.xcor())**2 + (unit.ycor() - mol.ycor())**2)
    return


# основное действие

while True:
    incr = 0
    for unit in pool:
        incr += 1
        flag = True
        collision_mol(unit)

        while (297 - abs(unit.ycor())) < 5 or (297 - abs(unit.xcor())) < 5:
            collision_walls(unit)
            flag = False
            unit.forward(5)

        if flag:
            unit.forward(5)
        
        if pool.index(unit) % 5 == 0:
            turtle.update()
