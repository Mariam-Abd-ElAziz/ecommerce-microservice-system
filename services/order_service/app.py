import os
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Connect to MySQL using environment variables
try:
    db_conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "ecommerce_user"),
        password=os.getenv("DB_PASS", "secure_password"),
        database=os.getenv("DB_NAME", "ecommerce_system")
    )
    cursor = db_conn.cursor(dictionary=True)
    print("Connected to MySQL database")
except Error as e:
    print(f" Error connecting to MySQL: {e}")
    exit(1)

@app.route('/api/orders/create', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON payload received"}), 400

        customer_id = data.get('customer_id')
        products = data.get('products')
        total_amount = data.get('total_amount')

        if not customer_id or not products or not total_amount:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Insert order
        cursor.execute(
            "INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)",
            (customer_id, total_amount)
        )
        db_conn.commit()
        order_id = cursor.lastrowid

        # Insert products for the order
        for p in products:
            product_id = p.get('product_id')
            quantity = p.get('quantity')
            if not product_id or not quantity:
                continue  # skip invalid product entry
            cursor.execute(
                "INSERT INTO orders_products (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                (order_id, product_id, quantity)
            )
        db_conn.commit()

        return jsonify({
            "message": "Order created successfully",
            "order_id": order_id,
            "status": "CONFIRMED"
        }), 201

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as ex:
        return jsonify({"status": "error", "message": str(ex)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        cursor.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
        order = cursor.fetchone()
        if not order:
            return jsonify({"status": "error", "message": "Order not found"}), 404

        cursor.execute(
            "SELECT product_id, quantity FROM orders_products WHERE order_id=%s",
            (order_id,)
        )
        products = cursor.fetchall()
        order['products'] = products
        return jsonify(order), 200

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
