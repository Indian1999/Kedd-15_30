from classes import Food, Rarity, Helmet, Stats

cheese = Food("Gouda", Rarity.UNCOMMON, 5)
helm = Helmet(
        name = "Doom of Balrogh", 
        rarity = Rarity.EPIC,
        vendorSellPrice = 187,
        minimumLevel = 11, 
        stats = Stats(59, 0, 12, 1, 30),
        maxDurability = 234
            )
print(cheese)
print(helm)