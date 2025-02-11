import random
# Az osztályok nevét nagy kezdőbetűvel írjuk
class Warrior:
    #Konstruktór - Mi történjen akkor amikor létrehozunk egy Warrior-t
    def __init__(self, name, health, damage, armor, energy):
        self.name = name
        self.health = health
        self.maxHealth = health
        self.damage = damage
        self.armor = armor
        self.energy = energy

    def __str__(self):
        return f"{self.name}: Health: {self.health}, Damage: {self.damage}, Armor: {self.armor}, Energy: {self.energy}"
    
    def takeDamage(self, amount):
        self.health -= amount * (1 - self.armor/100)
        self.health = max(0, self.health)
        self.health = round(self.health, 2)

    def restoreHealth(self, amount):
        self.health += amount
        self.health = min(self.health, self.maxHealth)

    def regainEnergy(self, amount):
        self.energy += amount


player = Warrior("Player", 100, 15, 20, 100)
enemy = Warrior("Enemy", 100, 12, 40, 100)

gameOn = True
turn_of_player = True

while gameOn:
    print(player)
    print(enemy)
    if turn_of_player:
        player.armor = 20
        print("Válassz egy akciót!")
        print("\t1. támadás")
        print("\t2. védekezés")
        print("\t3. gyógyulás")
        print("\t4. pihenés")
        print("\t5. erős támadás")
        print("\t6. vérengzés")
        action = input()
        if action == "1":
            print("Megtámadod az ellenfeled.")
            enemy.takeDamage(player.damage)
        elif action == "2":
            print("Felemeled a pajzsod.")
            player.armor = player.armor + 50
        elif action == "3":
            print("Megiszol egy HP potit.")
            player.restoreHealth(15)
        elif action == "4":
            print("Megállsz pihenni.")
            player.regainEnergy(20)
        elif action == "5" and player.energy >= 20:
            print("Erős támadást használsz az ellenfeleden.")
            enemy.takeDamage(1.5 * player.damage)
            player.energy -= 20
        elif action == "6" and player.energy >= 40:
            print("Teljesen megőrülsz és az ellenfeledre támadsz.")
            enemy.takeDamage(2.5 * player.damage)
            player.armor -= 50
            player.energy -= 40
        elif action == "7":
            print("Homokot dobsz a szemébe.")
            player.energy += 5
            player.health -= 1
            continue
        else:
            print("Érvénytelen akció!")
            continue # Abbahagyja az adott ciklus futást, és a következő iterációra lép (ciklus elejére)
    else: # szg köre
        enemy.armor = 40
        action = random.randint(1, 6)
        print("#" * 50)
        if action == 1:
            print("Az ellenfeled rádtámadt.")
            player.takeDamage(enemy.damage)
        elif action == 2:
            print("Az ellenfeled védekezik.")
            enemy.armor += 50
        elif action == 3:
            print("Az ellenfeled gyógyul.")
            enemy.restoreHealth(15)
        elif action == 4:
            print("Az ellenfeled pihen")
            enemy.regainEnergy(20)
        elif action == 5:
            if enemy.energy < 20:
                continue
            else:
                print("Az ellenfeled erős támadást használ.")
                player.takeDamage(1.5*enemy.damage)
                enemy.energy -= 20
        elif action == 6:
            if enemy.energy < 40:
                continue
            else:
                print("Az ellenfeled vérengző lett.")
                player.takeDamage(2.5*enemy.damage)
                enemy.energy -= 40
                enemy.armor -= 50
        print("#" * 50)
    
    turn_of_player = not turn_of_player
    if player.health <= 0:
        print("Vesztettél! Talán legközelebb")
        gameOn = False
    if enemy.health <= 0:
        print("Legyőzted az ellenfeled!")
        gameOn = False



