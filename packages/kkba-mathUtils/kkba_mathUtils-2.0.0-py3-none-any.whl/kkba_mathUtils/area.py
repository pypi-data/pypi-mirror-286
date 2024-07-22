import math

def area_circle(rayon):
    return 2*math.pi*rayon**2

def area_triangle(b, h):
    return (b+h)/2

def area_rectangle(lenght, width):
    return lenght*width

def parallelogram_area(base, height):
    return base * height

# Function to calculate the area of a trapezoid
def trapezoid_area(base1, base2, height):
    return 0.5 * (base1 + base2) * height

# Function to calculate the area of an ellipse
def ellipse_area(major_axis, minor_axis):
    return math.pi * major_axis * minor_axis

# Function to calculate the area of a sector of a circle
def sector_area(radius, angle):
    return (angle / 360) * math.pi * (radius ** 2)

# Function to calculate the area of a regular pentagon
def pentagon_area(side_length):
    return (5 * side_length ** 2) / (4 * math.tan(math.pi / 5))

# Function to calculate the area of a regular hexagon
def hexagon_area(side_length):
    return (3 * math.sqrt(3) * side_length ** 2) / 2

# Function to calculate the area of a regular heptagon
def heptagon_area(side_length):
    return (7 * side_length ** 2) / (4 * math.tan(math.pi / 7))

# Function to calculate the area of a regular octagon
def octagon_area(side_length):
    return (2 * (1 + math.sqrt(2)) * side_length ** 2)

# Function to calculate the area of a regular nonagon
def nonagon_area(side_length):
    return (9 * side_length ** 2) / (4 * math.tan(math.pi / 9))

# Function to calculate the area of a regular decagon
def decagon_area(side_length):
    return (5 * (5 + 2 * math.sqrt(5)) * side_length ** 2) / 4

