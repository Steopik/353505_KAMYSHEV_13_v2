import sys
import os
from . import classes_task3
from tabulate import tabulate
import math
import numpy as np

MAX_ITERATIONS_QUANTITY = 500

# Добавляем путь к родительской директории (где лежит Input_data.py) в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Input_data

def menu_task3():
    base_dir = os.path.dirname(__file__)
    png_path = os.path.join(base_dir, "graphik.png")
    while True:
            x = Input_data.Input_data("Write x: ", float, -1, 1)
            if x == -1:
                print("Error: Value must be at least 1. Please enter a valid value.")
            elif x == 1:
                print("Error: Value must be at most 1. Please enter a valid value.")
            else:
                break

    eps = Input_data.Input_data("Write eps: ", float, 0, 1)

    result, n, average, median, mode, variance, stdev = classes_task3.MyMath.sequence_sum(x, MAX_ITERATIONS_QUANTITY, eps)

    actual_value = math.log(1 + x)
    table_data = [
        [x, n, result, actual_value, eps, average, median, mode, variance, stdev]
    ]
    table_headers = ["x", "n", "F(x)", "Math F(x)", "eps", "average", "median", "mode", "variance", "stdev"]
    table = tabulate(table_data, headers=table_headers, floatfmt=".8f")
    print(table)


    x_points = []
    x_points.append(-1 + eps)
    y_points = []
    y_points.append(classes_task3.MyMath.get_only_sum(x_points[-1], MAX_ITERATIONS_QUANTITY, eps))
    a = math.log(eps + 1)
    while x_points[-1] < 1:
         x_points.append(x_points[-1] + eps)
         y_points.append(classes_task3.MyMath.get_only_sum(x_points[-1], MAX_ITERATIONS_QUANTITY, eps))


    classes_task3.MyMath.plot_series_vs_exact(x_points, y_points, np.log, title='Разложние lox(x + 1) в ряд', filename= png_path)
