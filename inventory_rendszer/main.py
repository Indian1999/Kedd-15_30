from classes import *
import tkinter as tk # pip install tkinter

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Little Inventory")
        
        self.player_inventory = Inventory()
        self.vendor_inventory = Inventory()
        self.setup_ui()
        
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
            self.create_item_widget(self.player_frame, item, None, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        row, col = 0, 0
        for item in self.vendor_inventory.items:
            self.create_item_widget(self.vendor_frame, item, None, row, col)
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
    
if __name__ == "__main__": # Ez a program belépési pontja
    root = tk.Tk()
    app = App(root)
    root.mainloop()

