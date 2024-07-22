
# Conversion dictionaries
length_conversion = {
    'm': 1,
    'cm': 0.01,
    'mm': 0.001,
    'km': 1000,
    'inch': 0.0254,
    'foot': 0.3048,
    'yard': 0.9144,
    'mile': 1609.34
}

mass_conversion = {
    'kg': 1,
    'g': 0.001,
    'mg': 1e-6,
    'ton': 1000,
    'lb': 0.453592,
    'ounce': 0.0283495
}

temperature_conversion = {
    'CtoF': lambda c: (c * 9/5) + 32,
    'FtoC': lambda f: (f - 32) * 5/9,
    'CtoK': lambda c: c + 273.15,
    'KtoC': lambda k: k - 273.15,
    'FtoK': lambda f: (f - 32) * 5/9 + 273.15,
    'KtoF': lambda k: (k - 273.15) * 9/5 + 32
}

def convert_units(value, from_unit, to_unit, conversion_dict):
    if from_unit not in conversion_dict or to_unit not in conversion_dict:
        raise ValueError(f"Invalid units: {from_unit} or {to_unit}")
    
    base_value = value * conversion_dict[from_unit]
    converted_value = base_value / conversion_dict[to_unit]
    return converted_value

def convert_temperature(value, from_unit, to_unit):
    conversion_key = f"{from_unit}to{to_unit}"
    if conversion_key not in temperature_conversion:
        raise ValueError(f"Invalid temperature conversion: {from_unit} to {to_unit}")
    
    return temperature_conversion[conversion_key](value)

