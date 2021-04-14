import turtle

turtle.shape("turtle")
turtle.color('blue')

turtle.speed(1)
turtle.width(3)

A_0 = [0, 0, 0, -40, 20, 0, 0, 40, -20, 0]
A_1 = [0, -20, 20, +20, 0, -40]
A_2 = [0, 0, 20, 0, 0, -20, -20, -20, 20, 0]
A_3 = [0, 0, 20, 0, -20, -20, 20, 0, -20, -20]
A_4 = [0, 0, 0, -20, 20, 0, 0, +20, 0, -40]
A_5 = [20, 0, -20, 0, 0, -20, 20, 0, 0, -20, -20, 0]
A_6 = [20, 0, -20, -20, 0, -20, 20, 0, 0, 20, -20, 0]
A_7 = [0, 0, 20, 0, -20, -20, 0, -20]
A_8 = [0, 0, 20, 0, 0, -40, -20, 0, 0, 40, 0, -20, 20, 0]
A_9 = [0, -40, 20, 20, 0, 20, -20, 0, 0, -20, 20, 0]


def pochta(A):
    X = []
    Y = []
    for i in range(len(A)):
        if ((i+1) % 2 > 0):
            X.append(A[i])
        else:
            Y.append(A[i])

    turtle.penup()
    turtle.goto(turtle.xcor()+X[0], turtle.ycor()+Y[0])
    turtle.pendown()

    for i in range(len(X)-1):
        turtle.goto(turtle.xcor()+X[i+1], turtle.ycor()+Y[i+1])


def otstup(kol: int, siz=1):
    for i in range(siz):
        turtle.penup()
        turtle.goto(20*(kol+i) + 15*(kol+i), 0)
        turtle.pendown()
    return kol + siz-1

B = [A_0, A_1, A_2, A_3, A_4, A_5, A_6, A_7, A_8, A_9]

B_1 = []
with open('input.txt') as file:
    for line in file:
        S = line.rsplit('\n')
        S = list(map(int, S[0].split(', ')))
        B_1.append(S)

A = list(map(int, turtle.textinput('Ввод', 'Введите цифры (через пробел!):').split()))
A_sorted = []
k = 0
for i in range(len(A)):
    if len(str(A[i])) != 1:
        for j in str(A[i]):
            pochta(B_1[int(j)])
            k += 1
            k = otstup(k)

            A_sorted.append(str(j))
    else:
        pochta(B_1[A[i]])
        k += 1
        k = otstup(k)
        A_sorted.append(str(A[i]))
out = open('output.txt', 'w')
out.write('Были введены числа: ' + ', '.join(A_sorted))

out.close()
input('Нажмите "Enter" что бы продолжить...')
