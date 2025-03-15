import Task1
import Task2
import Task3
import Task4
import Task5
import Input_data

def menu():
    """
    Function to display the main menu and execute the selected task.

    The function displays a menu with options for each task and prompts the user for input.
    Based on the user's choice, it executes the corresponding task or exits the program.

    Args: None

    Returns: None
    """
    while True:
        choice = Input_data.Input_data("Write numb of task (1 - 5) or 0 to Exit: ", int, 0, 6)

        match choice:
            case 1:
                Task1.Task1()
            case 2:
                Task2.Task2()
            case 3:
                Task3.Task3()
            case 4:
                Task4.Task4()
            case 5:
                Task5.Task5()
            case 0:
                break
    