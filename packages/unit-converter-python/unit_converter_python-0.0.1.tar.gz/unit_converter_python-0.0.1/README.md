# Unit Converter

This project is a simple unit converter.
In this first version it will be possible to convert units related to distance, pressure, temperature and weight.

The package unit_converter_python is used to:
	- Distance conversion:
		- centimeter
		- fathom
		- feet
		- inch
		- kilometer
		- meters
		- mile
		- yard

	- Pressure Conversion:
		- atm
		- bar
		- kgf/m²
		- pascal
		- psi

	- Temperature Conversion:
		- Celsius
		- Fahrenheit
		- Kelvin

	- Weight Conversion:
		- Gram
		- Kilogram
		- Ounce
		- Pound

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install unit_converter_python

```bash
pip install unit_converter_python
```

## Usage

Here we have an example of use converting a temperature measurement from Fahrenheit to Celsius.

### Step 1
Import the desired package.

```python
from unit_converter_python.temperature import fahrenheit_conversion_to
```

### Step 2
Use the function to convert the value from Fahrenheit to Celsius.

Example:
```python
fahrenheit_value = 62
converted_value = fahrenheit_conversion_to.f_to_c(fahrenheit_value)
print(f"The temperature of {fahrenheit_value}ºF was converted to {converted_value:.2F}ºC.")
```

## Author
Daniel Torres de Andrade

## License
[MIT](https://choosealicense.com/licenses/mit/)
