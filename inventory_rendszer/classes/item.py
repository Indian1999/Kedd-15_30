from .rarity import Rarity
import os
from PIL import Image, ImageTk

class Item:
    """
        Defines the Item abstarct class.
    """
    def __init__(self, name:str, rarity:Rarity = Rarity.COMMON, maxStackSize:int = 20, vendorSellPrice:int = 100, quantity: int = 1)-> None:
        """
            Args:
            name (str): The name of the item
            rairty (Rarity): The rarity of the item
            ...
        """
        self.quantity = quantity
        self.maxStackSize = maxStackSize
        self.vendorSellPrice = vendorSellPrice # Mennyiért tudom vendornak eladni
        self.vendorBuyPrice = 10*vendorSellPrice # Ha egy vendor árulja, mennyiért tudom megvenni?
        self.rarity = rarity
        self.name = name
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        # inventory_rendszer mappa útvonala
        self.icon_path =  os.path.join(base_dir, "images", self.get_file_name(self.name))
        if not os.path.exists(self.icon_path):
            self.icon_path = os.path.join(base_dir, "images", "placeholder_icon.png")
        self.icon_image = ImageTk.PhotoImage(Image.open(self.icon_path).resize((50,50)))
        
    def get_file_name(self, name:str) -> str:
        return name.lower().replace(" ","_").replace("'","") + ".png"
    
    #Enchanted Ring;epic;20;500;1
    def __str__(self):
        return f"{self.name};{self.rarity.name};{self.maxStackSize};{self.vendorSellPrice};{self.quantity}"
        