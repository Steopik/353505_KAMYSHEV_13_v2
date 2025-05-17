import Input_data
import functools
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def log_execution(func):
    """
    Decorator function to displays the function's operation status.

    This decorator wraps the input function and displays the function's operation status.

    Args:
    - func (function): The function to be decorated.

    Returns:
    - wrapper (function): The wrapper function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Запущена функция: {func.__name__}")

        result = func(*args, **kwargs)

        logging.info(f"Завершена функция: {func.__name__}")

        return result
    return wrapper


@log_execution
def Task5():
    """
    Function to process text and perform various operations.

    This function finds the product of the positive elements of the list 
    and the sum of the list elements arranged up to the minimum element modulo.

    Args: None

    Returns: None
    """

    size = Input_data.Input_data("Write size of list: ", int, 1)
    composition = 1
    sum = 0
    min_element = float("inf")
    numb_list = []

    for i in Input_data.List_Input(size, "Input next numb: "):
        if i > 0:
            composition *= i

        if abs(i) < abs(min_element):
            min_element = i

        numb_list.append(i)

    for i in numb_list:
        if i == min_element:
            break
        sum += i

    print(f"Composition: {composition}")
    print(f"Sum: {sum}")


