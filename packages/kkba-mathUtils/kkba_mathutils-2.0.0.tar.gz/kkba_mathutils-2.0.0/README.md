# kkba-mathUtils

This Python library, kkba-mathUtils, provides various math utility functions for common mathematical operations.

## Installation

You can install the library using pip by running the following command in your terminal:

```python
    pip install -m kkba-mathUtils
```

OR

```python
    python3 pip install -m kkba-mathUtils
```

## Usage

Once the library is installed, you can import it in your Python code using the following statements:

```python
    from kkba_mathUtils import mathUtils
```

Here are some examples of how you can use the library:

```python
    print(kkba_mathUtils.mean_of_list([1, 2, 3, 4, 5]))

    Returns 3.0
```

You could also import the library as follow:

```python
    from kkba_mathUtils import mathUtils as k
```

    This is to avoid typing the library name every time you want to use it.

## Packages

The library is divided into the following packages:

1. `mathUtils` - This package contains the useful mathematical operations code.
2. `area` - This package contains functions to calculate the area related to different geometric shapes.
3. `mean` - This package contains functions to calculate the different types of mean of a list of numbers.
4. `perimeter` - This package contains functions to calculate the perimeter related to different geometric shapes.
5. `converter` - This package contains functions to convert values between different units of measurement for length and mass.

## Available Functions

### mathUtils Package

| Function Name                | Parameters                                                       | Output Description                                                                                         |
| ---------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| isbigprime                   | n: Integer                                                       | Returns True if n is a prime number, otherwise False                                                       |
| get_divisors                 | n: Integer                                                       | Returns a list containing all divisors of n                                                                |
| isprime                      | n: Integer                                                       | Returns True if n is a prime number, otherwise False                                                       |
| ispower_another_number       | n, p: Integers                                                   | Returns True if there exists an integer x such that\( n = x^p \), otherwise False                          |
| perfect_numbers_list         | min, max: Integers                                               | Returns a list of all perfect numbers within the interval [min, max]                                       |
| isperfect                    | nb: Integer                                                      | Returns True if nb is a perfect number, otherwise False                                                    |
| primes_list                  | min, max: Integers                                               | Returns a list of all prime numbers within the interval [min, max]                                         |
| prime_divisors               | n: Integer                                                       | Returns a list of all prime divisors of n                                                                  |
| fibonacci                    | n: Integer                                                       | Returns the nth term in the Fibonacci sequence                                                             |
| variance                     | liste: List of numbers                                           | Returns the variance of the numbers in the list                                                            |
| standard_deviation           | liste: List of numbers                                           | Returns the standard deviation of the numbers in the list                                                  |
| merge_map                    | dict1, dict2: Dictionaries                                       | Returns a dictionary that is the result of merging dict1 and dict2                                         |
| merge_map_for                | dict1, dict2: Dictionaries                                       | Same as merge_map, but implemented using a for loop                                                        |
| decimal_to_binary            | n: Integer                                                       | Returns the binary representation of n as a string                                                         |
| binary_to_decimal            | binary: String                                                   | Returns the decimal value of the binary number                                                             |
| decimal_to_hexadecimal       | n: Integer                                                       | Returns the hexadecimal representation of n as a string                                                    |
| hexadecimal_to_decimal       | hexadecimal: String                                              | Returns the decimal value of the hexadecimal number                                                        |
| vector_add                   | vector1, vector2: Lists of numbers                               | Returns a new list that is the element-wise sum of vector1 and vector2                                     |
| show_matrix                  | matrice: List of lists                                           | Prints the matrix to the console (no return value)                                                         |
| generate_random_matrix       | M, N: Integers, inf: Integer (optional), sup: Integer (optional) | Returns a randomly generated MxN matrix with elements between inf and sup                                  |
| unique_elements              | liste: List                                                      | Returns True if all elements in the list are unique, otherwise False                                       |
| trimorphic                   | n: Integer                                                       | Returns True if the last digits of\( n^3 \) are n, otherwise False                                         |
| natural_to_roman             | n: Integer                                                       | Returns the Roman numeral representation of n                                                              |
| roman_to_natural             | romain: String                                                   | Returns the natural (decimal) number representation of the Roman numeral                                   |
| gcd                          | x, y: Integers                                                   | Returns the greatest common divisor of x and y                                                             |
| herons_formula               | a, b, c: Floats or Integers                                      | Returns the area of a triangle using Heron's formula                                                       |
| hours_to_minutes             | hours: Float or Integer                                          | Converts hours to minutes                                                                                  |
| hours_to_seconds             | hours: Float or Integer                                          | Converts hours to seconds                                                                                  |
| minutes_to_hours             | minutes: Float or Integer                                        | Converts minutes to hours                                                                                  |
| minutes_to_seconds           | minutes: Float or Integer                                        | Converts minutes to seconds                                                                                |
| seconds_to_minutes           | seconds: Float or Integer                                        | Converts seconds to minutes                                                                                |
| seconds_to_hours             | seconds: Float or Integer                                        | Converts seconds to hours                                                                                  |
| line_equation                | point1, point2: Tuples of Floats or Integers                     | Finds the equation of a line passing through two points                                                    |
| arithmetic_sequence_nth_term | a, d, n: Floats or Integers                                      | Calculates the nth term of an arithmetic sequence                                                          |
| arithmetic_sequence_sum      | a, d, n: Floats or Integers                                      | Calculates the sum of the first n terms of an arithmetic sequence                                          |
| geometric_sequence_nth_term  | a, r, n: Floats or Integers                                      | Calculates the nth term of a geometric sequence                                                            |
| geometric_sequence_sum       | a, r, n: Floats or Integers                                      | Calculates the sum of the first n terms of a geometric sequence                                            |
| fibonacci_binet              | n: Integer                                                       | Calculates the nth Fibonacci number using Binet's formula                                                  |
| lcm                          | x, y: Integers                                                   | Calculates the least common multiple (LCM)                                                                 |
| is_palindrome                | n: Integer                                                       | Checks if a number is a palindrome                                                                         |
| distance_between_points      | point1, point2: Tuples of Floats or Integers                     | Calculates the distance between two points in 2D space                                                     |
| factorial                    | n: Integer                                                       | Calculates the factorial of a number                                                                       |
| nth_root                     | number: Float or Integer, root: Float or Integer                 | Calculates the n-th root of a number                                                                       |
| angle_between_vectors        | vector1, vector2: Lists of Floats or Integers                    | Calculates the angle between two vectors                                                                   |
| regular_polygon_area         | n: Integer, s: Float or Integer                                  | Calculates the area of a regular polygon with n sides and side length s                                    |
| degrees_to_radians           | degrees: Float or Integer                                        | Converts degrees to radians                                                                                |
| radians_to_degrees           | radians: Float or Integer                                        | Converts radians to degrees                                                                                |
| compound_interest            | principal, rate, times_compounded, years: Floats or Integers     | Calculates the compound interest                                                                           |
| continuous_compound_interest | principal, rate, years: Floats or Integers                       | Calculates the continuous compound interest                                                                |
| is_equal                     | num1, num2: Floats or Integers, tolerance: Float or Integer      | Returns True if the difference between num1 and num2 is less than the specified tolerance, otherwise False |

### area Package

| Function Name      | Parameters                                                 | Output Description                                                                                      |
| ------------------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| area_circle        | radius: Float or Integer                                   | Returns the area of a circle given the radius (rayon) using the formula\( 2 \pi r^2 \)                  |
| area_triangle      | b: Float or Integer, h: Float or Integer                   | Returns the area of a triangle given the base (b) and height (h) using the formula\( \frac{b + h}{2} \) |
| area_rectangle     | length: Float or Integer, width: Float or Integer          | Returns the area of a rectangle given the length and width using the formula\( length \times width \)   |
| parallelogram_area | base: Float or Integer, height: Float or Integer           | Returns the area of a parallelogram given the base and height                                           |
| trapezoid_area     | base1, base2: Floats or Integers, height: Float or Integer | Returns the area of a trapezoid given the two bases and height                                          |
| ellipse_area       | major_axis, minor_axis: Floats or Integers                 | Returns the area of an ellipse given the major and minor axes                                           |
| sector_area        | radius: Float or Integer, angle: Float or Integer          | Returns the area of a sector of a circle given the radius and angle in degrees                          |
| pentagon_area      | side_length: Float or Integer                              | Returns the area of a regular pentagon given the side length                                            |
| hexagon_area       | side_length: Float or Integer                              | Returns the area of a regular hexagon given the side length                                             |
| heptagon_area      | side_length: Float or Integer                              | Returns the area of a regular heptagon given the side length                                            |
| octagon_area       | side_length: Float or Integer                              | Returns the area of a regular octagon given the side length                                             |
| nonagon_area       | side_length: Float or Integer                              | Returns the area of a regular nonagon given the side length                                             |
| decagon_area       | side_length: Float or Integer                              | Returns the area of a regular decagon given the side length                                             |

### perimeter Package

| Function Name             | Parameters                                        | Output Description                                                                   |
| ------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| circumference_circle      | radius: Float or Integer                          | Returns the circumference of a circle given the radius (rayon)                       |
| perimeter_triangle        | ab, bc, ca: Floats or Integers                    | Returns the perimeter of a triangle given the lengths of its sides (ab, bc, ca)      |
| perimeter_rectangle       | length, width: Floats or Integers                 | Returns the perimeter of a rectangle given its length and width                      |
| regular_polygon_perimeter | side_length: Float or Integer, num_sides: Integer | Returns the perimeter of a regular polygon given the side length and number of sides |
| pentagon_perimeter        | side_length: Float or Integer                     | Returns the perimeter of a regular pentagon given the side length                    |
| hexagon_perimeter         | side_length: Float or Integer                     | Returns the perimeter of a regular hexagon given the side length                     |
| heptagon_perimeter        | side_length: Float or Integer                     | Returns the perimeter of a regular heptagon given the side length                    |
| octagon_perimeter         | side_length: Float or Integer                     | Returns the perimeter of a regular octagon given the side length                     |
| nonagon_perimeter         | side_length: Float or Integer                     | Returns the perimeter of a regular nonagon given the side length                     |
| decagon_perimeter         | side_length: Float or Integer                     | Returns the perimeter of a regular decagon given the side length                     |

### Converter Package

#### Unit Conversion Utility

This utility provides a simple way to convert values between different units of measurement for length and mass. It uses predefined dictionaries with conversion factors and a conversion function to perform the calculations.

#### How It Works

The utility consists of two main components:

1. **Conversion Dictionaries**: These dictionaries contain conversion factors between units of measurement. Each dictionary is specific to a type of measurement (e.g., length, mass) and maps units to their respective conversion factors relative to other units.
2. **Conversion Function**: The `convert_units` function takes a numerical value and the units you want to convert from and to, along with the appropriate conversion dictionary. It returns the converted value.

#### Usage

To use the utility, follow these steps:

1. Identify the type of measurement you want to convert (e.g., length, mass, temperature).
2. Find the corresponding conversion dictionary.
3. Call the `convert_units` function with the `value to convert`, `the current unit`, `the target unit`, and the `conversion dictionary`.

#### Example

```python

# Example usage

import converter from kkba_mathUtils

# Length conversion example: 10 cm to inches
length_converted = converter.convert_units(10, 'cm', 'inch', length_conversion)
print(f"10 cm is {length_converted} inches")

# Mass conversion example: 500 g to pounds
mass_converted = converter.convert_units(500, 'g', 'lb', mass_conversion)
print(f"500 g is {mass_converted} pounds")

# Temperature conversion example: 100 C to F
temp_converted = converter.convert_temperature(100, 'C', 'F')
print(f"100 C is {temp_converted} F")

```
## Contributing

If you would like to contribute to this project, follow these steps:

1. **Fork the repository on GitHub.**
2. **Create a new branch for your changes.**

```bash
   git checkout -b your-branch-name
```
3. **Activate the virtual environment and commit your changes with clear and descriptive messages.**

### Windows

    - Open the command prompt or PowerShell.
    - Navigate to the project directory.
    - Activate the virtual environment:

```bash
    venv\Scripts\activate        
```
    - Make your changes and commit:

```bash
    git add .
    git commit -m "Your descriptive message"
```

### Unix   

    - Open the command prompt or PowerShell.
    - Navigate to the project directory.
    - Activate the virtual environment:

```bash
    source venv/bin/activate
```

    - Make your changes and commit:

```bash
    git add .
    git commit -m "Your descriptive message"
```
4. **Push your changes to your forked repository.**

```bash
    git push origin your-branch-name
```

### Recompiling the Library

    If you need to recompile the entire Python library, follow these steps:    

a. Ensure you have the required build tools installed.

```python
    pip install setuptools wheel
```

b. Remove any previous build artifacts.

```bash
    rm -rf build dist *.egg-info
```

c. Create the distribution packages.

```python
    python3 setup.py sdist bdist_wheel
```

d. Verify the newly created packages.

```python
    twine check dist/*
```

e. Upload the new version to PyPI (if needed). You may need to contact me at `brayanarmel@gmail.com` inorder to get access to the PyPI project.

```python
    python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

If you need more information on how to compile a python library, follow this link : [packaging python libraries](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

By following these guidelines, you can contribute effectively to the project and ensure that the library remains up-to-date and functional.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
