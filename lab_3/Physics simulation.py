import numpy as np
import turtle

turtle.tracer(1, 5)
turtle.shape("circle")
turtle.color('Red')
turtle.speed(0)
turtle.shapesize(0.4)
turtle.goto(500, 0)
turtle.goto(-500, 0)

ugol = np.radians(60)                  # agle in radian
V = 50                                 # start speed
X_0 = -450                             # start coordinate
g = 9.80665                            # Gravitational constant
h = (V**2 * np.sin(ugol)**2) / (2*g)   # height calculation
L = 0                                  # length

while h >= 0.01:

    V = np.sqrt((h * 2*g) / np.sin(ugol)**2)        # calculation spped
    L = (V**2 * np.sin(2 * ugol)) / g               # calculation length
    t_0 = (2 * V * np.sin(ugol)) / g                # calculation all time
    for i in range(int(t_0*30)+1):                  # 1 second = 30 + 1 steps
        t = i/30
        X = X_0 + V * np.cos(ugol) * t              # coordinate X
        Y = V * np.sin(ugol) * t - ((g * t**2)/2)   # coordinate Y
        turtle.goto(X, Y)
        
    h /= 2                # loss of energy
    X_0 += L
turtle.exitonclick()
