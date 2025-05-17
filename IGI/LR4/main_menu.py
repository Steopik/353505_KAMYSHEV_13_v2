from  Task1.Task1 import menu_task1
from  Task2.Task2 import menu_task2
from  Task3.Task3 import menu_task3
from  Task4.Task4 import menu_task4
from  Task5.Task5 import menu_task5
import Input_data


def menu():
    """
        Developer Stsyapan Kamyshev
        date: 12.04.2025
        function is developed for choosing one of five provided functions
        """
    while True:
        user_chs = Input_data.Input_data("0 - exit from program,\n 1 - Работа со списком товаров, \n"
                                    "2 - Анализ файла,\n 3 - Функция и ряд Тейлора\n"
                                    " 4 - Треугольник и его отрисовка,\n"
                                         "5 - анализ и работата с матрицей: ", int, 0, 5)
        if user_chs == 0:
            return
        elif user_chs == 1:
            menu_task1()
        elif user_chs == 2:
            menu_task2()
        elif user_chs == 3:
            menu_task3()
        elif user_chs == 4:
            menu_task4()
        elif user_chs == 5:
            menu_task5()
