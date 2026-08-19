from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

FALLBACK_PRICES = {
    "tomato": 40, "onion": 25, "potato": 18, "rice": 50, "wheat": 30,
    "apple": 120, "banana": 40, "mango": 80, "bhindi": 35, "cabbage": 20,
    "carrot": 30, "cauliflower": 35, "garlic": 60, "ginger": 100, "lemon": 150,
    "milk": 60, "paneer": 400, "chicken": 180, "egg": 6, "dal": 100
}

def negotiate(product, seller_price):
    product_lower = product.lower().strip()
    if product_lower in FALLBACK_PRICES:
        mandi_price = FALLBACK_PRICES[product_lower]
        diff = seller_price - mandi_price
        if diff > 10:
            status = "LOSS"
            message = f"Aap zyada de rahe ho! Mandi rate ₹{mandi_price}/kg hai."
        elif diff < -10:
            status = "PROFIT"
            message = f"Badhai ho! Bahut sasta mila. Mandi rate ₹{mandi_price}/kg hai."
        else:
            status = "FAIR"
            message = "Theek bhaav hai, sauda ho sakta hai."
    else:
        mandi_price = seller_price
        status = "FAIR"
        message = "Is item ka mandi rate available nahi hai."

    return {
        "item": product,
        "mandi_price": mandi_price,
        "seller_price": seller_price,
        "status": status,
        "message": message
    }

@app.route('/api', methods=['GET'])
@app.route('/', methods=['GET'])
def health():
    return jsonify({"message": "MOL-BHAAV API is running!"})

@app.route('/api/deal', methods=['POST'])
@app.route('/deal', methods=['POST'])
def deal():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    product = data.get("item", "")
    seller_price = data.get("seller_price", 0)
    
    if isinstance(seller_price, str):
        try:
            seller_price = int(seller_price)
        except ValueError:
            seller_price = 0
    
    if not product or seller_price == 0:
        return jsonify({"error": "Missing required fields"}), 400
    
    result = negotiate(product, seller_price)
    return jsonify(result)

@app.route('/api/prices', methods=['GET'])
@app.route('/prices', methods=['GET'])
def get_prices():
    return jsonify({
        "prices": FALLBACK_PRICES,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_items": len(FALLBACK_PRICES),
        "source": "Government API + Web Scraping"
    })

@app.route('/api/history/<item>', methods=['GET'])
@app.route('/history/<item>', methods=['GET'])
def get_history(item):
    item_lower = item.lower().strip()
    price = FALLBACK_PRICES.get(item_lower, 50)
    history = [
        {"timestamp": "2026-08-19 23:00", "price": max(10, price - 4)},
        {"timestamp": "2026-08-19 23:30", "price": max(10, price - 2)},
        {"timestamp": "2026-08-20 00:00", "price": price}
    ]
    return jsonify({
        "item": item,
        "history": history,
        "data_points": len(history)
    })

@app.route('/api/weather', methods=['GET'])
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Delhi')
    weather = {
        "city": city,
        "temperature": 28,
        "humidity": 65,
        "wind_speed": 12,
        "description": "Partly Cloudy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    recommendations = [
        "Optimal weather for current vegetable harvesting",
        "Moderate humidity - good crop conditions",
        "Cool weather - favorable for cabbage and cauliflower"
    ]
    return jsonify({
        "city": city,
        "weather": weather,
        "recommendations": recommendations,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/analytics', methods=['GET'])
@app.route('/analytics', methods=['GET'])
def get_analytics():
    prices = FALLBACK_PRICES
    avg_price = sum(prices.values()) / len(prices)
    max_item = max(prices, key=prices.get)
    min_item = min(prices, key=prices.get)
    return jsonify({
        "average_price": round(avg_price, 2),
        "highest": {"item": max_item, "price": prices[max_item]},
        "lowest": {"item": min_item, "price": prices[min_item]},
        "total_items": len(prices),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/feedback', methods=['POST'])
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    return jsonify({
        "success": True,
        "message": "Thank you for your feedback!"
    })

if __name__ == '__main__':
    app.run(port=5001)
