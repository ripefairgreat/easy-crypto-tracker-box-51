import requests
import argparse

API_URL = "https://api.coingecko.com/api/v3/simple/price"

TRACKED_COINS = ["bitcoin", "ethereum", "solana", "cardano", "polkadot",
             "chainlink", "avalanche-2", "polygon", "dogecoin", "shiba-inu"]

CURRENCIES = ["usd", "eur", "gbp", "jpy", "rub"]

def get_prices(coins=None, currency="usd"):
    if coins is None:
        coins = TRACKED_COINS
    ids = ",".join(coins)
    params = {
        "ids": ids,
        "vs_currencies": currency,
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }
    resp = requests.get(API_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def display_prices(data, currency="usd", sort_by="name"):
    symbol = {"usd": "$", "eur": "E", "gbp": "P", "jpy": "Y", "rub": "R"}.get(currency, "$")
    items = list(data.items())
    if sort_by == "price":
        items.sort(key=lambda x: x[1].get(currency, 0), reverse=True)
    elif sort_by == "change":
        items.sort(key=lambda x: x[1].get(f"{currency}_24h_change", 0), reverse=True)
    else:
        items.sort(key=lambda x: x[0])

    print(f"{'Coin':<15} {'Price':>14} {'24h Change':>12}")
    print("-" * 42)
    for coin, info in items:
        price = info.get(currency, 0)
        change = info.get(f"{currency}_24h_change", 0) or 0
        arrow = "+" if change >= 0 else ""
        print(f"{coin.title():<15} {symbol}{price:>13,.2f} {arrow}{change:.2f}%")

def main():
    parser = argparse.ArgumentParser(description="Crypto Price Tracker")
    parser.add_argument("coins", nargs="*", help="Coin IDs to track")
    parser.add_argument("-c", "--currency", default="usd", choices=CURRENCIES)
    parser.add_argument("-s", "--sort", default="name", choices=["name", "price", "change"])
    args = parser.parse_args()

    coins = args.coins if args.coins else None
    data = get_prices(coins, args.currency)
    display_prices(data, args.currency, args.sort)

if __name__ == "__main__":
    main()
