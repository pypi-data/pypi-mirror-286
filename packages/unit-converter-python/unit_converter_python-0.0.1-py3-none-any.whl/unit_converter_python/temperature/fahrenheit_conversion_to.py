"""
Code with functions for converting temperature values into Fahrenheit for:
1 - Celsius
2 - Kelvin
"""

def f_to_c(fahrenheit_input: float):
    """
    Function for converting the temperature value in Fahrenheit to Celsius.

    Args:
        fahrenheit_input (float): Input with temperature value in Fahrenheit.

    Returns:
        float: Temperature value converted into Celsius.
    """

    result = (fahrenheit_input - 32) * (5/9)
    return result

def f_to_k(fahrenheit_input: float):
    """
    Function for converting the temperature value in Fahrenheit to Kelvin.

    Args:
        fahrenheit_input (float): Input with temperature value in Fahrenheit.

    Returns:
        float: Temperature value converted into Kelvin.
    """

    result = (fahrenheit_input + 459.67) * (5/9)
    return result
