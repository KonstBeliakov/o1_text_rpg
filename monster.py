class Monster:
    def __init__(self, name, health, attack, defense, exp, drop_items, coin_drop):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.drop_items = drop_items  # List of Item objects
        self.coin_drop = coin_drop  # Dict with 'gold', 'silver', 'copper'

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name}: {self.health}/{self.max_health} HP"