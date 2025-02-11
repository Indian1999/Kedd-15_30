class Car:
    def __init__(self, rendszam, márka, típus, évjárat, súly):
        self.rendszam = rendszam
        self.márka = márka
        self.típus = típus
        self.évjárat = évjárat
        self.súly = súly

    def __str__(self):
        return f"{self.rendszam} - {self.márka} {self.típus} ({self.évjárat}), {self.súly} kg"
    
cars = []
f = open("car_data.txt", "r", encoding="utf-8")
for line in f:
    line = line.strip() # Az elejéről meg a végéről leszedni az üres karaktereket (space, enter) 
    items = line.split(";") # ['ABC-980', 'Ford', 'Mondeo', '2016', '1929']
    car = Car(items[0], items[1], items[2], int(items[3]), int(items[4]))
    cars.append(car)
f.close()

# 1. feladat: Írja ki a DEF-948 -as rendszámú autó adatait
for car in cars:
    if car.rendszam == "DEF-948":
        print(car)
        break
# 2. feladat: Mennyi az autók össz súlya tonnában?
összeg = 0
for car in cars:
    összeg += car.súly

print(f"Az autók össztömege: {round(összeg / 1000)}t")
# 3. feladat: Írja ki a legöregebb autó adatait
maxi = 0
for i in range(1, len(cars)):
    if cars[i].évjárat < cars[maxi].évjárat:
        maxi = i
print(f"A legöregebb autó a parkolóban: {cars[maxi]}")
# 4. feladat: Az autók hány százaléka készült 2013 után?
counter = 0
for car in cars:
    if car.évjárat > 2013:
        counter += 1
print(f"Az autók {round(counter/len(cars), 2)}%-a készült 2013 után")
# 5. feladat: Írjuk ki, hogy melyik évből hány autó szerepel 
év_darab = {}
for car in cars:
    if car.évjárat in év_darab:
        év_darab[car.évjárat] += 1
    else:
        év_darab[car.évjárat] = 1
print("A különböző évjáratokból ennyi darab van a parkolóban:")
for item in sorted(év_darab.items()):
    print(f"{item[0]} - {item[1]} db")
# 6. feladat: Milyen márkájú autóból van a legtöbb a parkolóban?
márka_darab = {}
for car in cars:
    if car.márka in márka_darab:
        márka_darab[car.márka] += 1
    else:
        márka_darab[car.márka] = 1
max_key = list(márka_darab.keys())[0]
for key in márka_darab.keys():
    if márka_darab[key] > márka_darab[max_key]:
        max_key = key
print(f"A(z) {max_key} márkájú autókból van a legtöbb a parkolóban, összesen {márka_darab[max_key]} db.")

# 7. feladat: Töröljük a Renault típusú autókat a listából
for i in range(len(cars)):
    if i >= len(cars):
        break
    while (cars[i].márka == "Renault"):
        del cars[i]

print(len(cars))

# 8. Adjunk minden autónak új rendszámot (AAAA 123)
for i in range(len(cars)):
    cars[i].rendszam = "ABCD-" + str(i + 100)

# 9. Írjuk ki egy fájlba a lista jelenlegi tartalmát!
# Példa: ABCD-105;Mercedes;GLC;19996;2510

f = open("modified_cars.txt", "w", encoding="utf-8")
for car in cars:
    f.write(f"{car.rendszam};{car.márka};{car.típus};{car.évjárat};{car.súly}\n")
f.close()