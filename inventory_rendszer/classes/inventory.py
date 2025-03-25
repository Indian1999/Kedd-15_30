from .item import Item

class Inventory:
    def __init__(self, size:int = 16, items: list[Item] = [], money:int = 0):
        self.size = size
        self.items = items
        self.money = money
        
    def addItem(self, item: Item):
        if item in self.items:
            self.items[self.items.find(item)].quantity += item.quantity
        elif len(self.items) < self.size:
            self.items.append(item)
        else:
            print("Inventory is full!")
    
    def removeItem(self, item: Item):
        for i in self.items:
            if i == item:
                self.items.remove(item)
                return
        print("This item is not in the inventory!")
        
    def __contains__(self, item): # in operátor műkédésének definiálása az osztályhoz
        return item in self.items
        
        