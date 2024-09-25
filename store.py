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
        while True:
            print("\n--- Store Menu ---")
            print("1. Buy Items")
            print("2. Exchange Coins")
            print("3. Exit Store")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.process_purchase(player)
            elif choice == '2':
                self.exchange_coins(player)
            elif choice == '3':
                print("Exiting the store.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def process_purchase(self, player):
        print("\nYour current coins:")
        player.display_coins()
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

    def exchange_coins(self, player):
        while True:
            print("\n--- Exchange Coins ---")
            print("1. Buy Silver for Copper (105 Copper = 1 Silver)")
            print("2. Sell Silver for Copper (1 Silver = 95 Copper)")
            print("3. Buy Gold for Silver (105 Silver = 1 Gold)")
            print("4. Sell Gold for Silver (1 Gold = 95 Silver)")
            print("5. Cancel")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.buy_silver(player)
            elif choice == '2':
                self.sell_silver(player)
            elif choice == '3':
                self.buy_gold(player)
            elif choice == '4':
                self.sell_gold(player)
            elif choice == '5':
                print("Cancelling coin exchange.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def buy_silver(self, player):
        try:
            amount = int(input("Enter the number of Silver coins you want to buy: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
            total_cost = {"gold":0, "silver":0, "copper":105 * amount}
            print(f"Total cost: {format_coins(total_cost)}")
            if player.spend_coins(total_cost):
                player.coins["silver"] += amount
                print(f"Successfully bought {amount} Silver.")
            else:
                print("Insufficient Copper to complete the purchase.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def sell_silver(self, player):
        try:
            amount = int(input("Enter the number of Silver coins you want to sell: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
            if player.coins["silver"] < amount:
                print("You don't have enough Silver to sell.")
                return
            total_return = {"gold":0, "silver":0, "copper":95 * amount}
            player.coins["silver"] -= amount
            player.add_coins(total_return)
            print(f"Successfully sold {amount} Silver for {95 * amount} Copper.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def buy_gold(self, player):
        try:
            amount = int(input("Enter the number of Gold coins you want to buy: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
            total_cost = {"gold":0, "silver":105 * amount, "copper":0}
            print(f"Total cost: {format_coins(total_cost)}")
            if player.spend_coins(total_cost):
                player.coins["gold"] += amount
                print(f"Successfully bought {amount} Gold.")
            else:
                print("Insufficient Silver to complete the purchase.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def sell_gold(self, player):
        try:
            amount = int(input("Enter the number of Gold coins you want to sell: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
            if player.coins["gold"] < amount:
                print("You don't have enough Gold to sell.")
                return
            total_return = {"gold":0, "silver":95 * amount, "copper":0}
            player.coins["gold"] -= amount
            player.add_coins(total_return)
            print(f"Successfully sold {amount} Gold for {95 * amount} Silver.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

