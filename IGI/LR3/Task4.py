import string


def Task4():
    """
    A control function for calling sub-functions for processing strings

    This function calls 3 subfunctions and displays the result of their operation.

    Args: None

    Returns: None
    """


    START_STRING = "So she was considering in her own mind, as well as she " \
    "could, for the hot day made her feel very sleepy and stupid, whether the " \
    "pleasure of making a daisy-chain would be worth the trouble of getting up " \
    "and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    words = START_STRING.split(" ")

    lowercase_number, uppercase_number = Sub_task1(START_STRING)
    print(f"Quantity lowercase letters = {lowercase_number}. Quantity uppercase letters = {uppercase_number}")

    index, word = Sub_task2(words)
    print(f"First word on 'z' is {word}. His numb is {index}")

    print("New string is:")
    print(Sub_task3(words))


    


def Sub_task1(s: str):
    """
    A function for counting the number of uppercase and lowercase letters.

    Args: 
    - s (str): The input string.

    Returns: 
    - tuple:
        - lowercase_number (int): Count of lowercase letters in input string.
        - uppercase_number (int): Count of uppercase letters in input string.
    """

    lowercase_number = 0
    uppercase_number = 0

    for i in string.ascii_lowercase:
        lowercase_number += s.count(i)

    for i in string.ascii_uppercase:
        uppercase_number += s.count(i)

    return lowercase_number, uppercase_number


def Sub_task2(words_list):
    """
    A function for finding the first word containing the letter 'z' of its index.

    Args: 
    - words_list (list<str>): The input string divided into separate words.

    Returns: 
    - tuple:
        - index (int/None): Index of first word with letter 'z'.
        - element (str/None): First word with letter 'z'.
    """
    for index, element in enumerate(words_list):
        if "z" in element:
            return index, element
    return "None","None"


def Sub_task3(words_list):
    """
    A function for deleting words starting with the letter 'a'
    
    Args: 
    - words_list (list<str>): The input string divided into separate words.

    Returns: 
    - new_string (str): Processed string.
    """

    for index, element in enumerate(words_list):
        if element[0] == "a":
            if "," in element:
                words_list[index] = ","
            else:
                words_list[index] = ""
    new_string = ""
    for element in words_list:
        if (element == ","):
            new_string = new_string.rstrip()
        new_string += element + " "
    return new_string.rstrip()
