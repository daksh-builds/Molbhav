from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MANDI_PRICES = {
    "tomato": 40, "onion": 25, "potato": 18, "rice": 50, "wheat": 30,
    "apple": 120, "banana": 40, "mango": 80, "bhindi": 35, "cabbage": 20,
    "carrot": 30, "cauliflower": 35, "garlic": 60, "ginger": 100, "lemon": 150,
    "milk": 60, "paneer": 400, "chicken": 180, "egg": 6, "dal": 100
}

def negotiate(product, seller_price):
    product_lower = product.lower()
    
    if product_lower in MANDI_PRICES:
        mandi_price = MANDI_PRICES[product_lower]
        diff = seller_price - mandi_price
        
        if diff > 10:
            status = "LOSS"
            message = f"Aap zyada de rahe ho! Mandi rate ₹{mandi_price} hai."
        elif diff < -10:
            status = "PROFIT"
            message = f"Badhai ho! Bahut sasta mila. Mandi rate ₹{mandi_price} hai."
        else:
            status = "FAIR"
            message = "Theek bhaav hai, sauda ho sakta hai."
    else:
        mandi_price = seller_price
        status = "UNKNOWN"
        message = "Is item ka mandi rate available nahi hai."

    return {
        "item": product,
        "mandi_price": mandi_price,
        "seller_price": seller_price,
        "status": status,
        "message": message
    }

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
    
    result = negotiate(product, seller_price)
    return jsonify(result)
