# 2. feladat
class LottoHuzas:
    def __init__(self, ev, het, datum, hatSzam, hatErtek, otSzam, otErtek, negySzam, negyErtek, haromSzam, haromErtek, elso, masodik, harmadik, negyedik, otodik, hatodik):
        self.ev = ev
        self.het = het
        self.datum = datum
        self.hatSzam = hatSzam
        self.hatErtek = hatErtek
        self.otSzam = otSzam
        self.otErtek = otErtek
        self.negySzam = negySzam
        self.negyErtek = negyErtek
        self.haromSzam = haromSzam
        self.haromErtek = haromErtek
        self.elso = elso
        self.masodik = masodik
        self.harmadik = harmadik
        self.negyedik = negyedik
        self.otodik = otodik
        self.hatodik = hatodik
    def __str__(self):
        return f"{self.ev}, {self.het}. hét, {self.datum}\n{self.hatSzam} db - 6-os találat, {self.hatErtek}-ot fizet\n{self.otSzam} db - 5-ös találat, {self.otErtek}-ot fizet\n{self.negySzam} db - 4-es találat, {self.negyErtek}-ot fizet\n{self.haromSzam} db - 3-as találat, {self.haromErtek}-ot fizet"

# 3. feladat
lottoHuzasok = []
f = open("hatos.txt", "r", encoding="utf-8")
for line in f:
    line = line.strip()
    items = line.split(";")
    huzas = LottoHuzas(int(items[0]), int(items[1]), items[2], int(items[3]), items[4], int(items[5]), items[6], int(items[7]), items[8], int(items[9]), items[10], int(items[11]), int(items[12]), int(items[13]), int(items[14]), int(items[15]), int(items[16]))
    lottoHuzasok.append(huzas)

f.close()

# 4. feladat
print(f"4. feladat: {len(lottoHuzasok)}")

# 5. feladat
counter = 0
for i in lottoHuzasok:
    if i.hatSzam >= 1:
        counter+=1

print(f"5. feladat: {round(counter/len(lottoHuzasok) * 100,2)}%")

# 6. feladat

def ossznyeremeny(ev, het):
    for i in lottoHuzasok:
        if i.ev == ev and i.het == het:
            ossz = int(i.hatErtek[0:-2])*i.hatSzam+int(i.otErtek[0:-2])*i.otSzam+int(i.negyErtek[0:-2])*i.negySzam+int(i.haromErtek[0:-2])*i.haromSzam
            return ossz

#print(f"{ossznyeremeny(int(input("6. feldat:\nÉv: ")),int(input("Hét: ")))}Ft")

print(ossznyeremeny(2023,10))
# 7. feladat
counter = 0
for i in lottoHuzasok:
    counter+=ossznyeremeny(i.ev, i.het)
print(f"7. feladat: {round(counter/len(lottoHuzasok))}Ft")

# 8. feladat:
szamlaloLista = [0 for i in range(46)] # 46 db 0-t
for huzas in lottoHuzasok:
    szamlaloLista[huzas.elso] += 1
    szamlaloLista[huzas.masodik] += 1
    szamlaloLista[huzas.harmadik] += 1
    szamlaloLista[huzas.negyedik] += 1
    szamlaloLista[huzas.otodik] += 1
    szamlaloLista[huzas.hatodik] += 1

segedLista = szamlaloLista[:]
print(szamlaloLista)
topHat = []
for i in range(6):
    legnagyobb = max(segedLista)
    topHat.append(segedLista.index(legnagyobb))
    segedLista[segedLista.index(legnagyobb)] = -1
print(topHat)
"""
# 9. feladat:
dict = {}

for i in lottoHuzasok:
    if i.ev in dict:
        dict[i.ev] += i.hatSzam
    else:
        dict[i.ev] = i.hatSzam
print("9. feladat:")
for i in dict:
    print(f"{i}: {dict[i]}")

# 10. feladat

f = open("nyertesSzelvenyek.txt", "w", encoding="utf-8")

for i in lottoHuzasok:
    f.write(f"{i.datum};{i.hatSzam+i.otSzam+i.negySzam+i.haromSzam}\n")
f.close()"""