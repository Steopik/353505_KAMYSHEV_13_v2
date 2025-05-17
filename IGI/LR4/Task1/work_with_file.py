import csv
import pickle
from . import classes_task1
import os


def load_from_csv(file_path):
    summary = {}
    with open(file_path, "r") as file:
        _reader = csv.reader(file)
        if os.path.getsize(file_path) != 0:
            next(_reader)
            for row in _reader:
                product_name, supply_volume, origin_сountry = row
                if product_name not in summary:
                    summary[product_name] = []
                syn = classes_task1.ProductIntelligence(product_name, supply_volume, origin_сountry)
                summary[product_name].append(syn)
    return summary


def write_to_csv(summary: dict, file_path):
    with open(file_path, "w", newline="") as file:
        _writer = csv.writer(file)
        _writer.writerow(["Товар", "Количество", "Производитель"])
        for productm, inform in summary.items():
            for i in inform:
                _writer.writerow([productm, i.supply_volume, i.origin_сountry])
    print("Данные успешно сохранены в csv")


def load_from_pickle(file_path):
    with open(file_path, "rb") as file:
        synonyms = pickle.load(file)
    return synonyms


def write_to_pickle(summary: dict, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(summary, file)
    print("Данные успешно сохранены в pickle")