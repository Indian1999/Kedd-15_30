from equippable import Equippable
from rarity import Rarity
from stats import Stats

class Helmet(Equippable):
    def __init__(self, name:str, rarity:Rarity = Rarity.COMMON, vendorSellPrice:int = 100, minimumLevel:int = 1, stats:Stats = Stats())-> None:
        super().__init__(name, rarity, vendorSellPrice, minimumLevel)