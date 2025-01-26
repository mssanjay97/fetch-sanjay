# Python version of the receipt processor
from flask import Flask, request, jsonify
import uuid
import math
import re

app = Flask(__name__)

receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.get_json()
    if not receipt:
        return jsonify({"error": "Invalid JSON"}), 400

    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts[receipt_id] = points

    return jsonify({"id": receipt_id})

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = receipts.get(receipt_id)
    if points is None:
        return jsonify({"error": "Receipt not found"}), 404

    return jsonify({"points": points})

def calculate_points(receipt):
    points = 0

    retailer = receipt.get("retailer", "")
    points += len(re.findall(r'[a-zA-Z0-9]', retailer))

    total = float(receipt.get("total", 0))
    if total == math.floor(total):
        points += 50

    if total % 0.25 == 0:
        points += 25

    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    for item in items:
        description = item.get("shortDescription", "").strip()
        price = float(item.get("price", 0))
        if len(description) % 3 == 0:
            points += math.ceil(price * 0.2)

    purchase_date = receipt.get("purchaseDate", "")
    if purchase_date:
        day = int(purchase_date.split("-")[2])
        if day % 2 != 0:
            points += 6

    purchase_time = receipt.get("purchaseTime", "")
    if purchase_time:
        hour, minute = map(int, purchase_time.split(":"))
        if 14 <= hour < 16:
            points += 10

    return points

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
