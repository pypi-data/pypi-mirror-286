"""
Code with functions for converting distance values into Feet for:
1 - Centimeter
2 - Fathom
3 - Inch
4 - Meter
5 - Yard
"""

def ft_to_cm(feet_input: float):
    """
    Function for converting the distance value in Feet to Centimeter.

    Args:
        feet_input (float): Input with distance value in Feet.

    Returns:
        float: Distance value converted into Centimeter.
    """

    result = feet_input * 30.48
    return result

def ft_to_fathom(feet_input: float):
    """
    Function for converting the distance value in Feet to Fathom.

    Args:
        feet_input (float): Input with distance value in Feet.

    Returns:
        float: Distance value converted into Fathom.
    """

    result = feet_input * 0.1666666667
    return result

def ft_to_inch(feet_input: float):
    """
    Function for converting the distance value in Feet to Inch.

    Args:
        feet_input (float): Input with distance value in Feet.

    Returns:
        float: Distance value converted into Inch.
    """

    result = feet_input * 12
    return result

def ft_to_mt(feet_input: float):
    """
    Function for converting the distance value in Feet to Meter.

    Args:
        feet_input (float): Input with distance value in Feet.

    Returns:
        float: Distance value converted into Meter.
    """

    result = feet_input * 0.3048
    return result

def ft_to_yd(feet_input: float):
    """
    Function for converting the distance value in Feet to Yard.

    Args:
        feet_input (float): Input with distance value in Feet.

    Returns:
        float: Distance value converted into Yard.
    """

    result = feet_input * 0.3333333333
    return result
