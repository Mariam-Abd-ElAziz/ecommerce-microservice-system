from flask import Flask, jsonify, request
import requests
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "customer Service running!"})

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM customers WHERE customer_id = %s",
        (customer_id,)
    )

    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer), 200
@app.route('/api/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Verify customer exists
    cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_id = %s",
        (customer_id,)
    )
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Customer not found"}), 404

    # 2. Get all order IDs for this customer
    cursor.execute(
        "SELECT order_id FROM orders WHERE customer_id = %s",
        (customer_id,)
    )
    order_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    # 3. Fetch full details for each order using Order Service
    detailed_orders = []
    for order_id in order_ids:
        try:
            response = requests.get(f"http://localhost:5001/api/orders/{order_id}", timeout=5)
            response.raise_for_status()
            detailed_orders.append(response.json())
        except requests.RequestException:
            # Skip this order if the service call fails
            continue

    return jsonify(detailed_orders), 200

@app.route('/api/customers/<int:customer_id>/loyalty', methods=['PUT'])
def update_loyalty(customer_id):
    data = request.get_json()

    if 'points' not in data:
        return jsonify({"error": "Missing loyalty points"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE customers SET loyalty_points = loyalty_points + %s WHERE customer_id = %s",
        (data['points'], customer_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "Customer not found"}), 404

    cursor.close()
    conn.close()
    return jsonify({"status": "Loyalty points updated"}), 200

if __name__ == '__main__':
    app.run(port=5004) 