import requests

API_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_price(coin_id="solana"):
    params = {"ids": coin_id, "vs_currencies": "usd"}
    resp = requests.get(API_URL, params=params)
    data = resp.json()
    return data[coin_id]["usd"]

if __name__ == "__main__":
    price = get_price()
    print(f"Solana: ${price:,.2f}")
