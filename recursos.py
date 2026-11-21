from math import isqrt

def es_primo(n):
    if n < 2:
        return False

    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return False

    return True

def mcd(a,b):
    if b == 0:
        return abs(a)
    
    r=a%b
    if r==0:
        return b
    return mcd(b,r)

def euclides_extendido(a, b):
    if b == 0:
        return a, 1, 0

    mcd, x1, y1 = euclides_extendido(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return mcd, x, y


def inverso_modular(n, m):
    if m <= 1:
        raise ValueError("El módulo debe ser mayor que 1.")

    mcd, x, _ = euclides_extendido(n, m)

    if mcd != 1:
        raise ValueError("No existe inverso modular: n y m no son primos relativos.")

    return x % m
    
def exponenciacion_modular(n, e, m):
    """Calcula n elevado a e modulo m mediante cuadrados sucesivos."""
    if e < 0:
        raise ValueError("El exponente debe ser no negativo.")
    if m <= 0:
        raise ValueError("El módulo debe ser mayor que cero.")

    resultado = 1 % m
    base = n % m

    # Un ciclo evita el límite de recursión para exponentes grandes.
    while e > 0:
        if e % 2 == 1:
            resultado = (resultado * base) % m
        base = (base * base) % m
        e //= 2

    return resultado
