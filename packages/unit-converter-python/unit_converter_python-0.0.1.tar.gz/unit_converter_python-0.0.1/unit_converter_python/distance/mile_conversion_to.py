"""
Code with functions for converting distance values into Mile for:
1 - Centimeter
2 - Fathom
3 - Inch
4 - Kilometer
5 - Meter
6 - Yard
"""

def mi_to_cm(mi_input: float):
    """
    Function for converting the distance value in Mile to Centimeter.

    Args:
        mi_input (float): Input with distance value in Mile.

    Returns:
        float: Distance value converted into Centimeter.
    """

    result = mi_input * 160934.4
    return result

def mi_to_fathom(mi_input: float):
    """
    Function for converting the distance value in Mile to Fathom.

    Args:
        mi_input (float): Input with distance value in Mile.

    Returns:
        float: Distance value converted into Fathom.
    """

    result = mi_input * 880
    return result

def mi_to_inch(mi_input: float):
    """
    Function for converting the distance value in Mile to Inch.

    Args:
        mi_input (float): Input with distance value in Mile.

    Returns:
        float: Distance value converted into Inch.
    """

    result = mi_input * 63360
    return result

def mi_to_km(mi_input: float):
    """
    Function for converting the distance value in Mile to Kilometer.

    Args:
        mi_input (float): Input with distance value in Mile.

    Returns:
        float: Distance value converted into Kilometer.
    """

    result = mi_input * 1.609344
    return result

def mi_to_mt(mi_input: float):
    """
    Function for converting the distance value in Mile to Meter.

    Args:
        mi_input (float): Input with distance value in Mile.

    Returns:
        float: Distance value converted into Meter.
    """

    result = mi_input * 1609.344
    return result

def mi_to_yd(mi_input: float):
    """
    Function for converting the distance value in Mile to Yard.

    Args:
        mi_input (float): Input with distance value in Mile.

    Returns:
        float: Distance value converted into Yard.
    """

    result = mi_input * 1760
    return result
