import math

def mean_of_list(list):
    return (1/len(list)) * sum(list)

def harmonic_mean(list):
    sum_liste = 0
    for num in list:
        sum_liste += (1/num)
        
    return len(list) / sum_liste

def geometric(liste):
    """Renvoie la moyenne géométrique des éléments d'une liste"""
    product_list = 1
    for nb in liste:
        product_list *= nb

    return product_list**(1/len(liste))

def quadratic(liste):
    """Renvoie la moyenne quadratique des éléments d'une liste"""
    sum_liste = 0
    for nb in liste:
        sum_liste += nb**2
    return math.sqrt(sum_liste/len(liste))


