from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area_calc(self):
        pass

class Circle(Shape):
    def __init__(self, radius: int | float):
        if radius <= 0:
            raise ValueError("The radius must be a positive number")
        self.radius = radius

    def area_calc(self):
        return math.pi * self.radius ** 2

class Triangle(Shape):
    def __init__(self,
                 s1: int | float,
                 s2: int | float,
                 s3: int | float):
        self.sides = sorted([s1, s2, s3])
        if not all(map(lambda i: i > 0, self.sides)):
            raise ValueError("The sides of triangle can not be negative")
        if self.sides[2] > self.sides[0] + self.sides[1]:
            raise ValueError("A triangle with given sides does not exist")

    def area_calc(self):
        p = sum(self.sides) / 2
        return math.sqrt(p * (p - self.sides[0]) * (p - self.sides[1]) * (p - self.sides[2]))

    def is_right_angle(self):
        return math.isclose(self.sides[0] ** 2 + self.sides[1] ** 2, self.sides[2] ** 2)
