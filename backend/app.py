from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from logic import negotiate, get_current_prices, get_price_history, get_weather_data
from datetime import datetime
import io
import base64

app = Flask(__name__, static_folder="../")
CORS(app)

@app.route("/")
def home():
    return send_from_directory("../", "index.html")

@app.route("/deal", methods=["POST"])
def deal():
    data = request.json
    print("Received data:", data)
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    product = data.get("item", "")
    seller_price = data.get("seller_price", 0)
    
    if isinstance(seller_price, str):
        seller_price = int(seller_price)
    
    print(f"Product: {product}, Seller Price: {seller_price}")
    
    if not product or seller_price == 0:
        return jsonify({"error": "Missing required fields"}), 400
    
    result = negotiate(product, seller_price, seller_price)
    return jsonify(result)

@app.route("/prices", methods=["GET"])
def get_prices():
    """Get all current mandi prices with timestamp"""
    current_prices = get_current_prices()
    return jsonify({
        "prices": current_prices,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_items": len(current_prices),
        "source": "Government API + Web Scraping"
    })

@app.route("/history/<item>", methods=["GET"])
def get_history(item):
    """Get price history for an item"""
    history = get_price_history(item)
    return jsonify({
        "item": item,
        "history": history,
        "data_points": len(history)
    })

@app.route("/weather", methods=["GET"])
def get_weather():
    """Get weather data for crop predictions"""
    city = request.args.get('city', 'Delhi')
    weather = get_weather_data(city)
    
    # Add crop recommendations based on weather
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

@app.route("/analytics", methods=["GET"])
def get_analytics():
    """Get market analytics"""
    prices = get_current_prices()
    
    # Calculate statistics
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

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    """Submit user feedback"""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    print(f"Feedback received: {data}")
    
    return jsonify({
        "success": True,
        "message": "Thank you for your feedback!"
    })

if __name__ == "__main__":
    print("🚀 Starting MOL-BHAAV Backend...")
    print("📊 Features enabled:")
    print("  ✅ Government API Integration")
    print("  ✅ Web Scraping (Agmarknet)")
    print("  ✅ Historical Price Tracking")
    print("  ✅ Weather Integration")
    print("  ✅ Price Trend Predictions")
    print("  ✅ Market Analytics")
    app.run(debug=False, port=5001)
