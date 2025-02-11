# Rekurzív függvény: olyan függvény, amely meghívja önmagát
# Hogy egy meglévő problémát, kisebb, részproblémára bontsuk fel

#Faktoriális: 
# n! = n * (n-1)!
# (n-1)! = (n-1)! * (n-2)!
# ...
# 1! = 1
# 0! = 1

# 3! = 3 * 2! = 3 * 2 * 1! = 3 * 2 * 1

def fakt(n):
    if n == 1 or n == 0:
        return 1
    else:
        return n * fakt(n - 1)
    
print(fakt(5))

#Fibonacci sorozat rekurzívan:
# 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
# fib(1) = 1
# fib(2) = 1
# fib(n) = fib(n-1) + fib(n-2)
def fib(n):
    if n < 1:
        return "ERROR"
    elif n == 1 or n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

print(fib(2))
print(fib(8))

# Legyen a(n) sorozat.
# a(1) = 3
# a(2) = 4
# a(n) = a(n-1)^2 + a(n-2) // 2
# **

def a(n):
    if n == 1:
        return 3
    elif n == 2:
        return 4
    else:
        return a(n-1)**2 + a(n-2) // 2
    
print(a(1))
# a(5) = a(4)^2 + a(3)//2
# a(5) = (a(3)^2 + a(2)//2)^2 + a(3)//2
# a(5) = ([a(2)^2 + a(1)//2]^2 + a(2)//2)^2 + [a(2)^2 + a(1)//2]//2
# a(5) = ([4^2 + 3//2]^2 + 4//2)^2 + [4^2 + 3//2]//2
# a(5) = (17^2 + 2)^2 + 8

# a^b = a * a^(b-1)
# 5^3 = 5 * 5^2 = 5* 5 * 5^1 = 5*5*5
def power(a, b):
    if b == 1:
        return a
    if b == 0 and a == 0:
        return "ERROR, 0^0 is not defined"
    if a == 0:
        return 0
    if b == 0:
        return 1
    return a * power(a, b-1)

print(power(5,3))

#Rekurzív föggvénnyel számoljuk ki egy lista elemeinek az összegét
import random
import sys
sys.setrecursionlimit(8000)
lista = [random.randint(-100, 100) for i in range(985)]
lista2 = [random.randint(-100, 100) for i in range(7000)]

def rek_sum(lista):
    if len(lista) == 0:
        return 0
    if len(lista) == 1:
        return lista[0]
    return lista[0] + rek_sum(lista[1:])

print(f"rek_sum(lista) = {rek_sum(lista)}, sum(lista) = {sum(lista)}")
print(f"rek_sum(lista2) = {rek_sum(lista2)}, sum(lista2) = {sum(lista2)}")
#RecursionError: maximum recursion depth exceeded while calling a Python object


