"""
Code with functions for converting distance values into Centimeter for:
1 - Feet
2 - Inch
3 - Milimeter
4 - Yard
"""

def cm_to_ft(cm_input: float):
    """
    Function for converting the distance value in Centimeter to Feet.

    Args:
        cm_input (float): Input with distance value in Centimeter.

    Returns:
        float: Distance value converted into Feet.
    """
    result = cm_input * 0.032808399
    return result

def cm_to_in(cm_input: float):
    """
    Function for converting the distance value in Centimeter to Inch.

    Args:
        cm_input (float): Input with distance value in Centimeter.

    Returns:
        float: Distance value converted into Inch.
    """
    result = cm_input * 0.3937007874
    return result

def cm_to_mm(cm_input: float):
    """
    Function for converting the distance value in Centimeter to Milimeter.

    Args:
        cm_input (float): Input with distance value in Centimeter.

    Returns:
        float: Distance value converted into Milimeter.
    """
    result = cm_input * 10
    return result

def cm_to_yd(cm_input: float):
    """
    Function for converting the distance value in Centimeter to Yard.

    Args:
        cm_input (float): Input with distance value in Centimeter.

    Returns:
        float: Distance value converted into Yard.
    """
    result = cm_input * 0.010936133
    return result
