import statistics
import numpy as np
import matplotlib.pyplot as plt
import math



class MyMath():

    def sequence_sum(x: float, n: int, eps: float):
        if n < 1: raise ValueError
        summand = x
        result = summand
        i = 1
        summands = []

        while abs(summand) > eps and i <= n:
            summands.append(summand)
            summand *= -x * i / (i + 1)
            result += summand
            i += 1

        return (result, n, result/n,  statistics.median(summands), statistics.mode(summands), 
            statistics.variance(summands), statistics.stdev(summands))

    def get_only_sum(x: float, n: int, eps: float):
        if n < 1: raise ValueError
        summand = x
        result = summand
        i = 1

        while  i <= n:
            summand *= -x * i / (i + 1)
            result += summand
            i += 1

        return result


    def plot_series_vs_exact(x_series, y_series, exact_func, title="", xlabel="x", ylabel="y", filename=None):
        x_exact = np.linspace(min(x_series), max(x_series), 100)
        y_exact = exact_func(x_exact)

        plt.figure(figsize=(10, 6))
        plt.plot(x_series, y_series, 'ro-', label='Разложение в ряд (приближенно)')
        plt.plot(x_exact, y_exact, 'b-', label=f'{exact_func.__name__} (точный)')

        # Оформление
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='upper right')
        plt.title(title if title else f'Сравнение разложения в ряд и {exact_func.__name__}')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # Текст и аннотация
        plt.text(
            np.mean(x_series), np.min(y_exact) - 0.2,
            'Приближенное решение содержит погрешность',
            fontsize=10, color='red', ha='center'
        )
        max_idx = np.argmax(y_exact)
        plt.annotate(
            'Максимум',
            xy=(x_exact[max_idx], y_exact[max_idx]),
            xytext=(x_exact[max_idx] + 0.5, y_exact[max_idx] - 0.2),
            arrowprops=dict(facecolor='green', shrink=0.05),
        )

        # Сохранение в файл (если указано)
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')  # dpi - качество, bbox - обрезка пустых полей
            print(f"График сохранён как '{filename}'")

        plt.show()