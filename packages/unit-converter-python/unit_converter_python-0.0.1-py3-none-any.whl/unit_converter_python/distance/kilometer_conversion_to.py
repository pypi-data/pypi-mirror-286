"""
Code with functions for converting distance values into Kilometer for:
1 - Fathom
2 - Meter
3 - Mile
4 - Sea Mile
5 - Yard
"""

def km_to_fathom(km_input: float):
    """
    Function for converting the distance value in Kilometer to Fathom.

    Args:
        km_input (float): Input with distance value in Kilometer.

    Returns:
        float: Distance value converted into Fathom.
    """

    result = km_input * 546.80664917
    return result

def km_to_meter(km_input: float):
    """
    Function for converting the distance value in Kilometer to Meter.

    Args:
        km_input (float): Input with distance value in Kilometer.

    Returns:
        float: Distance value converted into Meter.
    """

    result = km_input * 1000
    return result

def km_to_mile(km_input: float):
    """
    Function for converting the distance value in Kilometer to Mile.

    Args:
        km_input (float): Input with distance value in Kilometer.

    Returns:
        float: Distance value converted into Mile.
    """

    result = km_input * 0.6213711922
    return result

def km_to_seamile(km_input: float):
    """
    Function for converting the distance value in Kilometer to Sea Mile.

    Args:
        km_input (float): Input with distance value in Kilometer.

    Returns:
        float: Distance value converted into Sea Mile.
    """

    result = km_input * 0.5399568035
    return result

def km_to_yard(km_input: float):
    """
    Function for converting the distance value in Kilometer to Yard.

    Args:
        km_input (float): Input with distance value in Kilometer.

    Returns:
        float: Distance value converted into Yard.
    """

    result = km_input * 1093.6132983
    return result
