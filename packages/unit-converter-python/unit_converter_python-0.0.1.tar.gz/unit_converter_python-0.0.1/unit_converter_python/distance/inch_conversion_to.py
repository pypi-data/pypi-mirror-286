"""
Code with functions for converting distance values into Inch for:
1 - Centimeter
2 - Feet
3 - Milimeter
4 - Yard
"""

def inch_to_cm(inch_input: float):
    """
    Function for converting the distance value in Inch to Centimeter.

    Args:
        inch_input (float): Input with distance value in Inch.

    Returns:
        float: Distance value converted into Centimeter.
    """

    result = inch_input * 2.54
    return result

def inch_to_ft(inch_input: float):
    """
    Function for converting the distance value in Inch to Feet.

    Args:
        inch_input (float): Input with distance value in Inch.

    Returns:
        float: Distance value converted into Feet.
    """

    result = inch_input * 0.0833333333
    return result

def inch_to_mm(inch_input: float):
    """
    Function for converting the distance value in Inch to Milimeter.

    Args:
        inch_input (float): Input with distance value in Inch.

    Returns:
        float: Distance value converted into Milimeter.
    """

    result = inch_input * 25.4
    return result

def inch_to_yd(inch_input: float):
    """
    Function for converting the distance value in Inch to Yard.

    Args:
        inch_input (float): Input with distance value in Inch.

    Returns:
        float: Distance value converted into Yard.
    """

    result = inch_input * 0.0277777778
    return result
