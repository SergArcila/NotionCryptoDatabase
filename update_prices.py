import os
import requests
from dotenv import load_dotenv
import time

#To run activate enviorment source venv/bin/activate then run python3 update_prices.py


# Load environment variables from .env
load_dotenv()
print(os.getenv("NOTION_DATABASE_ID"))

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
CMC_API_KEY = os.getenv("CMC_API_KEY")

# Notion API version can vary; 2022-06-28 is common and stable.
NOTION_API_VERSION = "2022-06-28"


def get_notion_coins():
    """
    Fetch all crypto entries from the Notion database.
    Returns a list of dictionaries with 'page_id', 'name', 'symbol'.
    """
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()  # raise an error if request failed

    data = response.json()
    results = data.get("results", [])

    coins = []
    for page in results:
        page_id = page["id"]

        # Extract the coin name from the 'Name' title property
        name_property = page["properties"]["Name"]["title"]
        name = name_property[0]["text"]["content"] if name_property else ""

        # Extract the symbol from the 'Symbol' text property
        symbol_property = page["properties"]["Symbol"]["rich_text"]
        symbol = symbol_property[0]["text"]["content"] if symbol_property else ""

        coins.append({
            "page_id": page_id,
            "name": name,
            "symbol": symbol
        })


    return coins


def get_coin_price_from_cmc(symbol):
    """
    Fetch the latest price in USD for a given symbol (e.g., 'BTC') from CoinMarketCap.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {
        "symbol": symbol
    }
    headers = {
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    # data['data'] is a dictionary keyed by symbol if found
    try:
        price = data["data"][symbol]["quote"]["USD"]["price"]
        return price
    except KeyError:
        # If the symbol doesn't exist or an error occurs
        return None


def update_notion_price(page_id, price):
    """
    Update the 'Price' property of a Notion page with the given price.
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json"
    }

    # Update the 'Price' property (assumes it's a 'number' property in Notion)
    data = {
        "properties": {
            "Price": {
                "number": price
            }
        }
    }

    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def truncate(number: float, decimals: int) -> float:
    """
    Truncates `number` to a given number of decimal places (without rounding).
    Example: truncate(0.0011499, 5) -> 0.00114
    """
    # Convert to string with plenty of decimal places
    s = f"{number:.20f}"
    dot_index = s.find('.')
    
    if dot_index == -1:
        # No decimal found (unlikely, but just in case)
        return float(s)

    # Calculate cutoff index for the desired number of decimals
    cutoff = dot_index + 1 + decimals  
    # Slice safely
    truncated_str = s[:cutoff]
    
    return float(truncated_str)


def custom_price_format(price: float) -> float:
    """
    Returns a float truncated to the desired decimal places based on price ranges:
    - price >= 1:    2 decimals
    - 0.01 <= price < 1: 4 decimals
    - 0.001 <= price < 0.01: 5 decimals
    - 0.0000001 <= price < 0.001: 9 decimals
    - below that: 10 decimals (fallback)
    """
    if price >= 1:
        return truncate(price, 2)
    elif price >= 0.01:
        return truncate(price, 4)
    elif price >= 0.001:
        return truncate(price, 5)
    elif price >= 0.0000001:
        return truncate(price, 9)
    else:
        # Fallback if it's extremely tiny
        return truncate(price, 10)




def main():
    print("Fetching coins from Notion database...")
    notion_coins = get_notion_coins()

    for coin in notion_coins:
        if coin["name"] == "Everest":
            continue

        symbol = coin["symbol"].upper()
        page_id = coin["page_id"]
        if not symbol:
            print(f"Skipping '{coin['name']}' - no symbol found.")
            continue

        print(f"Fetching price for {coin['name']} ({symbol})...")

        try:
            raw_price = get_coin_price_from_cmc(symbol)
            if raw_price:
                # Optionally: format or truncate price
                final_price = custom_price_format(raw_price)
                update_notion_price(page_id, final_price)
                print(f"  Updated: {coin['name']} => ${raw_price}")
            else:
                print(f"  Could not fetch price for {coin['name']} ({symbol}).")
        except requests.exceptions.HTTPError as e:
            # If it's a 429, or other HTTP error
            print(f"  HTTP error for {coin['name']} ({symbol}): {e}")
        
        # Sleep for N seconds to avoid hitting rate limits 
        time.sleep(5)  # adjust 5 to your needs (e.g. 1, 2, 10 seconds)

if __name__ == "__main__":
    main()
