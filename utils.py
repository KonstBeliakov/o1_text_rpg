def format_coins(coin_dict):
    parts = []
    if coin_dict.get("gold", 0) > 0:
        parts.append(f"{coin_dict['gold']}G")
    if coin_dict.get("silver", 0) > 0:
        parts.append(f"{coin_dict['silver']}S")
    if coin_dict.get("copper", 0) > 0:
        parts.append(f"{coin_dict['copper']}C")
    return ' '.join(parts) if parts else "Free"
