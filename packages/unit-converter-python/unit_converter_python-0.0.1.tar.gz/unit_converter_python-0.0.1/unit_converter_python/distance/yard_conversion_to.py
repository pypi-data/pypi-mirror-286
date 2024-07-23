"""
Code with functions for converting distance values into Yard for:
1 - Centimeter
2 - Fathom
3 - Inch
4 - Kilometer
5 - Meter
6 - Mile
"""

def yd_to_cm(yd_input: float):
    """
    Function for converting the distance value in Yard to Centimeter.

    Args:
        yd_input (float): Input with distance value in Yard.

    Returns:
        float: Distance value converted into Centimeter.
    """

    result = yd_input * 91.44
    return result

def yd_to_fathom(yd_input: float):
    """
    Function for converting the distance value in Yard to Fathom.

    Args:
        yd_input (float): Input with distance value in Yard.

    Returns:
        float: Distance value converted into Fathom.
    """

    result = yd_input * 0.5
    return result

def yd_to_inch(yd_input: float):
    """
    Function for converting the distance value in Yard to Inch.

    Args:
        yd_input (float): Input with distance value in Yard.

    Returns:
        float: Distance value converted into Inch.
    """

    result = yd_input * 36
    return result

def yd_to_km(yd_input: float):
    """
    Function for converting the distance value in Yard to Kilometer.

    Args:
        yd_input (float): Input with distance value in Yard.

    Returns:
        float: Distance value converted into Kilometer.
    """

    result = yd_input * 0.0009144
    return result

def yd_to_mt(yd_input: float):
    """
    Function for converting the distance value in Yard to Meter.

    Args:
        yd_input (float): Input with distance value in Yard.

    Returns:
        float: Distance value converted into Meter.
    """

    result = yd_input * 0.9144
    return result

def yd_to_mi(yd_input: float):
    """
    Function for converting the distance value in Yard to Mile.

    Args:
        yd_input (float): Input with distance value in Yard.

    Returns:
        float: Distance value converted into Mile.
    """

    result = yd_input * 0.0005681818
    return result
