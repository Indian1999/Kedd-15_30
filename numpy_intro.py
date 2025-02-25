import numpy as np # terminálba: pip install numpy

# 0 Dimenzionális
arr = np.array(5)
print(arr)
print(type(arr))
print(arr.shape)

# 1 Dimenzionális
print([1,2,3,4,5])
arr = np.array([1,2,3,4,5])
print(arr)
print(type(arr))
print(arr.shape)

# 2 Dimenziós
arr = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
print(arr)
print(type(arr))
print(arr.shape)

# 3 Dimenziós
arr = np.array([[[1,2,3,4], [5,6,7,8], [9,10,11,12]],[[1,2,3,4], [5,6,7,8], [9,10,11,12]],[[1,2,3,4], [5,6,7,8], [9,10,11,12]]])
print(arr)
print(type(arr))
print(arr.shape)

# 5 dimenziós
arr = np.array([1,2,3,4,5,6,7,8,9,10,11,12,1,1,1,1,1,1,1,1,1,1,1], ndmin=5)
print(arr)
print(type(arr))
print(arr.shape)

# nparray indexelése

arr = np.array([i for i in range(1, 101)])
print(arr[5])
print(arr[-1])
print(arr[5:10])
arr = arr.reshape(10,10)
print(arr[5,8]) # lista[5][8]
print(arr[:,5]) # Az összes sor, 5. oszlopa
print(arr[3:6, 0]) # 3,4,5. sorok 0. oszlopai

# np array típusai
# Egy np arrayen belül, nem keverhetjük a típusokat
arr = np.array([54, "banán", True])
print(arr.dtype)
arr = np.array([54, 23, 11, 12])
print(arr.dtype) # int32 (32 bitet foglal el egy szám)
arr = arr.astype("float32")
print(arr.dtype)
print(arr)