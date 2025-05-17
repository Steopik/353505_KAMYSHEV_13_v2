import sys
import os
from .classes_task5 import AdvancedMatrix


def menu_task5():
    matrix = AdvancedMatrix(3, 4)
    matrix.generateMatrix(-10, 10)
    print(f"matrix = {matrix.matrix}")
    max_element = matrix.get_max()
    print(f"Максимальный элемент {max_element}")

    matrix2 = AdvancedMatrix.from_matrix(matrix, lambda x: x /  max_element)
    print(f"matrix2 = {matrix2.matrix}")
    print(f"Стандартная дисперсия {round(matrix2.standart_variance(), 2)}")
    print(f"Формульная дисперсия {round(matrix2.my_variance(), 2)}")


