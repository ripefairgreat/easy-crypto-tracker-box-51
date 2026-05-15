import requests
import sys

API_URL = "https://api.coingecko.com/api/v3/simple/price"

TRACKED_COINS = ["bitcoin", "ethereum", "solana", "cardano", "polkadot"]

def get_prices(coins=None):
    if coins is None:
        coins = TRACKED_COINS
    ids = ",".join(coins)
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}
    resp = requests.get(API_URL, params=params)
    return resp.json()

def display_prices(data):
    print(f"{'Coin':<15} {'Price':>12} {'24h Change':>12}")
    print("-" * 40)
    for coin, info in sorted(data.items()):
        price = info["usd"]
        change = info.get("usd_24h_change", 0)
        arrow = "+" if change >= 0 else ""
        print(f"{coin.title():<15} ${price:>11,.2f} {arrow}{change:.2f}%")

if __name__ == "__main__":
    coins = sys.argv[1:] if len(sys.argv) > 1 else None
    data = get_prices(coins)
    display_prices(data)
