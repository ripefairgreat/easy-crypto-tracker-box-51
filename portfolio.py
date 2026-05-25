import json
from pathlib import Path
from tracker import get_prices

PORTFOLIO_FILE = Path(__file__).parent / "portfolio.json"

def load_portfolio():
    if PORTFOLIO_FILE.exists():
        return json.loads(PORTFOLIO_FILE.read_text())
    return {}

def save_portfolio(portfolio):
    PORTFOLIO_FILE.write_text(json.dumps(portfolio, indent=2))

def add_holding(coin, amount, price=None):
    portfolio = load_portfolio()
    if coin not in portfolio:
        portfolio[coin] = {"amount": 0, "buy_prices": []}
    portfolio[coin]["amount"] += amount
    if price:
        portfolio[coin]["buy_prices"].append({"amount": amount, "price": price})
    save_portfolio(portfolio)
    print(f"Added {amount} {coin}")

def remove_holding(coin, amount=None):
    portfolio = load_portfolio()
    if coin not in portfolio:
        print(f"{coin} not in portfolio")
        return
    if amount is None or amount >= portfolio[coin]["amount"]:
        del portfolio[coin]
        print(f"Removed all {coin}")
    else:
        portfolio[coin]["amount"] -= amount
        print(f"Removed {amount} {coin}")
    save_portfolio(portfolio)

def show_portfolio(currency="usd"):
    portfolio = load_portfolio()
    if not portfolio:
        print("Empty portfolio")
        return
    coins = list(portfolio.keys())
    prices = get_prices(coins, currency)
    symbol = {"usd": "$", "eur": "E", "gbp": "P"}.get(currency, "$")
    total = 0

    print(f"{'Coin':<15} {'Amount':>10} {'Price':>12} {'Value':>12}")
    print("-" * 50)
    for coin, holding in portfolio.items():
        amount = holding["amount"]
        price = prices.get(coin, {}).get(currency, 0)
        value = price * amount
        total += value
        print(f"{coin.title():<15} {amount:>10.4f} {symbol}{price:>11,.2f} {symbol}{value:>11,.2f}")
    print("-" * 50)
    print(f"{'Total':<15} {'':>10} {'':>12} {symbol}{total:>11,.2f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "add":
        price = float(sys.argv[4]) if len(sys.argv) > 4 else None
        add_holding(sys.argv[2], float(sys.argv[3]), price)
    elif len(sys.argv) > 1 and sys.argv[1] == "remove":
        amt = float(sys.argv[3]) if len(sys.argv) > 3 else None
        remove_holding(sys.argv[2], amt)
    else:
        show_portfolio()
