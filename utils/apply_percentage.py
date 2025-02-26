def apply_percentage(price_str, percentage):
    """
    Fiyatı string olarak alır, virgülü noktaya çevirir, sayıya dönüştürür ve yüzde oranında ekleme yapar.
    """
    # .replace(",", ".")
    price_str = str(price_str)
    try:
        price_val = float(price_str)
        new_price = price_val * (1 + percentage / 100)
        return f"{new_price:.2f}"
    except ValueError:
        return price_str
