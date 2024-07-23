"""
Code with functions for converting weight values into Ounce for:
1 - Gram
2 - Kilogram
3 - Pound
"""

def ounce_to_gr(ounce_input: float):
    """
    Function for converting the weight value in Ounce to Gram.

    Args:
        ounce_input (float): Input with weight value in Ounces.

    Returns:
        float: Weight value converted into Grams.
    """

    result = ounce_input * 28.349523125
    return result

def ounce_to_kg(ounce_input: float):
    """
    Function for converting the weight value in Ounce to Kilogram.

    Args:
        ounce_input (float): Input with weight value in Ounces.

    Returns:
        float: Weight value converted into Kilograms.
    """

    result = ounce_input * 0.028349523125
    return result

def ounce_to_lb(ounce_input: float):
    """
    Function for converting the weight value in Ounce to Pound.

    Args:
        ounce_input (float): Input with weight value in Ounces.

    Returns:
        float: Weight value converted into Pounds.
    """

    result = ounce_input * 0.0625
    return result
