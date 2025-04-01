from classes import *
import tkinter as tk # pip install tkinter
from tkinter import messagebox
import os

"""
TODO:
Az inventoryk gridje legyen szélesebb, ne csak 2 oszlop
Amikor kilépünk, akkor mentsük el az inventorykat fileba
Minden itemnek legyen saját iconja
    A file neve, legyen az item neve + png (különleges karakterek nélkül)
Beolvasásnál vegyük figyelembe a rarity-t
    
"""

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Little Inventory")
        
        self.player_inventory = Inventory(money = 3000)
        self.vendor_inventory = Inventory(items=[])
        self.load_inventory()
        self.setup_ui()
        
    def load_inventory(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, "data", "player_inventory.csv"), "r", encoding="utf-8") as f:
            f.readline()
            line = f.readline()
            while line != "":
                line = line.strip().split(";")
                item = Item(line[0], Rarity.COMMON, int(line[2]), int(line[3]), int(line[4]))
                self.player_inventory.addItem(item)
                line = f.readline()
        with open(os.path.join(base_dir, "data", "vendor_inventory.csv"), "r", encoding="utf-8") as f:
            f.readline()
            line = f.readline()
            while line != "":
                line = line.strip().split(";")
                item = Item(line[0], Rarity.COMMON, int(line[2]), int(line[3]), int(line[4]))
                self.vendor_inventory.addItem(item)
                line = f.readline()
        
    def setup_ui(self):
        self.money_label = tk.Label(self.root, text=f"Gold: {self.player_inventory.money}", font = ("Arial", 16))
        self.money_label.grid(row = 0, column = 0, columnspan=4, pady=10)
        
        tk.Label(self.root,text="Your bag", font=("Arial",12)).grid(row=1, column=0, columnspan=2)
        tk.Label(self.root,text="Vendor", font=("Arial",12)).grid(row=1, column=2, columnspan=2)
        
        self.player_frame = tk.Frame(self.root)
        self.vendor_frame = tk.Frame(self.root)
        
        self.player_frame.grid(row=2, column=0, columnspan=2, padx=10)
        self.vendor_frame.grid(row=2, column=2, columnspan=2, padx=10)
        
        self.refresh_inventories()
        
    def refresh_inventories(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.vendor_frame.winfo_children():
            widget.destroy()
            
        row, col = 0, 0
        for item in self.player_inventory.items:
            self.create_item_widget(self.player_frame, item, self.sell_item, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        row, col = 0, 0
        for item in self.vendor_inventory.items:
            self.create_item_widget(self.vendor_frame, item, self.buy_item, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        self.money_label.config(text=f"Gold: {self.player_inventory.money}")
    
    def create_item_widget(self, frame, item, action_func, row, col):
        item_frame = tk.Frame(frame, padx=5, pady=5)
        item_frame.grid(row=row, column=col, padx=5, pady=5)
        
        icon_label = tk.Label(item_frame, image=item.icon_image)
        icon_label.pack()
        
        name_label = tk.Label(item_frame, text=f"{item.name}")
        name_label.pack()
        
        quantity_label = tk.Label(item_frame, text=f"Amount: {item.quantity}")
        quantity_label.pack()
        
        if action_func == self.buy_item:
            price_label = tk.Label(item_frame, text=f"{item.vendorBuyPrice} 🪙")
            price_label.pack()
        else:
            price_label = tk.Label(item_frame, text=f"{item.vendorSellPrice} 🪙")
            price_label.pack()
        
        action_btn = tk.Button(item_frame, text = "Buy" if action_func == self.buy_item else "Sell",
                               command = lambda: action_func(item))
        action_btn.pack(pady=5)
        
    def buy_item(self, item):
        if item not in self.vendor_inventory:
            return
        if self.player_inventory.money < item.vendorBuyPrice:
            messagebox.showwarning("Not Enough Gold", "You do not have enough gold to buy this item.")
            return
        self.player_inventory.money -= item.vendorBuyPrice
        if item.quantity == 1:
            self.vendor_inventory.removeItem(item)
        else:
            item.quantity -= 1
            
        self.player_inventory.addItem(Item(item.name, item.rarity, item.maxStackSize, item.vendorSellPrice, 1))
        
        self.refresh_inventories()
    
    def sell_item(self, item):
        if item not in self.player_inventory:
            return
        self.player_inventory.money += item.vendorSellPrice
        item.quantity -= 1
        if item.quantity == 0:
            self.player_inventory.removeItem(item)
        self.vendor_inventory.addItem(Item(item.name, item.rarity, item.maxStackSize, item.vendorSellPrice, 1))
        self.refresh_inventories()
        
    
    
if __name__ == "__main__": # Ez a program belépési pontja
    root = tk.Tk()
    app = App(root)
    root.mainloop()

