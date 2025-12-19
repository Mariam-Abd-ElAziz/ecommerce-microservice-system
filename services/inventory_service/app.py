from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Connect to MySQL
try:
    db_conn = mysql.connector.connect(
        host="localhost",
        user="ecommerce_user",
        password="secure_password",
        database="ecommerce_system"
    )
    cursor = db_conn.cursor(dictionary=True)
    print("Connected to MySQL database")
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit(1)

# Check stock availability
@app.route('/api/inventory/check/<int:product_id>', methods=['GET'])
def check_inventory(product_id):
    try:
        cursor.execute("SELECT * FROM inventory WHERE product_id=%s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"status": "error", "message": "Product not found"}), 404
        return jsonify(product), 200
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Update inventory automatically
@app.route('/api/inventory/update', methods=['POST'])
def update_inventory():
    """
    Automatically decrement stock for products based on an order.
    Expects JSON:
    {
        "products": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 4, "quantity": 1}
        ]
    }
    """
    try:
        data = request.get_json()
        products = data.get("products")
        if not products or not isinstance(products, list):
            return jsonify({"status": "error", "message": "No products provided"}), 400

        updated_products = []

        for item in products:
            product_id = item["product_id"]
            quantity = item["quantity"]

            cursor.execute(
                "SELECT quantity_available FROM inventory WHERE product_id=%s",
                (product_id,)
            )
            product = cursor.fetchone()
            if not product:
                updated_products.append({
                    "product_id": product_id,
                    "status": "error",
                    "message": "Product not found"
                })
                continue

            current_quantity = product["quantity_available"]
            new_quantity = current_quantity - quantity
            if new_quantity < 0:
                updated_products.append({
                    "product_id": product_id,
                    "status": "error",
                    "message": "Not enough stock"
                })
                continue

            cursor.execute(
                "UPDATE inventory SET quantity_available=%s, last_updated=NOW() WHERE product_id=%s",
                (new_quantity, product_id)
            )
            updated_products.append({
                "product_id": product_id,
                "old_quantity": current_quantity,
                "new_quantity": new_quantity,
                "status": "success"
            })

        db_conn.commit()
        return jsonify({"status": "completed", "updated_products": updated_products}), 200

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5002, debug=True)
