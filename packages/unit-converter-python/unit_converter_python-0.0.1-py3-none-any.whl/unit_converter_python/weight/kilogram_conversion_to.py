"""
Code with functions for converting weight values into Kilogram for:
1 - Gram
2 - Ounce
3 - Pound
"""

def kg_to_gr(kg_input: float):
    """
    Function for converting the weight value in Kilogram to Gram.

    Args:
        kg_input (float): Input with weight value in Kilograms.

    Returns:
        float: Weight value converted into Grams.
    """

    result = kg_input * 1000
    return result

def kg_to_ounce(kg_input: float):
    """
    Function for converting the weight value in Kilogram to Ounce.

    Args:
        kg_input (float): Input with weight value in Kilograms.

    Returns:
        float: Weight value converted into Ounces.
    """

    result = kg_input * 35.27396195
    return result

def kg_to_pound(kg_input: float):
    """
    Function for converting the weight value in Kilogram to Pound.

    Args:
        kg_input (float): Input with weight value in Kilograms.

    Returns:
        float: Weight value converted into Pounds.
    """

    result = kg_input * 2.2046226218
    return result
