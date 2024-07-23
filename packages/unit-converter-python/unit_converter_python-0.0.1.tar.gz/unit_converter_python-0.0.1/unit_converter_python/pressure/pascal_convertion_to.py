"""
Code with functions for converting pressure values into Pascal for:
1 - Atm
2 - Bar
3 - Kgf/m²
4 - Psi
"""

def pascal_to_atm(pa_input: float):
    """
    Function for converting the pressure value in Pascal to Atm.

    Args:
        pa_input (float): Input with pressure value in Pascal.

    Returns:
        float: Pressure value converted into Atm.
    """

    result = pa_input * 0.000009869233
    return result

def pascal_to_bar(pa_input: float):
    """
    Function for converting the pressure value in Pascal to Bar.

    Args:
        pa_input (float): Input with pressure value in Pascal.

    Returns:
        float: Pressure value converted into Bar.
    """

    result = pa_input * 0.00001
    return result

def pascal_to_kgfm(pa_input: float):
    """
    Function for converting the pressure value in Pascal to Kgf/m².

    Args:
        pa_input (float): Input with pressure value in Pascal.

    Returns:
        float: Pressure value converted into Kgf/m².
    """

    result = pa_input * 0.1019716
    return result

def pascal_to_psi(pa_input: float):
    """
    Function for converting the pressure value in Pascal to Psi.

    Args:
        pa_input (float): Input with pressure value in Pascal.

    Returns:
        float: Pressure value converted into Psi.
    """

    result = pa_input * 0.0001450377
    return result
