from random import randint, randrange
import math as matek
import numpy as np

print(randint(1,10))
print(randrange(20, 25))

print(matek.pi)

tömb = np.linspace(0, 5, 100) # 0tól kezdődően, 5-ig generáljon 100 egyenletes számot
print(tömb)

print(type(tömb))
print(tömb.shape)
tömb = tömb.reshape(10,10)
print(tömb)
print(tömb.shape)
tömb = tömb.reshape(20, -1)
print(tömb)
print(tömb.shape)
tömb = tömb.reshape(5,5,-1)
print(tömb)
print(tömb.shape)

print(tömb.std()) # standard deviation (szórás)