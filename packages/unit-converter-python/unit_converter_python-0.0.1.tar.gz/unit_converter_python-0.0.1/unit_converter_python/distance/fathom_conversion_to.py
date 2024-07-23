"""
Code with functions for converting distance values into Fathom for:
1 - Centimeter
2 - Inch
3 - Kilometer
4 - Meter
5 - Mile
6 - Yard
"""

def fathom_to_cm(fathom_input: float):
    """
    Function for converting the distance value in Fathom to Centimeter.

    Args:
        fathom_input (float): Input with distance value in Fathom.

    Returns:
        float: Distance value converted into Centimeter.
    """

    result = fathom_input * 182.88
    return result

def fathom_to_inch(fathom_input: float):
    """
    Function for converting the distance value in Fathom to Inch.

    Args:
        fathom_input (float): Input with distance value in Fathom.

    Returns:
        float: Distance value converted into Inch.
    """

    result = fathom_input * 72
    return result

def fathom_to_km(fathom_input: float):
    """
    Function for converting the distance value in Fathom to Kilometer.

    Args:
        fathom_input (float): Input with distance value in Fathom.

    Returns:
        float: Distance value converted into Kilometer.
    """

    result = fathom_input * 0.0018288
    return result

def fathom_to_mt(fathom_input: float):
    """
    Function for converting the distance value in Fathom to Meter.

    Args:
        fathom_input (float): Input with distance value in Fathom.

    Returns:
        float: Distance value converted into Meter.
    """

    result = fathom_input * 1.8288
    return result

def fathom_to_mi(fathom_input: float):
    """
    Function for converting the distance value in Fathom to Mile.

    Args:
        fathom_input (float): Input with distance value in Fathom.

    Returns:
        float: Distance value converted into Mile.
    """

    result = fathom_input * 0.0011363636
    return result

def fathom_to_yd(fathom_input: float):
    """
    Function for converting the distance value in Fathom to Yard.

    Args:
        fathom_input (float): Input with distance value in Fathom.

    Returns:
        float: Distance value converted into Yard.
    """

    result = fathom_input * 2
    return result
