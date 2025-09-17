# Felmérő


lista = [13, 16, 9, 0, -2, -3, 9, 4, -1, 2, 2, 0, 13, -8]
legnagyobb = lista[0]
# 1. feladat: Írd ki a legnagyobb számot
print(max(lista))
# 2. feladat: Írd ki a számok átlagát

# 3. feladat: Hány darab negatív szám van a listában?

# 4. feladat: Fordíts meg a listát és írd ki printtel ([-8, 13, 0, 2, 2, ..., 16, 13])

for i in lista[::-1]:
    print(i)
# 5. feladat: Rendezd növekvő sorrendbe a listát