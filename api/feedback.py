from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    return jsonify({
        "success": True,
        "message": "Thank you for your feedback!"
    })
