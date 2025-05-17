import sys
import os
from .classes_task4 import Triangle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Input_data


def menu_task4():
    base_dir = os.path.dirname(__file__)
    png_path = os.path.join(base_dir, "triangle.png")

    print("Создание треугольника")
    
    a = Input_data.Input_data("Введите длину стороны a: ", float, 0.1)
    b = Input_data.Input_data("Введите длину стороны b: ", float, 0.1)
    c = Input_data.Input_data("Введите длину стороны c: ", float, 0.1)
    color = input("Введите цвет треугольника: ")
    label = input("Введите подпись для треугольника: ")

    try:
        triangle = Triangle(a, b, c, color)
        
        print("\n" + triangle.get_parameters())
        
        triangle.draw(png_path, label)
        
        print(f"Изображение сохранено в {png_path}")
        
        

    except ValueError as e:
        print(f"Ошибка: {e}")

