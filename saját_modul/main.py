from myPackage import functions
from myPackage.vector3 import Vector3

import numpy as np

print(functions.add(4,5))
print(functions.power(2,3))

mtx = functions.matrix_generator(5, 7)
print(mtx)

v = Vector3(1,2,3)
print(v)
a = Vector3(2,-5,0)
print(a)
print(Vector3.distance(a,v))


