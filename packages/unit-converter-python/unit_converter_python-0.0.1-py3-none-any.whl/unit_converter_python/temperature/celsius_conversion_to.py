"""
Code with functions for converting temperature values into Celsius for:
1 - Fahrenheit
2 - Kelvin
"""

def c_to_f(celsius_input: float):
    """
    Function for converting the temperature value in Celsius to Fahrenheit.

    Args:
        celsius_input (float): Input with temperature value in Celsius.

    Returns:
        float: Temperature value converted into Fahrenheit.
    """

    result = (celsius_input * (9/5)) + 32
    return result

def c_to_k(celsius_input: float):
    """
    Function for converting the temperature value in Celsius to Kelvin.

    Args:
        celsius_input (float): Input with temperature value in Celsius.

    Returns:
        float: Temperature value converted into Kelvin.
    """

    result = celsius_input + 273.15
    return result
