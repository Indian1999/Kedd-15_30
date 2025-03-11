from .item import Item
from .rarity import Rarity

class Food(Item):
    def __init__(self, name:str, rarity:Rarity = Rarity.UNCOMMON, vendorSellPrice:int = 100, minimumLevel:int = 1, healthResotre:int = 5, effect = None)-> None:
        super().__init__(name, rarity, vendorSellPrice, minimumLevel)
        self.minimumLevel = minimumLevel
        self.healthRestore = healthResotre
        self.effect = effect
        
    def __str__(self):
        return f"{self.name}, {self.rarity.name}\n{self.vendorSellPrice} gold\nMinimum level: {self.minimumLevel}\nRestore {self.healthRestore} health"