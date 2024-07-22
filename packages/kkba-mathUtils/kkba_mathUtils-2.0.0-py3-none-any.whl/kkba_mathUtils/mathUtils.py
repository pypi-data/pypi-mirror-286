import math
from mean import mean_of_list

def isbigprime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_divisors(n):
    dividers_list = []
    for divider in range(1, n+1):
        if n % divider == 0:
            dividers_list.append(divider)

    return dividers_list

def isprime(n):
    for d in range(2,n):
        if n % d == 0:
            return False
    return True

def ispower_another_number(n,p):
    for i in range(1, n):
        if i**p > n:
            return False
        elif i**p == n:
            return True
        
def perfect_numbers_list(min, max):
    perfect_numbers_list = []
    for n in range(min, max+1):
        if isperfect(n):
            perfect_numbers_list.append(n)
    return perfect_numbers_list

def isperfect(nb):
    print(get_divisors(28))
    if sum(get_divisors(nb)[:-1]) == nb:
        return True
    else:
        return False

def primes_list(min, max):
    primes_list = []
    for num in range(min, max+1):
        if isprime(num):
            primes_list.append(num)
    return primes_list

def prime_divisors(n):
    dividers_prime_list = []
    for divider in get_divisors(n):
        if isprime(divider):
            dividers_prime_list.append(divider)

    return dividers_prime_list

def fibonacci(n):

    if n==1 or n==2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
def variance(liste):
    moy = mean_of_list(liste)
    var = 0

    for nb in liste:
        var += (nb - moy)**2

    return var / len(liste)



def standard_deviation(liste):
    moy = mean_of_list(liste)
    var = 0
    for nb in liste:
        var += (nb - moy)**2

    return math.sqrt(var/len(liste))

def merge_map(dict1, dict2):
    
    final_dict = dict1.copy()
    final_dict.update(dict2)
    return final_dict



def merge_map_for(dict1, dict2):

    final_dict = dict()
    for dictionnaire in [dict1,dict2]:
        for key, value in dictionnaire.items():
            final_dict[key] = value

    return final_dict

def decimal_to_binary(n):
    
    binary = ""
    while n > 0 :
        binary = str(n%2) + binary
        n = n // 2

    return binary

def binary_to_decimal(binary):
    
    if "0b" in binary:
        binary = binary.replace("0b", "")
        
    total = 0
    for i, bit in enumerate(binary[::-1]):
        total += int(bit) * 2**i

    return total

def decimal_to_hexadecimal(n):
    hexadecimal = ""
    hexa_values = {"0" : "0", "1" : "1", "2" : "2", "3" : "3", "4" : "4", "5" : "5", "6" : "6",
            "7" : "7", "8" : "8", "9" : "9", "10" : "A", "11" : "B", "12" : "C",
            "13" : "D", "14" : "E", "15" : "F"}

    while n > 0:
        hexadecimal = hexa_values[str(n%16)] + hexadecimal
        n = n // 16

    return hexadecimal

def hexadecimal_to_decimal(hexadecimal):
    
    hexa_values = {"0" : 0, "1" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6,
                   "7" : 7, "8" : 8, "9" : 9 , "A" : 10, "B" : 11, "C" : 12,
                   "D" : 13, "E" : 14, "F" : 15}

    if "0x" in hexadecimal:
        hexadecimal = hexadecimal.replace("0x", "")

    hexadecimal = hexadecimal.upper()
    total = 0
    for i, digit in enumerate(hexadecimal[::-1]):
        total += hexa_values[digit] * 16**i

    return total

def vector_add(vector1, vector2):
    
    if len(vector1) != len(vector2):
        return None
    
    new_vector = list()
    for i in range(len(vector1)):
        new_vector.append(vector1[i] + vector2[i])

    return new_vector

def show_matrix(matrice):
    """Affiche la matrice dans la console"""
    
    for line in matrice:
        print(line)

        

def generate_random_matrix(M, N, inf=1, sup=100):
    
    matrix = []

    for i in range(M):
        line = []
        for j in range(N):
            line.append(math.randint(inf, sup))
        matrix.append(line)

    return matrix


def unique_elements(liste):
    if len(liste) == len(list(set(liste))):
        return True

    else:
        return False
    
def trimorphic(n):
    return str(n**3).endswith(str(n))

def natural_to_roman(n):
    int_rom = [(1000, "M"),
               (900, "CM"),
               (500, "D"),
               (400, "CD"),
               (100, "C"),
               (90, "XC"),
               (50, "L"),
               (40, "XL"),
               (10, "X"),
               (9, "IX"),
               (5, "V"),
               (4, "IV"),
               (1, "I")]

    romain = []

    for i, num in int_rom:
        while n >= i:
            n -= i
            #print(n)
            romain.append(num)

    return "".join(romain)

def roman_to_natural(romain):
    
    double = {"CM" : 900, "CD" : 400, "XC" : 90, "XL" : 40, "IX" : 9, "IV" : 4}
    unique = {"M" : 1000, "D" : 500, "C" : 100, "L" : 50, "X" : 10, "V" : 5, "I" : 1}

    entier = 0
    i = 0

    #Tant qu'on a pas parcouru le nombre romain en entier
    while i < len(romain):
        if i < len(romain) - 1 and romain[i:i+2] in double:
            entier += double[romain[i:i+2]]
            i += 2
        else:
            entier += unique[romain[i]]
            i += 1
    return entier

def gcd(x,y):
    
    if x < y:
        x, y = y, x

    if x % y == 0:
        return y

    for k in range(y//2, 0, -1):
        if x % k == 0 and y % k == 0:
            return k


# Function to calculate the area of a triangle using Heron's formula
def herons_formula(a, b, c):
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area


def hours_to_minutes(hours):
    return hours * 60

def hours_to_seconds(hours):
    return hours * 3600

# Function to convert minutes to hours
def minutes_to_hours(minutes):
    return minutes / 60

# Function to convert minutes to seconds
def minutes_to_seconds(minutes):
    return minutes * 60

def seconds_to_minutes(seconds):
    return seconds / 60

def seconds_to_hours(seconds):
    return seconds / 3600

# Function to find the equation of a line passing through two points
def line_equation(point1, point2):
    (x1, y1), (x2, y2) = point1, point2
    m = (y2 - y1) / (x2 - x1)  # slope of the line
    b = y1 - m * x1  # y-intercept
    return f"y = {m}x + {b}"

# Function to calculate the nth term of an arithmetic sequence
def arithmetic_sequence_nth_term(a, d, n):
    return a + (n - 1) * d

# Function to calculate the sum of the first n terms of an arithmetic sequence
def arithmetic_sequence_sum(a, d, n):
    return n / 2 * (2 * a + (n - 1) * d)

# Function to calculate the nth term of a geometric sequence
def geometric_sequence_nth_term(a, r, n):
    return a * r ** (n - 1)

# Function to calculate the sum of the first n terms of a geometric sequence
def geometric_sequence_sum(a, r, n):
    if r == 1:
        return a * n
    else:
        return a * (1 - r ** n) / (1 - r)

# Function to calculate the nth Fibonacci number using Binet's formula
def fibonacci_binet(n):
    phi = (1 + math.sqrt(5)) / 2
    return round((phi ** n - (-1 / phi) ** n) / math.sqrt(5))

# Function to calculate the least common multiple (LCM)
def lcm(x, y):
    return abs(x * y) // gcd_euclid(x, y)

# Function to check if a number is a palindrome
def is_palindrome(n):
    return str(n) == str(n)[::-1]

# Function to calculate the distance between two points in 2D space
def distance_between_points(point1, point2):
    (x1, y1), (x2, y2) = point1, point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to calculate the factorial of a number
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# Function to calculate the n-th root of a number
def nth_root(number, root):
    return number ** (1 / root)

# Function to calculate the angle between two vectors
def angle_between_vectors(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vector1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vector2))
    return math.acos(dot_product / (magnitude1 * magnitude2))

# Function to calculate the area of a regular polygon with n sides and side length s
def regular_polygon_area(n, s):
    return (n * s ** 2) / (4 * math.tan(math.pi / n))

# Function to convert degrees to radians
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

# Function to convert radians to degrees
def radians_to_degrees(radians):
    return radians * (180 / math.pi)

# Function to calculate the compound interest
def compound_interest(principal, rate, times_compounded, years):
    return principal * (1 + rate / times_compounded) ** (times_compounded * years)

# Function to calculate the continuous compound interest
def continuous_compound_interest(principal, rate, years):
    return principal * math.exp(rate * years)

def is_equal(num1, num2, tolerance):
    return abs(num1 - num2) < tolerance