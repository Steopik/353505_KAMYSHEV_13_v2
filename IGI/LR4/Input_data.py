<<<<<<< HEAD
def input_data(prompt, data_type, min_value=None, max_value=None):
    """
    Function to get user input with data type validation and optional value range constraints.
=======
import random
import string

def Input_data(promt: str, data_type: type, min_value=None, max_value=None):

    '''
    A function for receiving user input
>>>>>>> I_LR4

    Args:
    - prompt (str): The prompt message for the user.
    - data_type (type): The expected data type for user input (int, float, or str).
<<<<<<< HEAD
    - min_value (int/float, optional): The minimum allowed value (inclusive). Defaults to None.
    - max_value (int/float, optional): The maximum allowed value (inclusive). Defaults to None.
=======
    - min_value (int/float/str, optional): The minimum allowed value (inclusive). Defaults to None.
    - max_value (int/float/str, optional): The maximum allowed value (inclusive). Defaults to None.
>>>>>>> I_LR4

    Returns:
    - user_input (int/float/str): The validated user input.

    Raises:
    - ValueError: If the user input does not match the specified data type or falls outside the specified range.
<<<<<<< HEAD
    """

    while True:
        try:
            user_input = data_type(input(prompt))
            if min_value is not None and user_input < min_value:
                raise ValueError(f"Value must be at least {min_value}")
            if max_value is not None and user_input > max_value:
                raise ValueError(f"Value must be at most {max_value}")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid value.")
=======
    '''

    while True:
        try:
            data = data_type(input(promt))

            if min_value is not None and data < min_value:
                raise ValueError(f"Value must be less than {min_value}")
            
            if max_value is not None and data > max_value:
                raise ValueError(f"Value must be more than {max_value}")
                
            return data
        except Exception as e:
            print(f"Error: {e}. Please enter a valid value.")



def Random_Input(data_type: type, min_value=None, max_value=None):
    """
    Function to generate random data based on the specified data type and optional value range constraints.

    Args:
    - data_type (type): The data type for the generated value (int, float, or str).
    - min_value (int/float, optional): The minimum allowed value (inclusive). Defaults to None.
    - max_value (int/float, optional): The maximum allowed value (inclusive). Defaults to None.

    Returns:
    - generated_value (int/float/str): The randomly generated value.

    Raises:
    - ValueError: If the specified data type is not supported (supported types: int, float, str).
    """


    if data_type == str:
        if min_value is None:
            min_value = 1
        if max_value is None:
            max_value = 10

        generated_value = ''.join(
            random.choices(string.ascii_letters + string.digits, k=random.randint(min_value, max_value)))
        return generated_value

    if min_value is None:
        min_value = float('-inf')
    if max_value is None:
        max_value = float('inf')

    if data_type == int:
        generated_value = random.randint(min_value, max_value)
    elif data_type == float:
        generated_value = random.uniform(min_value, max_value)
    else:
        raise ValueError("Unsupported data type. Supported types are int, float, and str.")

    return generated_value


def List_Input(size: int, promt):
    """
    Function to receiving set of real numbers.

    Args:
    - size (int): The size of the input set.
    - prompt (str): The prompt message for the user.

    Yields:
    -float: The next real number provided by the user.
    """
    
    for i in range(size):
        try:
            yield Input_data(promt, float)
        except Exception as e:
            print(f"{e}")


>>>>>>> I_LR4
