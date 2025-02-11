"""
f = open("hatos.txt", "r", encoding="utf-8")
print(f.read(20))
f.seek(0)
print(f.read(20))
f.seek(0)
line = f.readline()
while line:
    #print(line)
    line = f.readline()
f.close()

with open("hatos.txt", "r", encoding="utf-8") as file:
    data = file.readlines()
    print(data[54])

#Itt már be van zárva az file
#file.read()

with open("myFile.txt", "w", encoding="utf-8") as f:
    f.write("General Kenobi!\nHi there.")
    f.seek(0)

with open("myFile.txt", "a", encoding="utf-8") as f:
    f.write("\nEmpire.\n")

with open("myFile.txt", "a+", encoding="utf-8") as f:
    f.write("a+ a végéről indul")

with open("myFile.txt", "r+", encoding="utf-8") as f:
    f.write("r+ az elejéről indul")
"""
import csv
import pandas as pd #pip install pandas

with open("Mall_Customers.csv", "r", encoding="utf-8") as f:
    data = csv.reader(f, delimiter= ",")
    for row in data:
        print(row)

data = pd.read_csv("Mall_Customers.csv")
meanIncome = data["Annual Income (k$)"].mean()
print(f"Átlagkereset = {round(meanIncome*1000)}$")
