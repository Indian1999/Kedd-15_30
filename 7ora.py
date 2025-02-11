# yield függvények
# yield - olyan mint a return, csak nem állítja le a függvényt

def f_return():
    return "cica"
    print("returned cica")

print(f_return())

#Generator objektum
def f_yield():
    yield "cica"
    print("yielded cica")

print(f_yield())

def one_to_five():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5

for i in range(5):
    print(i)

for i in one_to_five():
    print(i, end = ", ")
print()

#Mértani sorozatok:
# a1 = 3; q = 2
# 3; 6; 12; 24; 48; 96;
# a2 = a1 * q
# a3 = a1 * q * q = a1 * q^2
# an = a1 * q^(n-1)
def mértani_range(an, a1 = 1, q = 2):
    while a1 < an:
        yield a1
        a1 *= q

print([i for i in mértani_range(1025)]) # mértani_range(1025, 1, 2)
print([i for i in mértani_range(1025, 3, 3)])

#for i in range(10): # Generátort, ami felsorolja a számokat 0-tól 9-ig

def myRange(upperBound, lowerBound = 0, step = 1):
    while lowerBound < upperBound:
        yield lowerBound
        lowerBound += step

print([i for i in myRange(10)])
print([i for i in myRange(100, 20, 10)])
"""
Függvények mintaillesztése nem működik pythonban, de hasznos megjegyezni, mert c, c++, java, stb. nyelveken használható
def myRange2(upperBound):
    i = 0
    while i < upperBound:
        yield i
        i += 1

def myRange2(lowerBound, upperBound):
    i = lowerBound
    while i < upperBound:
        yield i
        i += 1

def myRange2(lowerBound, upperBound, step):
    i = lowerBound
    while i < upperBound:
        yield i
        i += step

print([i for i in myRange2(10)])
print([i for i in myRange2(2,15)])
print([i for i in myRange2(100,1000, 50)])
"""

# Írjunk egy generátort ami a fibonacci számokat adja vissza
def fib(n):
    a, b = 1, 1 
    # 2. futáskor a = 1, b = 2      3.nál: a = 2, b = 3,       a = 3, b = 5
    for i in range(n):
        yield a
        a, b = b, a + b
    
print([i for i in fib(20)])

fib_gen = fib(10)
print(next(fib_gen))
print(next(fib_gen))

def squared_numbers():
    i = 1
    while True:
        yield i*i
        i += 1

myGenerator = squared_numbers()
for i in range(40):
    print(next(myGenerator), end = " ")
print()

myGenerator = squared_numbers()
print([next(myGenerator) for i in range(20)])

# Írjunk egy generátort, ami a harmónikus sor elemeit generálja le
# 1/1; 1/2; 1/3; 1/4; 1/5; ...

#Írjunk egy generátort, ami x db random számot generál, lehessen azt is megadni opcionálisan, hogy mekkora tartományból legyen kiválasztva a random számok, ha nem adunk meg semmit, akkor alapból a [0,1) tartományból generálunk számokat

import random
def random_nums(n, lowerBound = None, upperBound = None):
    if lowerBound == None and upperBound != None or lowerBound != None and upperBound == None:
        raise Exception("You have to provide both bounds!")
    if lowerBound == None and upperBound == None:
        for i in range(n):
            yield random.random() # 0 és 1 között random
    else:
        for i in range(n):
            yield random.randint(lowerBound, upperBound)

print([round(i, 2) for i in random_nums(10)])
print([i for i in random_nums(10, 1, 10)])
#print([i for i in random_nums(10, -10)]) HIBA
    

# Írjunk egy generátort ami egy megnyitott file sorait adogatja vissza

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for row in f:
            yield row.strip()

for sor in read_file("car_data.txt"):
    print(sor)


# Írjunk egy függvényt, ami az aktuális időt adja vissza 1 mp-ként
import time
import datetime

def time_generator():
    while True:
        yield datetime.datetime.now().strftime("%H:%M:%S")
        time.sleep(1)

for timestamp in time_generator():
    print(timestamp)
