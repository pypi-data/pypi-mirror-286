"""
Code with functions for converting pressure values into Psi for:
1 - Atm
2 - Bar
3 - Kgf/m²
4 - Pascal
"""

def psi_to_atm(psi_input: float):
    """
    Function for converting the pressure value in Psi to Atm.

    Args:
        psi_input (float): Input with pressure value in Psi.

    Returns:
        float: Pressure value converted into Atm.
    """

    result = psi_input * 0.06804598
    return result

def psi_to_bar(psi_input: float):
    """
    Function for converting the pressure value in Psi to Bar.

    Args:
        psi_input (float): Input with pressure value in Psi.

    Returns:
        float: Pressure value converted into Bar.
    """

    result = psi_input * 0.06894759
    return result

def psi_to_kgfm(psi_input: float):
    """
    Function for converting the pressure value in Psi to Kgf/m².

    Args:
        psi_input (float): Input with pressure value in Psi.

    Returns:
        float: Pressure value converted into Kgf/m².
    """

    result = psi_input * 703.06961569
    return result

def psi_to_pa(psi_input: float):
    """
    Function for converting the pressure value in Psi to Pascal.

    Args:
        psi_input (float): Input with pressure value in Psi.

    Returns:
        float: Pressure value converted into Pascal.
    """

    result = psi_input * 6894.7590868
    return result
