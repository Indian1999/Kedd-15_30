print(bin(250))
print(type(bin(250)))
print(bin(7))

num_base_2 = bin(27)[2:]
print(num_base_2)

binary = "10111011111100011" #96227
num = int(binary, 2)
print(num)

hexa = "19A5FA" #1680890
num = int(hexa, 16)
print(num)

#alt gr + W -> |
#alt gr + 3 -> ^   (kétszer kell megnyomni)
#Bináris operatorok:

a = 33
b = 42

print(a & b)   # 32   (és)
print(a | b)   # 43   (vagy)
print(a ^ b)   # 11   (kizáró vagy) [XOR]
print(a << 2)  # 132  (balra shiftelés kettővel)
#megszoroztuk a szemot 2^2-nal
print(a << 10) #33792      2^10-nel szorzunk
print(b >> 1)  #21
print(b >> 2)  #10


def is_even(num):
    if num & 1 == 1:
        return False
    return True
    
print(is_even(13))
print(is_even(123))
print(is_even(1310))
print(is_even(1301))
print(is_even(1300))


# 1. feladat: Készítsünk egy szótárat ami 30-85-ig tartalmazza a számokat kulcsként és értékkül a kettes számrendszer beli értékét tárolja el stringként
dict = {
    30: "11110",
    31: "11111",
    32: "100000",
}

for i in range(30, 86):
    dict[i] = bin(i)[2:]
    
print(dict)


# 2. feladat: Írjunk egy függvényt ami egy 16-os számrendszer beli számot átvált 10-es számrendszerbe (visszaadja ezt a számot)

def hex_to_dec(hex_num):
    return int(hex_num, 16)
    
# 3. feladat: Írjunk egy függvényt ami egy ip címet kiír kettes számrendszerben
# "192.168.1.1" -> 11000000101010000000000100000001
#                  11000000101010000000000100000001

def ip_to_bits(address):
    quartets = address.split(".")
    q0 = bin(int(quartets[0]))[2:]
    q1 = bin(int(quartets[1]))[2:]
    q2 = bin(int(quartets[2]))[2:]
    q3 = bin(int(quartets[3]))[2:]
    while len(q0) < 8:
        q0 = "0" + q0
    while len(q1) < 8:
        q1 = "0" + q1
    while len(q2) < 8:
        q2 = "0" + q2
    while len(q3) < 8:
        q3 = "0" + q3
    
    return q0+q1+q2+q3
    
print(ip_to_bits("192.168.1.1"))

