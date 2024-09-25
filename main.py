import random

from player import Player
from monster import Monster
from store import Store
from items import *
from utils import *


# Function to create random monsters
def generate_monsters():
    # Decide the number of monsters in the encounter (e.g., 2-4)
    num_monsters = random.randint(2, 4)
    available_monsters = [
        Monster("Goblin", 50, 10, 5, 50, [
            Consumable("Small Potion", "Heals 20 HP", healing=20),
            Equipment("Wooden Shield", "A basic shield made of wood.", slot="Armor", defense_bonus=5)
        ], coin_drop={"gold": 0, "silver": 5, "copper": 50}),
        Monster("Skeleton", 60, 12, 8, 60, [
            Equipment("Bone Shield", "A shield crafted from bones.", slot="Armor", defense_bonus=8),
            Equipment("Short Sword", "A short but sharp sword.", slot="Weapon", attack_bonus=7)
        ], coin_drop={"gold": 0, "silver": 10, "copper": 70}),
        Monster("Orc", 80, 15, 10, 80, [
            Equipment("Orcish Axe", "A mighty axe that increases attack.", slot="Weapon", attack_bonus=10),
            Consumable("Large Potion", "Heals 50 HP", healing=50)
        ], coin_drop={"gold": 0, "silver": 15, "copper": 100}),
        Monster("Troll", 120, 20, 15, 120, [
            Equipment("Troll Hide Armor", "Heavy armor made from troll hide.", slot="Armor", defense_bonus=15),
            Consumable("Mega Potion", "Heals 100 HP", healing=100)
        ], coin_drop={"gold": 1, "silver": 0, "copper": 200}),
        Monster("Dragon", 200, 30, 20, 300, [
            Equipment("Dragon Scale Shield", "A very rare and powerful shield.", slot="Armor", defense_bonus=25),
            Equipment("Dragon Slayer Axe", "An axe capable of slaying dragons.", slot="Weapon", attack_bonus=30)
        ], coin_drop={"gold": 5, "silver": 0, "copper": 500})
    ]
    # Randomly select monsters, allowing repetition
    monsters = []
    for _ in range(num_monsters):
        monster_template = random.choice(available_monsters)
        # Create a copy to have independent health
        monsters.append(Monster(monster_template.name, monster_template.max_health, monster_template.attack,
                                monster_template.defense, monster_template.exp, monster_template.drop_items,
                                monster_template.coin_drop))
    return monsters


# Combat system
def combat(player, monsters):
    print("\n=== Combat Start ===")
    print(f"A group of {len(monsters)} monsters approaches!")
    active_monsters = monsters.copy()

    while active_monsters and player.is_alive():
        print("\n--- Current Status ---")
        player.display_health_bar()
        print("\nMonsters:")
        for idx, monster in enumerate(active_monsters, 1):
            monster.display_health_bar()
        print("----------------------")

        print("\nChoose your action:")
        print("1. Attack")
        print("2. Use Consumable")
        print("3. Equip Item")
        print("4. View Stats")
        print("5. Run")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Attack action
            # Let player choose which monster to attack
            try:
                target = int(input(f"Select the monster to attack (1-{len(active_monsters)}): "))
                if 1 <= target <= len(active_monsters):
                    monster = active_monsters[target - 1]
                    damage = max(player.attack - monster.defense, 1)
                    monster.health -= damage
                    print(f"\nYou attack the {monster.name} for {damage} damage.")
                    if not monster.is_alive():
                        print(f"You have defeated the {monster.name}!")
                        player.gain_exp(monster.exp)
                        player.add_coins(monster.coin_drop)
                        # Handle item drops
                        if monster.drop_items:
                            drop_chance = random.random()
                            if drop_chance < 0.7:  # 70% chance to drop an item
                                dropped_item = random.choice(monster.drop_items)
                                print(f"The {monster.name} dropped a {dropped_item.name}!")
                                player.add_item(dropped_item)
                        active_monsters.remove(monster)
                else:
                    print("Invalid target.")
                    continue
            except ValueError:
                print("Invalid input.")
                continue

        elif choice == '2':
            player.use_item()
        elif choice == '3':
            player.equip_item()
        elif choice == '4':
            player.show_stats()
            continue  # Allow player to continue without monsters attacking
        elif choice == '5':
            # Attempt to run away; success chance depends on number of monsters
            success_chance = 0.3 + (0.1 * len(active_monsters))  # Base 30% + 10% per monster
            if random.random() < success_chance:
                print("You successfully ran away from the battle!")
                return
            else:
                print("Failed to run away!")
        else:
            print("Invalid choice.")
            continue

        # Check if all monsters are defeated
        if not active_monsters:
            print("\n*** You have defeated all the monsters! ***")
            break

        # Monsters' turn to attack
        print("\n--- Monsters' Turn ---")
        for monster in active_monsters:
            if monster.is_alive():
                damage = max(monster.attack - player.defense, 1)
                player.health -= damage
                print(f"The {monster.name} attacks you for {damage} damage.")
                if not player.is_alive():
                    print("\nYou have been defeated. Game Over.")
                    exit()
        print("-----------------------")

    if not player.is_alive():
        print("\nYou have been defeated. Game Over.")
        exit()

    print("=== Combat End ===\n")


def add_monster_health_bar():
    def display_health_bar(self):
        bar_length = 20
        health_ratio = self.health / self.max_health
        filled_length = int(bar_length * health_ratio)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"{self.name}: |{bar}| {self.health}/{self.max_health} HP")

    Monster.display_health_bar = display_health_bar


# Main game loop
def main():
    store = Store()
    print("=== Welcome to the Text RPG Game ===")
    player_name = input("Enter your character's name: ")
    player = Player(player_name)
    print(f"\nWelcome, {player.name}! Your adventure begins...\n")

    while player.is_alive():
        print("Choose an action:")
        print("1. Explore (Fight monsters)")
        print("2. View Inventory")
        print("3. View Equipment")
        print("4. View Stats")
        print("5. Use Consumable")
        print("6. Equip Item")
        print("7. Unequip Item")
        print("8. Visit Store")
        print("9. Quit Game")
        print("10. Use Magic Scroll")

        choice = input("Enter your choice: ")

        if choice == '1':
            monsters = generate_monsters()
            combat(player, monsters)
        elif choice == '2':
            player.show_inventory()
        elif choice == '3':
            player.show_equipment()
        elif choice == '4':
            player.show_stats()
        elif choice == '5':
            player.use_item()
        elif choice == '6':
            player.equip_item()
        elif choice == '7':
            player.unequip_item()
        elif choice == '8':
            store.buy_item(player)
        elif choice == '9':
            print("Thank you for playing! Goodbye.")
            break
        elif choice == '10':
            player.use_item()
        else:
            print("Invalid choice. Please select a valid action.")

    if not player.is_alive():
        print("You have perished on your journey. Game Over.")


def add_monster_health_bar():
    def display_health_bar(self):
        bar_length = 20
        health_ratio = self.health / self.max_health
        filled_length = int(bar_length * health_ratio)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"{self.name}: |{bar}| {self.health}/{self.max_health} HP")

    Monster.display_health_bar = display_health_bar


# Run the game
if __name__ == "__main__":
    add_monster_health_bar()
    main()

