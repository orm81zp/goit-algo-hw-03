""" 
Модуль для малювання сніжинки.
Приймає рівень рекурсії та розмір як аргументи командного рядка. 3 та 500 за замовчуванням
"""

from turtle import Turtle, Screen
import sys


def parse_arguments():
    """Отримує аргументи командного рядка"""

    order = "3"
    size = "500"

    if len(sys.argv) > 2:
        order = sys.argv[1]
        size = sys.argv[2]
    elif len(sys.argv) > 1:
        order = sys.argv[1]

    order = int(order)
    size = int(size)

    print(f"Розмір: {size}, рівень рекурсії: {order}")
    print()

    return (order, size)


def draw_snowflake(turtle: Turtle, size, order):
    """Малює сніжинку. Викликає сама себе із зменшенням рівня рекурсії"""

    if order == 0:
        turtle.forward(size)
    else:
        size = size / 3
        order -= 1

        draw_snowflake(turtle, size, order)
        turtle.left(60)
        draw_snowflake(turtle, size, order)
        turtle.right(120)
        draw_snowflake(turtle, size, order)
        turtle.left(60)
        draw_snowflake(turtle, size, order)


def main():
    """Отримає параметри з командного рядка, якщо були передані та запускає малювання сніжинки"""

    order, size = parse_arguments()
    screen = Screen()
    screen.bgcolor("white")

    turtle = Turtle()
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-size / 2, size / 3)
    turtle.pendown()

    for _ in range(3):
        draw_snowflake(turtle, size, order)
        turtle.right(120)

    screen.mainloop()


if __name__ == "__main__":
    main()
