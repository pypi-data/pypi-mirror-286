"""
Code with functions for converting temperature values into Kelvin for:
1 - Celsius
2 - Fahrenheit
"""

def k_to_c(kelvin_input: float):
    """
    Function for converting the temperature value in Kelvin to Celsius.

    Args:
        kelvin_input (float): Input with temperature value in Kelvin.

    Returns:
        float: Temperature value converted into Celsius.
    """

    result = kelvin_input - 273.15
    return result

def k_to_f(kelvin_input: float):
    """
    Function for converting the temperature value in Kelvin to Fahrenheit.

    Args:
        kelvin_input (float): Input with temperature value in Kelvin.

    Returns:
        float: Temperature value converted into Fahrenheit.
    """

    result = (kelvin_input * (9/5)) - 459.67
    return result
