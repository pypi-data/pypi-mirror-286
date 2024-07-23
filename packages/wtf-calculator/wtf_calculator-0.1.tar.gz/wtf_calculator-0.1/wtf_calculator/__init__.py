# wtf_calculator/__init__.py

import random

def absurd_add(a, b):
    """Effectue une addition complètement absurde."""
    return random.randint(100000000, 1000000000) + random.randint(100000000, 1000000000)

def absurd_subtract(a, b):
    """Effectue une soustraction complètement absurde."""
    return random.randint(-1000000000, 0) - random.randint(0, 1000000000)

def absurd_multiply(a, b):
    """Effectue une multiplication complètement absurde."""
    return random.randint(1000, 10000) * random.randint(1000, 10000)

def absurd_divide(a, b):
    """Effectue une division complètement absurde."""
    if b == 0:
        return "Infini"  # Division par zéro humoristique
    return random.randint(1, 1000000) / random.randint(1, 10000)
