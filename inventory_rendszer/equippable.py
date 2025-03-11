from item import Item
from rarity import Rarity

class Equippable(Item):
    def __init__(self, name:str, rarity:Rarity = Rarity.COMMON, vendorSellPrice:int = 100, minimumLevel:int = 1)-> None:
        super().__init__(name, rarity, 1, vendorSellPrice)
        self.minimumLevel = minimumLevel