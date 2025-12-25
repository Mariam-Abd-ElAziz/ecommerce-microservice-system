from flask import Flask, request, jsonify
from mysql.connector import Error
import requests  # to call Inventory Service
from db import get_db_connection
app = Flask(__name__)

@app.route('/')
def home():
    return "Order service is running!"

@app.route('/api/orders/create', methods=['POST'])
def create_order():
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        customer_id = data['customer_id']
        products = data['products']
        total_amount = data['total_amount']
        if not customer_id or not products or total_amount is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Insert order
        cursor.execute(
            "INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)",
            (customer_id, total_amount)
        )
        db_conn.commit()
        order_id = cursor.lastrowid

        # Insert products for the order
        for p in products:
            if p['quantity'] <= 0:
                return jsonify({"error": "Quantity must be > 0"}), 400
            cursor.execute(
                "INSERT INTO orders_products (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                (order_id, p['product_id'], p['quantity'])
            )
        db_conn.commit()

        # Automatically update inventory
        try:
            inventory_response = requests.post(
                "http://localhost:5002/api/inventory/update",
                json={"products": products}
            )
            print("Inventory update response:", inventory_response.json())
        except Exception as inv_err:
            print(f"Failed to update inventory: {inv_err}")

        #Automatically update customer loyalty points
        try:
            requests.put(
                f"http://localhost:5004/api/customers/{customer_id}/loyalty",
                json={"points": 10},
                timeout=3
            )
        except Exception as e:
            print("Loyalty update failed:", e)

        #Automatically send notification

        try:
            requests.post(
                "http://localhost:5005/api/notifications/send",
                json={
                    "order_id": order_id,
                    "customer_id": customer_id
                },
                timeout=3
            )
        except Exception as e:
            print("Notification failed:", e)


        return jsonify({"order_id": order_id, "status": "success"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)
    cursor.execute(
    "SELECT * FROM orders WHERE order_id = %s",
    (order_id,)
    )
    order = cursor.fetchone()

    if not order:
        cursor.close()
        db_conn.close()
        return jsonify({"error": "Order not found"}), 404
    
    cursor.execute(
        "SELECT product_id, quantity FROM orders_products WHERE order_id = %s",
        (order_id,)
    )
    products = cursor.fetchall()

    cursor.close()
    db_conn.close()

    return jsonify({
        "order": order,
        "products": products
    }), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
                    