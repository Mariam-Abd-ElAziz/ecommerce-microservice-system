from flask import Flask, request, jsonify
from mysql.connector import Error
import requests  # to call Inventory Service
from db import get_db_connection
app = Flask(__name__)

# Connect to MySQL
try:
    db_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="ecommerce_system"
    )
    cursor = db_conn.cursor(dictionary=True)
    print("Connected to MySQL database")
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit(1)

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

        if not customer_id or not products:
            return jsonify({"error": "Missing required fields (customer ID or no selected products)"}), 400


        # Calculate total amount
        total_amount = 0
        for p in products:
            try:
                inventory_response = requests.get(
                    "http://localhost:5002/api/inventory/price/" + str(p['product_id']),
                )
                unit_price = float(inventory_response.json()["unit_price"])
                total_amount += unit_price * p['quantity']
            except Exception as inv_err:
                print(f"failed to retreive the price: {type(inv_err).__name__}: {inv_err}")

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

    try:
        # Fetch order details
        cursor.execute(
            "SELECT * FROM orders WHERE order_id = %s",
            (order_id,)
        )
        order = cursor.fetchone()

        if not order:
            return jsonify({"error": "Order not found"}), 404

        # Fetch products for this order
        cursor.execute(
            "SELECT product_id, quantity FROM orders_products WHERE order_id = %s",
            (order_id,)
        )
        products = cursor.fetchall()

        return jsonify({
            "order": order,
            "products": products
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        db_conn.close()
if __name__ == '__main__':
    app.run(port=5001, debug=True)
    