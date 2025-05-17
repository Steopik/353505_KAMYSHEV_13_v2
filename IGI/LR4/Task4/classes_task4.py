import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
from abc import ABC, abstractmethod
import math



class GeometricFigure:
    @abstractmethod
    def calculate_area(self):
        pass

class FigureColor:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value


class Triangle(GeometricFigure):
    name = "Треугольник"  
    
    def __init__(self, a, b, c, color):
        """
        Конструктор треугольника
        :param a: сторона a
        :param b: сторона b
        :param c: сторона c
        :param color: цвет фигуры
        """
        self.a = a
        self.b = b
        self.c = c
        self.color = FigureColor(color)
        self.validate_triangle()

    def validate_triangle(self):
        """Проверка, что треугольник с такими сторонами может существовать"""
        sides = sorted([self.a, self.b, self.c])
        if sides[0] + sides[1] <= sides[2]:
            raise ValueError("Треугольник с такими сторонами не существует")

    def calculate_area(self):
        """Вычисление площади по формуле Герона"""
        p = (self.a + self.b + self.c) / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def get_parameters(self):
        """Возвращает строку с параметрами фигуры"""
        return "Фигура: {name}\nСтороны: a={a}, b={b}, c={c}\nЦвет: {color}\nПлощадь: {area:.2f}".format(
            name=self.name,
            a=self.a,
            b=self.b,
            c=self.c,
            color=self.color.color,
            area=self.calculate_area()
        )

    @classmethod
    def get_figure_name(cls):
        """Метод класса для получения названия фигуры"""
        return cls.name
    
    
    def draw(self, path, label=""):
        alpha = math.acos((self.b**2 + self.c**2 - self.a**2) / (2 * self.b * self.c))
        x1, y1 = 0, 0
        x2, y2 = self.c, 0

        x3 = self.b * math.cos(alpha)
        y3 = self.b * math.sin(alpha)

        fig, ax = plt.subplots()
        triangle = patches.Polygon(
            [(x1, y1), (x2, y2), (x3, y3)],
            closed=True,
            fill=True,
            color=self.color.color
        )

        ax.add_patch(triangle)

        try:
            rgb = mcolors.to_rgb(self.color.color)
            text_color = 'white' if sum(rgb)/3 < 0.5 else 'black'
        except:
            text_color = 'black'

        ax.text(
            (x1 + x2 + x3)/3, (y1 + y2 + y3)/3,  # Центр треугольника
            label,
            ha='center',
            va='center',
            color=text_color,
            fontsize=12,
            bbox=dict(facecolor='gray', alpha=0.3)
        )

        margin = max(self.a, self.b, self.c) * 0.1
        ax.set_xlim(min(x1, x2, x3) - margin, max(x1, x2, x3) + margin)
        ax.set_ylim(min(y1, y2, y3) - margin, max(y1, y2, y3) + margin)
        ax.set_aspect('equal')
        ax.set_title(f"{self.name}\nПлощадь: {self.calculate_area():.2f}")
        ax.grid(True, linestyle='--', alpha=0.7)


        plt.savefig(path)
        plt.show()