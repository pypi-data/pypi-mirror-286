from typing import List
from functools import reduce
from math import sqrt, pi


class GeometryFigure(object):
    """
    Base geometry figure class
    """

    def __init__(self) -> None:
        self.area = None

    def get_area(self) -> float:
        """
        :return: float representing the area of the figure
        """
        return self.area


class Triangle(GeometryFigure):
    """
    A triangle figure class
    """

    def __init__(self, sides: List[float]) -> None:
        """
        :param sides: 3 floats representing the sides of the triangle
        """
        super().__init__()
        self.sides = sorted(sides)
        self.s_p = sum(sides) / 2
        self.area = sqrt(self.s_p * reduce(lambda x, y: x * y,
                                           [self.s_p - side for side in self.sides]))

    def update_sides(self, sides: List[float]) -> None:
        """
        :param sides: 3 floats representing the sides of the
        :return: None
        """
        self.sides = sorted(sides)
        self.s_p = sum(sides) / 2
        self.area = sqrt(self.s_p * reduce(lambda x, y: x * y,
                                           [self.s_p - side for side in self.sides]))

    def is_right_triangle(self, error: float = 0.0001) -> bool:
        """
        :param error: maximum error of float comparison
        :return: True if the triangle is right-angled, False otherwise
        """

        return abs(self.sides[2] ** 2 - self.sides[0] ** 2 - self.sides[1] ** 2) < error


class Circumference(GeometryFigure):
    """
    A circumference figure class
    """

    def __init__(self, radius: float) -> None:
        """
        :param radius: radius of the Circumference
        """
        super().__init__()
        self.radius = radius
        self.area = pi * radius ** 2

    def update_radius(self, radius: float) -> None:
        """
        :param radius: radius of the Circumference
        """
        self.radius = radius
        self.area = pi * radius ** 2
