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

arr = np.array([1,2,3,4], dtype="i")
print(arr)
print(arr.dtype)

arr = np.array([i for i in range(4096)]).reshape(4,4,4,4,16)

for i in range(4):
    for j in range(4):
        for k in range(4):
            for l in range(4):
                for m in range(16):
                    pass
                    #print(arr[i,j,k,l,m]) EZ SZÍVÁS
                    

    
x = np.where(arr % 512 == 0)

print(x)

filtered = []
for item in np.nditer(arr):
    if item % 512 == 0:
        filtered.append(item)
        
filtered = np.array(filtered)
#print(filtered)

filtered = arr[arr % 1024 == 0]
#print(filtered)

filter_arr = arr % 138 == 0
filtered = arr[filter_arr]
#print(filtered)

rand = np.random.randint(1, 10, size = (5,5,10))
#print(rand)

rand = np.random.rand(5, 5)
#print(rand)
rand = np.round(rand * 100, 2)
#print(rand)


import matplotlib.pyplot as plt # pip install matplotlib
rand_value = np.random.choice(["alma", "banán", "citrom", "dinnye"], p=[0.5, 0.2, 0.1, 0.2], size = 100)
#print(rand_value)

uniques, counts = np.unique(rand_value, return_counts=True)

plt.bar(uniques, counts, color = ["red", "brown", "yellow", "green"])
plt.xlabel("Gyümölcs")
plt.ylabel("Gyakoriság")
plt.title("Gyümölcsök gyakorisága")
#plt.show()
plt.savefig("fruit_bar.png")