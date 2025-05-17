import math
import Input_data
from tabulate import tabulate

def Task1():
    """
    Function to compute the natural logarithm approximation using Taylor series expansion.

    This function prompts the user for manual or automatic input of x and epsilon values.
    It then calculates the natural logarithm approximation using the Taylor series expansion.
    The result is displayed in a table format showing the input values, number of iterations,
    computed approximation, actual mathematical value, and epsilon.

    Args: None

    Returns: None
    """

    MAX_ITERATIONS_QUANTITY = 500
    choice = Input_data.Input_data("Write 1 for manual input, 2 for automatic input: ", int, 1, 2)
    if choice == 1:
        while True:
            x = Input_data.Input_data("Write x: ", float, -1, 1)
            if x == -1:
                print("Error: Value must be at least 1. Please enter a valid value.")
            elif x == 1:
                print("Error: Value must be at most 1. Please enter a valid value.")
            else:
                break

        eps = Input_data.Input_data("Write eps: ", float, 0, 1)

    else:
        x = Input_data.Random_Input(float, -0.999999999999999, 0.9999999999999999)
        eps = Input_data.Random_Input(float, 0, 1)
    
    n = 1
    summand = x
    result = summand

    while abs(summand) > eps and n <= MAX_ITERATIONS_QUANTITY:
        summand *= -x * n / (n + 1)
        result += summand
        n += 1


    actual_value = math.log(1 + x)
    table_data = [
        [x, n, result, actual_value, eps]
    ]
    table_headers = ["x", "n", "F(x)", "Math F(x)", "eps"]
    table = tabulate(table_data, headers=table_headers, floatfmt=".8f")
    print(table)

