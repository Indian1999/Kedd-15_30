# Szótár - dictionary

lista = ["alma", "banán", "citrom", "dinnye"]
print(lista[1], lista[3])

leltár = {
    "alma": 12,
    "banán": 20,
    "citrom": 9,
    "dinnye": 11,
    "avokádó": 4,
    "mangó": 16,
    "eper": 3
}
print(leltár["dinnye"])
for item in leltár.keys():
    print(item, leltár[item])

total = 0
for value in leltár.values():
    total += value
print(total/len(leltár))

x = leltár.items()
x = list(x)
print(x)
print(type(x))
for item in x:
    print(item)
    print(type(item))

my_tuple = (1, 5, 7)
print(my_tuple)
#my_tuple[1] = 10 TypeError
print(my_tuple[1]) #5
my_tuple = (my_tuple[0], 10, my_tuple[2])
print(my_tuple)

#immutable
tuple1 = (1,2,3)
tuple2 = (6,5,2)
tuple3 = (8,1,5)
tuple4 = (7,8,2)

print(tuple1 + tuple2) # Concat (összefűzés)
#print(tuple1 - tuple2) 
#print(tuple1 * tuple2) 
#print(tuple1 / tuple2) 

print(tuple1.__add__(tuple2))
print(tuple1.__contains__(5))
print(5 in tuple1)
print(tuple1.count(1)) # Megszámolja, hogy az adott érték, hányszor szerepel a tupleben
print(tuple1.index(3)) #2

def get_max(lista):
    max_index = 0
    for i in range(1, len(lista)):
        if lista[i] > lista[max_index]:
            max_index = i
    return (lista[max_index], max_index)

lista = [12, 83, 12, 16, 54, 91, 23, 37, 58, 90]
maximum = get_max(lista)
print(maximum)
max_value, max_index = get_max(lista)
print(max_value)
print(max_index)
a, b , c = tuple1
print(a,b,c) 

tuple1 = (1,2,3)
tuple2 = (3,2,1)
tuple3 = (1,2,3)

print(tuple1 == tuple2)
print(tuple1 == tuple3)

print("kutya"*5)
print(tuple1 * 3)

import random

#list comprehension
lista = [random.randint(1, 10) for i in range(10)]
print(lista)

tuple1 = (random.randint(1,10) for i in range(5))
print(tuple1)

lista = [random.randint(-100, 100) for i in range(50000)]
# Számoljuk meg, hogy melyik szám, hányszor szerepel a listában

count_dict = {}
for num in lista:
    if num in count_dict:
        count_dict[num] += 1
    else:
        count_dict[num] = 1
print(count_dict)


words = []
with open("input.txt", "r", encoding="utf-8") as f:
    words = f.read().split()
print(words)

word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

#print(word_count)

from pprint import pprint

pprint(word_count)

"""
count_lista = [0 for i in range(201)]
for num in lista:
    count_lista[num] += 1

for i in range(-100, 101):
    print(f"{i} -> {count_lista[i]}")"""










# Amit majd nézzünk meg:
# szótár gyakorlás
# számrendszerek
# fájl kezelést
# osztályok (OOP)


