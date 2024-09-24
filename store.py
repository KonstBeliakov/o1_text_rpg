from items import *
from utils import *


class Store:
    def __init__(self):
        # Define items available for purchase
        self.items = [
            Consumable("Small Potion", "Heals 20 HP", healing=20, cost={"gold":0, "silver":10, "copper":50}),
            Consumable("Large Potion", "Heals 50 HP", healing=50, cost={"gold":0, "silver":25, "copper":0}),
            Consumable("Mega Potion", "Heals 100 HP", healing=100, cost={"gold":1, "silver":0, "copper":0}),
            Equipment("Iron Sword", "A sturdy iron sword.", slot="Weapon", attack_bonus=10, cost={"gold":2, "silver":0, "copper":0}),
            Equipment("Steel Shield", "A strong steel shield.", slot="Armor", defense_bonus=10, cost={"gold":2, "silver":50, "copper":0}),
            MagicScroll("Attack Scroll", "A scroll that enchants a weapon, increasing its attack.", scroll_type="Attack", enchant_bonus=5, cost={"gold":1, "silver":50, "copper":0}),
            MagicScroll("Defense Scroll", "A scroll that enchants armor, increasing its defense.", scroll_type="Defense", enchant_bonus=5, cost={"gold":1, "silver":50, "copper":0})
        ]

    def show_items(self):
        print("\n--- Store Items ---")
        for idx, item in enumerate(self.items, 1):
            if isinstance(item, Consumable) and not isinstance(item, MagicScroll):
                healing_info = f"Heals {item.healing} HP" if item.healing > 0 else "No healing"
                cost_str = format_coins(item.cost)
                print(f"{idx}. {item.name} - {item.description} | {healing_info} | Cost: {cost_str}")
            elif isinstance(item, MagicScroll):
                cost_str = format_coins(item.cost)
                print(f"{idx}. {item.name} - {item.description} | Type: {item.scroll_type} +{item.enchant_bonus} | Cost: {cost_str}")
            elif isinstance(item, Equipment):
                bonuses = []
                if item.attack_bonus:
                    bonuses.append(f"Attack +{item.attack_bonus}")
                if item.defense_bonus:
                    bonuses.append(f"Defense +{item.defense_bonus}")
                bonus_str = ", ".join(bonuses) if bonuses else "No bonuses"
                cost_str = format_coins(item.cost)
                print(f"{idx}. {item.name} ({item.slot}) - {item.description} | {bonus_str} | Cost: {cost_str}")
        print("---------------------\n")

    def buy_item(self, player):
        self.show_items()
        try:
            choice = int(input("Select the number of the item you want to buy (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(self.items):
                item = self.items[choice - 1]
                if player.spend_coins(item.cost):
                    # Deep copy to add to player's inventory
                    if isinstance(item, Consumable) and not isinstance(item, MagicScroll):
                        bought_item = Consumable(item.name, item.description, item.healing, item.cost)
                    elif isinstance(item, MagicScroll):
                        bought_item = MagicScroll(item.name, item.description, item.scroll_type, item.enchant_bonus, item.cost)
                    elif isinstance(item, Equipment):
                        bought_item = Equipment(item.name, item.description, item.slot, item.attack_bonus, item.defense_bonus, item.cost)
                    player.add_item(bought_item)
                    print(f"You purchased {item.name}.")
                else:
                    print("Purchase failed due to insufficient funds.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

