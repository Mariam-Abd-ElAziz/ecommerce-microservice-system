from flask import Flask, request, jsonify
from mysql.connector import Error
from db import get_db_connection
app = Flask(__name__)

@app.route('/')
def home():
    return "Inventory service is running!"

# Get all available products
@app.route('/api/inventory/products', methods=['GET'])
def retreive_inventory():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT product_name, unit_price , quantity_available 
            FROM inventory
            WHERE quantity_available > 0
        """)

        rows = cursor.fetchall()

        products = [
        {
        "product_name": row["product_name"],
        "unit_price": float(row["unit_price"]) ,
        "quantity_available": row["quantity_available"]
        }
        for row in rows
        ]

        if not products:
            print("No available products found")
            return jsonify({"status": "inventory_empty", "message": "all products are currently unavailable"}), 200
        
        print("Retrieved available products:", products)
        return jsonify(products), 200
    
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Check stock availability
@app.route('/api/inventory/check/<int:product_id>', methods=['GET'])
def check_inventory(product_id):
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM inventory WHERE product_id=%s", (product_id, ))
        product = cursor.fetchone()
        if not product:
            return jsonify({"status": "error", "message": "Product not found"}), 404
        return jsonify(product), 200
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
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

        conn.commit()
        return jsonify({"status": "completed", "updated_products": updated_products}), 200

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(port=5002, debug=True)
