from random import randint
import math 
import turtle

turtle.tracer(0, 0)
turtle.setup(700, 700)

turtle.bgcolor('#a1dffb')
turtle.title("Balls")

number_of_turtles = 10

# отрисовка стенок
border = turtle.Turtle()
border.up()
border.goto(300, 300)
border.down()
border.pensize(6)
border.color('#f9de59')
border.hideturtle()
border.goto(300, -300)
border.goto(-300, -300)
border.goto(-300, 300)
border.goto(300, 300)
turtle.update()

# создание шариков
pool = [turtle.Turtle(shape='circle', visible=False) for i in range(number_of_turtles)]
for unit in pool:
    unit.color('pink')
    unit.penup()
    unit.shapesize(4)
    unit.speed(0)
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
    rad_mol = 40
    if 297 - mol.ycor() < rad_mol and 0 < mol.heading() < 180:  # верхняя стенка
        mol.setheading(-mol.heading())
    elif -297 - mol.ycor() > -rad_mol and 180 < mol.heading() < 360:  # нижняя стенка
        mol.setheading(-mol.heading())
    elif 297 - mol.xcor() < rad_mol and (0 <= mol.heading() < 90 or 270 < mol.heading() < 360):  # правая стенка
        mol.setheading(180 - mol.heading())
    elif -297 - mol.xcor() > -rad_mol and 90 < mol.heading() < 270:  # левая стенка
        mol.setheading(180 - mol.heading())
    return

def collision_mol(mol):
    """
    Функция проверяет коллизию между объектами turtle
    :param mol: turtle
    :return:
    """
    rad_mol = 80
    for unit in pool:
        if mol != unit:
            leng = math.sqrt((unit.xcor() - mol.xcor()) ** 2 + (unit.ycor() - mol.ycor()) ** 2)
            if leng < rad_mol:
                mol.color('#f9de59')
                unit.color('#e8a628')
                x = mol.heading()
                mol.setheading(unit.heading())
                unit.setheading(x)
            while leng < rad_mol:
                mol.forward(1)
                leng = math.sqrt((unit.xcor() - mol.xcor()) ** 2 + (unit.ycor() - mol.ycor()) ** 2)
    return


incr = 0
while True:
    incr += 1
    for unit in pool:
        key = False

        if incr % 100 == 0:
            unit.color('pink')
            unit.clear()

        collision_mol(unit) 

        while (297 - abs(unit.ycor())) < 40 or (297 - abs(unit.xcor())) < 40:
            unit.color('#f98365')
            key = True
            collision_walls(unit)
            unit.forward(1)

        if not key:
            unit.forward(1)
    turtle.update()
