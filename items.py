class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"


class Consumable(Item):
    def __init__(self, name, description, healing=0, cost={"gold": 0, "silver":0, "copper":0}):
        super().__init__(name, description)
        self.healing = healing
        self.cost = cost  # Cost in coins


class Equipment(Item):
    def __init__(self, name, description, slot, attack_bonus=0, defense_bonus=0, cost={"gold":0, "silver":0, "copper":0}):
        super().__init__(name, description)
        self.slot = slot  # e.g., 'Weapon', 'Armor'
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.cost = cost  # Cost in coins

    def __str__(self):
        bonuses = []
        if self.attack_bonus:
            bonuses.append(f"Attack +{self.attack_bonus}")
        if self.defense_bonus:
            bonuses.append(f"Defense +{self.defense_bonus}")
        bonus_str = ", ".join(bonuses) if bonuses else "No bonuses"
        return f"{self.name} ({self.slot}): {self.description} [{bonus_str}]"


class MagicScroll(Consumable):
    def __init__(self, name, description, scroll_type, enchant_bonus, cost={"gold":0, "silver":0, "copper":0}):
        super().__init__(name, description, healing=0, cost=cost)
        self.scroll_type = scroll_type  # 'Attack' or 'Defense'
        self.enchant_bonus = enchant_bonus  # e.g., 5

    def __str__(self):
        return f"{self.name}: {self.description} [{self.scroll_type} +{self.enchant_bonus}]"

