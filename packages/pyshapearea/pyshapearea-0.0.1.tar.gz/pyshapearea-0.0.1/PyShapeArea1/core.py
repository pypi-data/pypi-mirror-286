import math


def circle(r):
    "Calculating circle area"
    return math.pow(r, 2) * math.pi


def triangle(x1, x2, x3):
    "Calculating triangle area"
    p = (x1 + x2 + x3)/2
    return math.sqrt(
        p*(p-x1)*(p-x2)*(p-x3))


def right_triangle(x1, x2, x3):
    "Checking, if a triangle is right triangle"
    if math.pow(x1, 2) + math.pow(x2, 2) == math.pow(x3, 2):
        return True
    if math.pow(x3, 2) + math.pow(x2, 2) == math.pow(x1, 2):
        return True
    if math.pow(x1, 2) + math.pow(x3, 2) == math.pow(x2, 2):
        return True
    else:
        return False
