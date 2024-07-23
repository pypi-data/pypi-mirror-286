"""
Code with functions for converting weight values into Pound for:
1 - Grams
2 - Kilogram
3 - Ounce
"""

def lb_to_gr(lb_input: float):
    """
    Function for converting the weight value in Pound to Gram.

    Args:
        lb_input (float): Input with weight value in Pounds.

    Returns:
        _type_: Weight value converted into Grams.
    """

    result = lb_input * 453.59237
    return result

def lb_to_kg(lb_input: float):
    """
    Function for converting the weight value in Pound to Kilogram.

    Args:
        lb_input (float): Input with weight value in Pounds.

    Returns:
        _type_: Weight value converted into Kilograms.
    """

    result = lb_input * 0.45359237
    return result

def lb_to_ounce(lb_input: float):
    """
    Function for converting the weight value in Pound to Ounce.

    Args:
        lb_input (float): Input with weight value in Pounds.

    Returns:
        _type_: Weight value converted into Ounces.
    """

    result = lb_input * 16
    return result
