from enum import Enum

class Rarity(Enum):
    JUNK = 0
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    
#print(Rarity.COMMON)
#print(Rarity.RARE.name)
#print(Rarity.EPIC.value)