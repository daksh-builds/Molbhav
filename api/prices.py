from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

MANDI_PRICES = {
    "tomato": 40, "onion": 25, "potato": 18, "rice": 50, "wheat": 30,
    "apple": 120, "banana": 40, "mango": 80, "bhindi": 35, "cabbage": 20,
    "carrot": 30, "cauliflower": 35, "garlic": 60, "ginger": 100, "lemon": 150,
    "milk": 60, "paneer": 400, "chicken": 180, "egg": 6, "dal": 100
}

@app.route('/api/prices', methods=['GET'])
def get_prices():
    return jsonify({
        "prices": MANDI_PRICES,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_items": len(MANDI_PRICES)
    })
