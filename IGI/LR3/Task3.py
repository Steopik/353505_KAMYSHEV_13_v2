import Input_data

def Task3():
    """
    A function to check whether the entered string is a binary number.

    This function prompts the user for manual or automatic input of a string.
    It then checks whether the entered string is a binary number.

    Args: None

    Returns: None
    """

    choice = Input_data.Input_data("Write 1 for manual input, 2 for automatic input: ", int, 1, 2)
    user_input= None
    if choice == 1:
        user_input = Input_data.Input_data("Write input string: ", str)
    else:
        user_input = Input_data.Random_Input(str, 0, 100)
        print(f"Random string = {user_input}")

    if (len(user_input) - 1 == user_input.count("0") + user_input.count("1") 
            and (user_input[0 : 2] == "0b" or user_input[0 : 2] == "0B")):
        print("Your string is binary numb")
    else:
        print("Your string is not binary numb")

if __name__ == "__main__":
    Task3()