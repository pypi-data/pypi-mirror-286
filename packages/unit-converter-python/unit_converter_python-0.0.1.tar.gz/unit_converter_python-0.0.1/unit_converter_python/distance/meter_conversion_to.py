"""
Code with functions for converting distance values into Meter for:
1 - Centimeter
2 - Fathom
3 - Feet
4 - Yard
"""

def mt_to_cm(mt_input: float):
    """
    Function for converting the distance value in Meter to Centimeter.

    Args:
        mt_input (float): Input with distance value in Meter.

    Returns:
        float: Distance value converted into Centimeter.
    """

    result = mt_input * 100
    return result

def mt_to_fathom(mt_input: float):
    """
    Function for converting the distance value in Meter to Fathom.

    Args:
        mt_input (float): Input with distance value in Meter.

    Returns:
        float: Distance value converted into Fathom.
    """

    result = mt_input * 0.5468066492
    return result

def mt_to_feet(mt_input: float):
    """
    Function for converting the distance value in Meter to Feet.

    Args:
        mt_input (float): Input with distance value in Meter.

    Returns:
        float: Distance value converted into Feet.
    """

    result = mt_input * 3.280839895
    return result

def mt_to_yard(mt_input: float):
    """
    Function for converting the distance value in Meter to Yard.

    Args:
        mt_input (float): Input with distance value in Meter.

    Returns:
        float: Distance value converted into Yard.
    """

    result = mt_input * 1.0936132983
    return result
