"""
Code with functions for converting distance values into Atm for:
1 - Bar
2 - Kgf/m²
3 - Pascal
4 - Psi
"""

def atm_to_bar(atm_input: float):
    """
    Function for converting the pressure value in Atm to Bar.

    Args:
        atm_input (float): Input with pressure value in Atm.

    Returns:
        float: Pressure value converted into Bar.
    """

    result = atm_input * 1.01324997
    return result

def atm_to_kgfm(atm_input: float):
    """
    Function for converting the pressure value in Atm to Kgf/m².

    Args:
        atm_input (float): Input with pressure value in Atm

    Returns:
        float: Pressure value converted into Kgf/m².
    """

    result = atm_input * 1.03322720
    return result

def atm_to_pa(atm_input: float):
    """
    Function for converting the pressure value in Atm to Pascal.

    Args:
        atm_input (float): Input with pressure value in Atm

    Returns:
        float: Pressure value converted into Pascal.
    """

    result = atm_input * 101324.99658
    return result

def atm_to_psi(atm_input: float):
    """
    Function for converting the pressure value in Atm to Psi.

    Args:
        atm_input (float): Input with pressure value in Atm

    Returns:
        float: Pressure value converted into Psi.
    """

    result = atm_input * 14.69594446
    return result
