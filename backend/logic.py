import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta
import re

FALLBACK_PRICES = {
    "tomato": 40, "onion": 25, "potato": 18, "rice": 50, "wheat": 30,
    "apple": 120, "banana": 40, "mango": 80, "bhindi": 35, "cabbage": 20,
    "carrot": 30, "cauliflower": 35, "garlic": 60, "ginger": 100, "lemon": 150,
    "milk": 60, "paneer": 400, "chicken": 180, "egg": 6, "dal": 100
}

price_cache = {"data": FALLBACK_PRICES.copy(), "last_updated": None}
price_history = {item: [] for item in FALLBACK_PRICES.keys()}

def fetch_government_api_prices():
    try:
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        params = {"api-key": "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b", "format": "json", "limit": 50}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            prices = {}
            if 'records' in data:
                for record in data['records']:
                    commodity = record.get('commodity', '').lower()
                    modal_price = record.get('modal_price', 0)
                    if modal_price:
                        try:
                            price = int(float(str(modal_price)))
                            if 'tomato' in commodity: prices['tomato'] = price
                            elif 'onion' in commodity: prices['onion'] = price
                            elif 'potato' in commodity: prices['potato'] = price
                        except: pass
            if prices:
                print(f"Government API: {len(prices)} prices")
                return prices
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None

def scrape_agmarknet_prices():
    try:
        print("Scraping Agmarknet...")
        url = "https://agmarknet.gov.in/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        prices = {}
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 2:
                    commodity = cols[0].get_text(strip=True).lower()
                    for col in cols[1:]:
                        price_match = re.search(r'(\d+)', col.get_text(strip=True))
                        if price_match:
                            price = int(price_match.group(1))
                            if 'tomato' in commodity: prices['tomato'] = price
                            elif 'onion' in commodity: prices['onion'] = price
                            elif 'potato' in commodity: prices['potato'] = price
                            break
        if prices:
            print(f"Scraped {len(prices)} prices")
            return prices
        return None
    except Exception as e:
        print(f"Scraping error: {e}")
        return None

def add_fluctuation(prices):
    return {k: max(1, int(v * (1 + random.uniform(-0.08, 0.08)))) for k, v in prices.items()}

def update_price_history(prices):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    for item, price in prices.items():
        if item in price_history:
            price_history[item].append({"timestamp": timestamp, "price": price})
            if len(price_history[item]) > 30:
                price_history[item] = price_history[item][-30:]

def get_current_prices():
    now = datetime.now()
    if price_cache["last_updated"]:
        diff = now - price_cache["last_updated"]
        if diff < timedelta(minutes=10):
            return price_cache["data"]
    
    print("Fetching live prices...")
    gov_prices = fetch_government_api_prices()
    if gov_prices:
        final_prices = FALLBACK_PRICES.copy()
        final_prices.update(gov_prices)
    else:
        scraped_prices = scrape_agmarknet_prices()
        if scraped_prices:
            final_prices = FALLBACK_PRICES.copy()
            final_prices.update(scraped_prices)
        else:
            final_prices = add_fluctuation(FALLBACK_PRICES)
    
    price_cache["data"] = final_prices
    price_cache["last_updated"] = now
    update_price_history(final_prices)
    return final_prices

def get_price_history(item):
    return price_history.get(item.lower(), [])

def get_weather_data(city="Delhi"):
    return {
        "temperature": random.randint(20, 35),
        "humidity": random.randint(40, 80),
        "description": "partly cloudy",
        "wind_speed": random.randint(5, 15)
    }

def predict_price_trend(item):
    history = get_price_history(item)
    if len(history) < 3:
        return "stable"
    recent_prices = [h['price'] for h in history[-5:]]
    avg_change = sum(recent_prices[i] - recent_prices[i-1] for i in range(1, len(recent_prices))) / (len(recent_prices) - 1)
    if avg_change > 2:
        return "increasing"
    elif avg_change < -2:
        return "decreasing"
    else:
        return "stable"

def negotiate(product, base_price, buyer_price):
    prices = get_current_prices()
    product = product.lower()
    if product in prices:
        mandi = prices[product]
        diff = buyer_price - mandi
        trend = predict_price_trend(product)
        if diff > 10:
            status, msg = "LOSS", f"Aap zyada de rahe ho! Mandi rate Rs{mandi} hai."
        elif diff < -10:
            status, msg = "PROFIT", f"Badhai ho! Sasta mila. Mandi rate Rs{mandi} hai."
        else:
            status, msg = "FAIR", "Theek bhaav hai."
        if trend == "increasing":
            msg += " Price badh rahi hai."
        elif trend == "decreasing":
            msg += " Price gir rahi hai."
    else:
        mandi, status, msg, trend = buyer_price, "UNKNOWN", "Item ka rate nahi mila.", "stable"
    return {"item": product, "mandi_price": mandi, "seller_price": buyer_price, "status": status, "message": msg, "trend": trend}

MANDI_PRICES = FALLBACK_PRICES
