class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.base_max_health = 100
        self.max_health = self.base_max_health
        self.base_attack = 20
        self.attack = self.base_attack
        self.base_defense = 10
        self.defense = self.base_defense
        self.health = self.max_health
        self.inventory = []
        # Equipment slots: 'Weapon', 'Armor'
        self.equipment = {
            'Weapon': None,
            'Armor': None
        }
        # Currency
        self.coins = {"gold": 10, "silver": 50, "copper": 100}  # Starting coins

    def is_alive(self):
        return self.health > 0

    def gain_exp(self, amount):
        self.exp += amount
        print(f"\nYou gained {amount} XP.")
        while self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.base_max_health += 20
        self.base_attack += 5
        self.base_defense += 3
        self.max_health = self.base_max_health
        self.health = self.max_health
        self.update_stats()
        print(f"\n*** Congratulations! You reached level {self.level}! ***")
        print(f"Stats increased: Base Health: {self.base_max_health}, Base Attack: {self.base_attack}, Base Defense: {self.base_defense}\n")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Added {item.name} to your inventory.")

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("\n--- Inventory ---")
            for idx, item in enumerate(self.inventory, 1):
                print(f"{idx}. {item}")
            print("-----------------\n")

    def use_item(self):
        consumables = [item for item in self.inventory if isinstance(item, Consumable)]
        if not consumables:
            print("You have no consumable items to use.")
            return
        print("\n--- Consumables ---")
        for idx, item in enumerate(consumables, 1):
            print(f"{idx}. {item}")
        print("-------------------")
        try:
            choice = int(input("Select the number of the consumable you want to use (0 to cancel): "))
            if choice == 0:
                return
            consumable = consumables[choice - 1]
            if consumable.healing > 0:
                self.health += consumable.healing
                if self.health > self.max_health:
                    self.health = self.max_health
                print(f"You used {consumable.name} and healed for {consumable.healing} HP.")
                self.inventory.remove(consumable)
            else:
                print(f"{consumable.name} has no use.")
        except (IndexError, ValueError):
            print("Invalid choice.")

    def equip_item(self):
        equipables = [item for item in self.inventory if isinstance(item, Equipment)]
        if not equipables:
            print("You have no equipment items to equip.")
            return
        print("\n--- Equipable Items ---")
        for idx, item in enumerate(equipables, 1):
            print(f"{idx}. {item}")
        print("------------------------")
        try:
            choice = int(input("Select the number of the item you want to equip (0 to cancel): "))
            if choice == 0:
                return
            equipment = equipables[choice - 1]
            slot = equipment.slot
            currently_equipped = self.equipment.get(slot)
            if currently_equipped:
                print(f"Unequipping {currently_equipped.name} from {slot} slot.")
                self.inventory.append(currently_equipped)
                self.remove_equipment_bonus(currently_equipped)
            self.equipment[slot] = equipment
            self.inventory.remove(equipment)
            self.apply_equipment_bonus(equipment)
            print(f"Equipped {equipment.name} to {slot} slot.")
        except (IndexError, ValueError):
            print("Invalid choice.")

    def unequip_item(self):
        equipped = {slot: item for slot, item in self.equipment.items() if item is not None}
        if not equipped:
            print("You have no equipment equipped.")
            return
        print("\n--- Equipped Items ---")
        for idx, (slot, item) in enumerate(equipped.items(), 1):
            print(f"{idx}. {item} (Slot: {slot})")
        print("----------------------")
        try:
            choice = int(input("Select the number of the item you want to unequip (0 to cancel): "))
            if choice == 0:
                return
            slot = list(equipped.keys())[choice - 1]
            item = self.equipment[slot]
            self.equipment[slot] = None
            self.inventory.append(item)
            self.remove_equipment_bonus(item)
            print(f"Unequipped {item.name} from {slot} slot.")
        except (IndexError, ValueError):
            print("Invalid choice.")

    def show_equipment(self):
        print("\n--- Equipped Items ---")
        for slot, item in self.equipment.items():
            if item:
                print(f"{slot}: {item.name}")
            else:
                print(f"{slot}: None")
        print("----------------------\n")

    def show_stats(self):
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Level: {self.level}")
        print(f"EXP: {self.exp}/{self.exp_to_level}")
        self.display_health_bar()
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        self.display_coins()
        print("---------------------------\n")

    def apply_equipment_bonus(self, equipment):
        self.attack += equipment.attack_bonus
        self.defense += equipment.defense_bonus
        print(f"Stats updated: +{equipment.attack_bonus} Attack, +{equipment.defense_bonus} Defense.")

    def remove_equipment_bonus(self, equipment):
        self.attack -= equipment.attack_bonus
        self.defense -= equipment.defense_bonus
        print(f"Stats updated: -{equipment.attack_bonus} Attack, -{equipment.defense_bonus} Defense.")

    def update_stats(self):
        # Reset stats to base plus equipment bonuses
        self.attack = self.base_attack
        self.defense = self.base_defense
        for equipment in self.equipment.values():
            if equipment:
                self.attack += equipment.attack_bonus
                self.defense += equipment.defense_bonus

    def display_health_bar(self):
        # Display a visual health bar
        bar_length = 20
        health_ratio = self.health / self.max_health
        filled_length = int(bar_length * health_ratio)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"Health: |{bar}| {self.health}/{self.max_health} HP")

    def display_coins(self):
        # Display coins in a readable format
        gold = self.coins["gold"]
        silver = self.coins["silver"]
        copper = self.coins["copper"]
        print(f"Coins: {gold} Gold, {silver} Silver, {copper} Copper")

    def add_coins(self, coin_dict):
        # Add coins, handling the conversion if necessary
        self.coins["copper"] += coin_dict.get("copper", 0)
        self.coins["silver"] += coin_dict.get("silver", 0)
        self.coins["gold"] += coin_dict.get("gold", 0)
        # Convert excess copper to silver and silver to gold
        self.convert_coins()

    def convert_coins(self):
        # 100 copper = 1 silver, 100 silver = 1 gold
        # Convert copper to silver
        if self.coins["copper"] >= 100:
            self.coins["silver"] += self.coins["copper"] // 100
            self.coins["copper"] = self.coins["copper"] % 100
        # Convert silver to gold
        if self.coins["silver"] >= 100:
            self.coins["gold"] += self.coins["silver"] // 100
            self.coins["silver"] = self.coins["silver"] % 100

    def spend_coins(self, cost):
        """
        Attempt to spend coins. Cost is a dict with 'gold', 'silver', 'copper'.
        Returns True if successful, False otherwise.
        """
        # First, calculate total copper
        total_player = self.coins["gold"] * 10000 + self.coins["silver"] * 100 + self.coins["copper"]
        total_cost = cost.get("gold", 0) * 10000 + cost.get("silver", 0) * 100 + cost.get("copper", 0)
        if total_player < total_cost:
            print("You don't have enough coins for this purchase.")
            return False
        # Deduct copper, then silver, then gold
        remaining = total_cost
        # Deduct gold
        gold_needed = remaining // 10000
        if gold_needed > self.coins["gold"]:
            gold_needed = self.coins["gold"]
        self.coins["gold"] -= gold_needed
        remaining -= gold_needed * 10000
        # Deduct silver
        silver_needed = remaining // 100
        if silver_needed > self.coins["silver"]:
            silver_needed = self.coins["silver"]
        self.coins["silver"] -= silver_needed
        remaining -= silver_needed * 100
        # Deduct copper
        if remaining > self.coins["copper"]:
            # Not enough copper, need to adjust
            # Here, we'll assume coins have already been converted
            print("Error in coin deduction.")
            return False
        self.coins["copper"] -= remaining
        return True