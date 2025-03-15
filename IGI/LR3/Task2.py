import Input_data

def Task2():
    """
    A function for finding the number of numbers less than 12.

    This function prompts the user for manual or automatic input of integers.
    Then it finds the sum of the numbers less than 12.

    Args: None

    Returns: None
    """

    quantity = 0
    choice = Input_data.Input_data("Write 1 for manual input, 2 for automatic input: ", int, 1, 2)

    if choice == 1:
        while True:
            numb = Input_data.Input_data("Write numb: ", int)
            if numb == 0:
                break
            if numb > 12:
                quantity += 1
    else:
        while True:
            numb = Input_data.Random_Input(int, -100000, 100000)
            if numb == 0:
                break
            if numb > 12:
                quantity += 1

    print(f"Input is finished. Number of numbers is more than 12 - {quantity}")

if __name__ == "__main__":
    Task2()