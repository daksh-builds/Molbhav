# 🔄 Real-Time Price Integration Guide

## Current Status
- ✅ Static mandi prices (manually updated)
- ✅ Auto-refresh UI every 30 seconds
- ✅ Timestamp tracking
- ❌ Real-time API integration (not yet implemented)

## How to Add Real-Time Prices

### Option 1: Government Agmarknet API

```python
import requests

def fetch_live_prices():
    """Fetch real-time prices from Agmarknet"""
    try:
        # Agmarknet API endpoint
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        params = {
            "api-key": "YOUR_API_KEY",
            "format": "json",
            "limit": 100
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # Process and return prices
        prices = {}
        for record in data['records']:
            commodity = record['commodity'].lower()
            price = float(record['modal_price'])
            prices[commodity] = price
        
        return prices
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return MANDI_PRICES  # Fallback to static prices
```

### Option 2: Web Scraping (Agmarknet Portal)

```python
from bs4 import BeautifulSoup
import requests

def scrape_mandi_prices():
    """Scrape prices from Agmarknet website"""
    url = "https://agmarknet.gov.in/PriceAndArrivals/CommodityDailyStateWise.aspx"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse table data
        prices = {}
        # Add parsing logic here
        
        return prices
    except:
        return MANDI_PRICES
```

### Option 3: Third-Party APIs

**Data.gov.in API:**
- Register at: https://data.gov.in/
- Get API key
- Access agricultural commodity prices

**Steps:**
1. Register on data.gov.in
2. Get API key
3. Find "Agricultural Marketing" datasets
4. Integrate API calls

### Implementation in Your App

Update `backend/logic.py`:

```python
import requests
from datetime import datetime, timedelta

# Cache for prices (refresh every 1 hour)
price_cache = {
    "data": MANDI_PRICES,
    "last_updated": None
}

def get_current_prices():
    """Get prices with caching"""
    now = datetime.now()
    
    # Check if cache is valid (less than 1 hour old)
    if price_cache["last_updated"]:
        time_diff = now - price_cache["last_updated"]
        if time_diff < timedelta(hours=1):
            return price_cache["data"]
    
    # Fetch new prices
    try:
        new_prices = fetch_live_prices()  # Your API call
        price_cache["data"] = new_prices
        price_cache["last_updated"] = now
        return new_prices
    except:
        return price_cache["data"]  # Return cached data on error

# Update negotiate function
def negotiate(product, base_price, buyer_price):
    CURRENT_PRICES = get_current_prices()  # Use live prices
    product_lower = product.lower()
    
    if product_lower in CURRENT_PRICES:
        mandi_price = CURRENT_PRICES[product_lower]
        # ... rest of logic
```

## Why Not Real-Time Yet?

1. **API Keys Required** - Need government API registration
2. **Rate Limits** - APIs have request limits
3. **Reliability** - Static prices ensure app always works
4. **Hackathon Demo** - Static data is sufficient for demo

## For Production

To make it truly real-time:

1. **Get API Access**
   - Register on data.gov.in
   - Get Agmarknet API credentials

2. **Add Caching**
   - Use Redis for distributed caching
   - Cache prices for 1-6 hours

3. **Add Database**
   - Store historical prices
   - Track price trends

4. **Add Webhooks**
   - Get notified when prices update
   - Push notifications to users

5. **Add ML Model**
   - Predict future prices
   - Analyze trends

## Quick Demo Hack

For hackathon demo, you can:

1. **Simulate Updates**
```python
import random

def simulate_price_fluctuation():
    """Add small random changes to prices"""
    updated_prices = {}
    for item, price in MANDI_PRICES.items():
        # Add ±5% random fluctuation
        fluctuation = random.uniform(-0.05, 0.05)
        new_price = int(price * (1 + fluctuation))
        updated_prices[item] = new_price
    return updated_prices
```

2. **Show "Live" Updates**
   - Prices change slightly every 30 seconds
   - Looks like real-time data
   - Good for demo purposes

## Current Features (Already Working)

✅ **Auto-refresh UI** - Frontend updates every 30 seconds
✅ **Timestamp** - Shows last updated time
✅ **Manual Refresh** - Button to refresh prices
✅ **20+ Items** - Comprehensive price list
✅ **Voice Feedback** - Hindi voice announcements
✅ **Status Indicators** - PROFIT/LOSS/FAIR badges

## Conclusion

Your app has the **infrastructure** for real-time prices:
- Auto-refresh mechanism ✅
- API endpoints ready ✅
- Timestamp tracking ✅
- Error handling ✅

Just need to **plug in** a real API when you get access!

For hackathon: **Current setup is perfect** - judges will understand it's a demo with static data that can easily be connected to real APIs.
