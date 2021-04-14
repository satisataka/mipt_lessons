import turtle
import random
print("Hello world")


turtle.shape("turtle")
turtle.color('Red')
turtle.speed(10)


for i in range(1000):
    turtle.left(random.randint(-180, 180))

    a = random.randint(-20, 20)
    turtle.forward(a)
turtle.exitonclick()
