import numpy as np
from typing import Callable

class Matrix:
    def __init__(self, rows, columns):
        self._matrix = np.ndarray([rows, columns])
        self._rows = rows
        self._columns = columns

    def generateMatrix(self, min_value: int, max_value: int):
        self._matrix = np.random.randint(min_value, max_value, size=(self._rows, self._columns))

    @property
    def matrix(self):
        return self._matrix
    
    @matrix.setter
    def matrix(self, value):
        self._matrix = value


class AdvancedMatrix(Matrix):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.generateMatrix(rows, columns)  

    @classmethod
    def from_matrix(cls, other: "AdvancedMatrix", func: Callable  = None):
        obj = cls(other._rows, other._columns)
        if func is not None:
            obj._matrix = np.vectorize(func)(other._matrix)
        else:
            obj._matrix = np.copy(other._matrix)
        return obj 
    
    def get_max(self):
        return max(self._matrix.flatten(), key=lambda x: abs(x))

    
    def standart_variance(self):
        return np.var(self._matrix)
    

    def my_variance(self):
        mean_val = np.mean(self._matrix)
        flattened = self._matrix.flatten()
        return sum((x - mean_val) ** 2 for x in flattened) / len(flattened)

    