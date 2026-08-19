from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add root directory to path so backend module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.logic import negotiate, get_current_prices, get_price_history, get_weather_data

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def health():
    return jsonify({"message": "MOL-BHAAV API is running!"})

@app.route('/api/deal', methods=['POST'])
def deal():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    product = data.get("item", "")
    seller_price = data.get("seller_price", 0)
    
    if isinstance(seller_price, str):
        seller_price = int(seller_price)
    
    if not product or seller_price == 0:
        return jsonify({"error": "Missing required fields"}), 400
    
    result = negotiate(product, seller_price, seller_price)
    return jsonify(result)

@app.route('/api/prices', methods=['GET'])
def get_prices():
    current_prices = get_current_prices()
    return jsonify({
        "prices": current_prices,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_items": len(current_prices),
        "source": "Government API + Web Scraping"
    })

@app.route('/api/history/<item>', methods=['GET'])
def get_history(item):
    history = get_price_history(item)
    return jsonify({
        "item": item,
        "history": history,
        "data_points": len(history)
    })

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Delhi')
    weather = get_weather_data(city)
    
    recommendations = []
    if weather['temperature'] > 30:
        recommendations.append("High temperature - good for summer crops like tomato, bhindi")
    if weather['humidity'] > 70:
        recommendations.append("High humidity - watch for fungal diseases")
    if weather['temperature'] < 25:
        recommendations.append("Cool weather - good for cabbage, cauliflower")
    
    return jsonify({
        "city": city,
        "weather": weather,
        "recommendations": recommendations,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    prices = get_current_prices()
    
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
