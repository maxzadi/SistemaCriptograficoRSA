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
    
def exponenciacion_modular(n,e,m):
    if e==0:return 1%m
    if e==1:return n%m
    if e%2==0:
        return (exponenciacion_modular(n,(e)//2,m)**2)%m
    else:
        return (n*exponenciacion_modular(n,(e)//2,m)**2)%m