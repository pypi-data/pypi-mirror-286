"""
Code with functions for converting weight values into Gram for:
1 - Kilogram
2 - Ounce
3 - Pound
"""

def gram_to_kg(grams_input: float):
    """
    Function for converting the weight value in Gram to Kilogram.

    Args:
        grams_input (float): Input with weight value in Grams.

    Returns:
        float: Weight value converted into Kilograms.
    """

    result = grams_input * 0.001
    return result

def gram_to_ounce(grams_input: float):
    """
    Function for converting the weight value in Gram to Ounce.

    Args:
        grams_input (float): Input with weight value in Grams.

    Returns:
        float: Weight value converted into Ounce.
    """

    result = grams_input * 0.03527396195
    return result

def gram_to_lb(grams_input: float):
    """
    Function for converting the weight value in Gram to Pound.

    Args:
        grams_input (float): Input with weight value in Grams.

    Returns:
        float: Weight value converted into Pounds.
    """

    result = grams_input * 0.002204622622
    return result
