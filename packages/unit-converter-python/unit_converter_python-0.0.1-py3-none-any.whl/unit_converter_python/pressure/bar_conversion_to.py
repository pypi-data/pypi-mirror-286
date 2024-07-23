"""
Code with functions for converting pressure values into Bar for:
1 - Atm
2 - Kgf/m²
3 - Pascal
4 - Psi
"""

def bar_to_atm(bar_input: float):
    """
    Function for converting the pressure value in Bar to Atm.

    Args:
        bar_input (float): Input with pressure value in Bar.

    Returns:
        _type_: Pressure value converted into Atm.
    """

    result = bar_input * 0.9869233
    return result

def bar_to_kgfm(bar_input: float):
    """
    Function for converting the pressure value in Bar to Kgf/m².

    Args:
        bar_input (float): Input with pressure value in Bar.

    Returns:
        _type_: Pressure value converted into Kgf/m².
    """

    result = bar_input * 10197.16
    return result

def bar_to_pa(bar_input: float):
    """
    Function for converting the pressure value in Bar to Pascal.

    Args:
        bar_input (float): Input with pressure value in Bar.

    Returns:
        _type_: Pressure value converted into Pascal.
    """

    result = bar_input * 100000
    return result

def bar_to_psi(bar_input: float):
    """
    Function for converting the pressure value in Bar to Psi.

    Args:
        bar_input (float): Input with pressure value in Bar.

    Returns:
        _type_: Pressure value converted into Psi.
    """

    result = bar_input * 14.50377
    return result
