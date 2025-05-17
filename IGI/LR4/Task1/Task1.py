from . import work_with_file
from . import classes_task1

import sys
import os

# Добавляем путь к родительской директории (где лежит Input_data.py) в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Input_data


def menu_task1():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "summary.csv")
    pickle_path = os.path.join(base_dir, "summary.pickle")

    summary = {}

    while True:
        print("Меню")
        print("1. Добавить товар")
        print("2. Вывести список товаров")
        print("3. Отсортировать список товаров")
        print("4. Вывести список стран по введенному товару")
        print("5. Сохранить данные в файл CSV")
        print("6. Загрузить данные из файла CSV")
        print("7. Сохранить данные в файл pickle")
        print("8. Загрузить данные из файла pickle")
        print("0. Выход")

        choice = Input_data.Input_data("Выберите пункт меню: ", int, 0, 10)

        if choice == 1:
            name = input("Введите название товара: ")
            supply_volume = Input_data.Input_data("Введите объем поставок: ", int, 0)
            origin_сountry = input("Введите название страны: ")

            intelligence = classes_task1.ProductIntelligence(name, supply_volume, origin_сountry)
            if name not in summary:
                summary[name] = []
            summary[name].append(intelligence)

        elif choice == 2:
            for product, intelligences in summary.items():
                print(product + ":")
                for i in intelligences:
                    print(i.get_info())
        elif choice == 3:
            summary = {k: summary[k] for k in sorted(summary)}

        elif choice == 4:
            name = input("Введите название товара: ")
            
            if name not in summary:
                print("Такого товара нет")
            else:
                print("Список стран:")
                for product, intelligences in summary.items():
                    if product == name:
                        for i in intelligences:
                            print(i.origin_сountry)
        elif choice == 5:
            work_with_file.write_to_csv(summary,csv_path )
        elif choice == 6:
            summary = work_with_file.load_from_csv(csv_path)
        elif choice == 7:
            work_with_file.write_to_pickle(summary, pickle_path)
        elif choice == 8:
            summary = work_with_file.load_from_pickle(pickle_path)
        elif choice == 0:
            return

