import math

def circumference_circle(rayon):
    return 2*math.pi*rayon

def perimeter_triangle(ab,bc,ca):
    return ab+bc+ca


def perimeter_rectangle(length, width):
    return 2*length + 2*width

# Function to calculate the perimeter of a regular polygon
def regular_polygon_perimeter(side_length, num_sides):
    return num_sides * side_length

# Examples for perimeters of regular polygons:
# Pentagon
def pentagon_perimeter(side_length):
    return regular_polygon_perimeter(side_length, 5)

# Hexagon
def hexagon_perimeter(side_length):
    return regular_polygon_perimeter(side_length, 6)

# Heptagon
def heptagon_perimeter(side_length):
    return regular_polygon_perimeter(side_length, 7)

# Octagon
def octagon_perimeter(side_length):
    return regular_polygon_perimeter(side_length, 8)

# Nonagon
def nonagon_perimeter(side_length):
    return regular_polygon_perimeter(side_length, 9)

# Decagon
def decagon_perimeter(side_length):
    return regular_polygon_perimeter(side_length, 10)