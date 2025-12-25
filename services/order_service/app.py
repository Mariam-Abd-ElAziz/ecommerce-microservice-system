from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import requests  # to call Inventory Service

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
    try:
        data = request.get_json()
        customer_id = data['customer_id']
        products = data['products']

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

        return jsonify({"order_id": order_id, "status": "success"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
