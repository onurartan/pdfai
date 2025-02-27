import requests
import json
import os
from datetime import datetime, timedelta
from typing import Union


from config import CURRENCY_RATES_FILE


def format_price(price: float) -> str:
    """Fiyatı '16.000' formatına çevir (binlik ayracı olarak nokta, 2 ondalık basamak)."""
    formatted_price = "{:,.0f}".format(price).replace(",", ".")
    return formatted_price


def load_currency_data() -> dict:
    """JSON dosyasından döviz kuru verilerini yükle."""
    if os.path.exists(CURRENCY_RATES_FILE):
        with open(CURRENCY_RATES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_currency_data(data: dict):
    """Döviz kuru verilerini JSON dosyasına kaydet."""
    with open(CURRENCY_RATES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def fetch_currency_rates() -> dict:
    """CoinGecko API'sinden döviz kuru verilerini al."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,try"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        btc_usd = data["bitcoin"]["usd"]
        btc_try = data["bitcoin"]["try"]

        try_usd_rate = btc_try / btc_usd
        timestamp = datetime.now().isoformat()

        try_usd_rate_str = f"{try_usd_rate:.2f}"

        return {
            "timestamp": timestamp,
            "btc_usd": btc_usd,
            "btc_try": btc_try,
            "try_usd_rate": float(try_usd_rate_str),
        }
    else:
        print("API isteği başarısız:", response.status_code)
        return None


def usd_to_try(usd: Union[float, str]) -> str:
    """USD'yi TRY'ye çevir. Eğer 'Bilinmiyor' ise 0 döndür."""
    if usd == "Bilinmiyor":
        return "0"

    try:
        usd = float(usd)
    except ValueError:
        return "0"

    currency_data = load_currency_data()

    current_time = datetime.now()
    if not currency_data or "timestamp" not in currency_data:
        new_data = fetch_currency_rates()
        if new_data:
            save_currency_data(new_data)
            currency_data = new_data
    else:
        last_update = datetime.fromisoformat(currency_data["timestamp"])
        if current_time - last_update > timedelta(minutes=10):
            new_data = fetch_currency_rates()
            if new_data:
                save_currency_data(new_data)
                currency_data = new_data

    try_usd_rate = currency_data.get("try_usd_rate", 35.8)

    usd_to_try_price = try_usd_rate * usd
    print(f"1 USD ≈ {try_usd_rate:.2f} TRY")
    print(f"{usd} USD ≈ {usd_to_try_price:.2f} TRY")
    formatted_price = format_price(usd_to_try_price)
    return formatted_price


if __name__ == "__main__":
    result = usd_to_try(10)
    print(f"10 USD = {result} TRY")
