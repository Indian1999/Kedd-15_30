from rarity import Rarity
class Item:
    """
        Defines the Item abstarct class.
    """
    def __init__(self, name:str, rarity:Rarity = Rarity.COMMON, maxStackSize:int = 20, vendorSellPrice:int = 100)-> None:
        """
            Args:
            name (str): The name of the item
            rairty (Rarity): The rarity of the item
            ...
        """
        self.maxStackSize = maxStackSize
        self.vendorSellPrice = vendorSellPrice # Mennyiért tudom vendornak eladni
        self.vendorBuyPrice = 10*vendorSellPrice # Ha egy vendor árulja, mennyiért tudom megvenni?
        self.rarity = rarity
        self.name = name