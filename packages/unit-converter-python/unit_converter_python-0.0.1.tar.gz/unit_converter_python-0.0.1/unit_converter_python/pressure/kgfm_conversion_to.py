"""
Code with functions for converting pressure values into Kgf/m²:
1 - Atm
2 - Bar
3 - Pascal
4 - Psi
"""

def kgfm_to_atm(kgfm_input):
    """
    Function for converting the pressure value in Kgf/m² to Atm.

    Args:
        kgfm_input (float): Input with pressure value in Kgf/m².

    Returns:
        float: Pressure value converted into Atm.
    """

    result = kgfm_input * 0.0000967841
    return result

def kgfm_to_bar(kgfm_input):
    """
    Function for converting the pressure value in Kgf/m² to Bar.

    Args:
        kgfm_input (float): Input with pressure value in Kgf/m².

    Returns:
        float: Pressure value converted into Bar.
    """

    result = kgfm_input * 0.0000980665
    return result

def kgfm_to_pa(kgfm_input):
    """
    Function for converting the pressure value in Kgf/m² to Pascal.

    Args:
        kgfm_input (float): Input with pressure value in Kgf/m².

    Returns:
        float: Pressure value converted into Pascal.
    """

    result = kgfm_input * 9.80665205
    return result

def kgfm_to_psi(kgfm_input):
    """
    Function for converting the pressure value in Kgf/m² to Psi.

    Args:
        kgfm_input (float): Input with pressure value in Kgf/m².

    Returns:
        float: Pressure value converted into Psi.
    """

    result = kgfm_input * 0.0014223343
    return result
