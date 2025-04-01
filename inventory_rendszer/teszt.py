from classes import *
import tkinter as tk # pip install tkinter
from tkinter import messagebox

"""
TODO:
szélesebb grid
kilépéskor mentés
itemeknek ikon

"""
#asdsadasd


"""cheese = Food("Parenyica", Rarity.RARE, 15)
ushanka = Helmet("Ushanka", Rarity.UNCOMMON, 7, 1, Stats(3,0,1,10,10), 21)"""

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyper-backpackers (aka 4D backpackers, because their backpacks can hold a ridicolusly lot of stuff)")
        self.plr_inventory = Inventory(items = [], money = 1000)
        self.vendor_inventory = Inventory(items=[])
        self.load_inventory()
        self.setup_ui()
        
    def load_inventory(self):
        with open("inventory_rendszer/data/player_inventory.csv","r",encoding="utf-8") as f:
            f.readline()
            line = f.readline()
            while line != "":
                line = line.strip().split(";")
                item = Item(line[0],Rarity.COMMON,int(line[2]),int(line[3]),int(line[4]))
                self.plr_inventory.addItem(item)
                line = f.readline()
        with open("inventory_rendszer/data/vendor_inventory.csv","r",encoding="utf-8") as f:
            f.readline()
            line = f.readline()
            while line != "":
                line = line.strip().split(";")
                item = Item(line[0],Rarity.COMMON,int(line[2]),int(line[3]),int(line[4]))
                self.vendor_inventory.addItem(item)
                line = f.readline()
        print(len(self.vendor_inventory.items))
        print(len(self.plr_inventory.items))
    def setup_ui(self):
        self.money_label = tk.Label(self.root, text = f"Gold: {self.plr_inventory.money}", font=("Times New Roman",16))
        self.money_label.grid(row = 0, column = 0, columnspan = 4, pady=10)

        tk.Label(self.root,text="Your Hyper-backpack", font=("Times New Roman",18)).grid(row=1, column=0,columnspan=2)
        tk.Label(self.root, text="Vendor's Hyper-backpack", font=("Times New Roman", 18)).grid(row=1, column=2, columnspan=2)

        self.player_frame = tk.Frame(self.root)
        self.vendor_frame = tk.Frame(self.root)
        self.player_frame.grid(row=2,column=0,columnspan=2,padx=10)
        self.vendor_frame.grid(row=2, column=2, columnspan=2, padx=10)

        self.refresh_inventories()

    def refresh_inventories(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.vendor_frame.winfo_children():
            widget.destroy()

        row,col = 0,0
        for item in self.plr_inventory.items:
            self.create_item_widget(self.player_frame, item, self.sell_item, row,col)
            col+=1
            if col > 1:
                col= 0
                row+=1

        row, col = 0, 0
        for item in self.vendor_inventory.items:
            self.create_item_widget(self.vendor_frame, item, self.buy_item, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        self.money_label.config(text = f"Gold: {self.plr_inventory.money}")

    def create_item_widget(self, frame, item, action_function, row,col):
        item_frame = tk.Frame(frame, padx=5,pady=5)
        item_frame.grid(row=row,column=col,padx=5,pady=5)
        icon_label = tk.Label(item_frame, image=item.icon_image)
        icon_label.pack()

        name_label = tk.Label(item_frame, text=f"{item.rarity.name} {item.name} {item.quantity}x")
        name_label.pack()

        if action_function == self.buy_item:
            price_label = tk.Label(item_frame, text=f"{item.vendorBuyPrice} 🪙")
            price_label.pack()
        else:
            price_label = tk.Label(item_frame, text=f"{item.vendorSellPrice} 🪙")
            price_label.pack()

        action_btn = tk.Button(item_frame,text = "Buy" if action_function == self.buy_item else "Sell",
                               command=lambda: action_function(item))
        action_btn.pack(pady=5)

    def buy_item(self, item):
        if item not in self.vendor_inventory:
            return
        if self.plr_inventory.money < item.vendorBuyPrice:
            messagebox.showwarning("Not enough gold!","You cannot afford this item!")
            return
        self.plr_inventory.money -= item.vendorBuyPrice
        if item.quantity == 1:
            self.vendor_inventory.removeItem(item)
        else:
            item.quantity -= 1

        self.plr_inventory.addItem(Item(item.name, item.rarity, item.maxStackSize, item.vendorSellPrice, 1))
        self.refresh_inventories()

    def sell_item(self, item):
        if item not in self.plr_inventory:
            return
        self.plr_inventory.money += item.vendorSellPrice
        item.quantity-=1
        if item.quantity == 0:
            self.plr_inventory.removeItem(item)
        self.vendor_inventory.addItem(Item(item.name, item.rarity, item.maxStackSize, item.vendorSellPrice, 1))
        self.refresh_inventories()


if __name__ == "__main__": # Ez a program belépsi pontja
    root = tk.Tk()
    app = App(root)
    root.mainloop()