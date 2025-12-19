from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import requests

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

@app.route('/api/pricing/calculate', methods=['POST'])
def calculate_pricing():
    """
    Calculate final pricing for an order.
    Request JSON:
    {
        "products": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ],
        "region": "Cairo"   # optional for tax calculation
    }
    """
    try:
        data = request.get_json()
        products = data.get("products")
        region = data.get("region", "Cairo")  # default region

        if not products or not isinstance(products, list):
            return jsonify({"status": "error", "message": "No products provided"}), 400

        itemized = []
        total = 0.0

        for item in products:
            product_id = item["product_id"]
            quantity = item["quantity"]

            # Get base price from Inventory Service
            inventory_response = requests.get(
                f"http://localhost:5002/api/inventory/check/{product_id}"
            )
            if inventory_response.status_code != 200:
                return jsonify({"status": "error", "message": f"Product {product_id} not found in inventory"}), 404

            product_data = inventory_response.json()
            base_price = float(product_data["unit_price"])

            # Check for discount rules
            cursor.execute(
                "SELECT discount_percentage, min_quantity FROM pricing_rules WHERE product_id=%s",
                (product_id,)
            )
            discount_row = cursor.fetchone()
            discount = 0.0
            if discount_row and quantity >= discount_row["min_quantity"]:
                discount = float(discount_row["discount_percentage"])

            price_after_discount = base_price * quantity * (1 - discount / 100)

            # Apply tax
            cursor.execute("SELECT tax_rate FROM tax_rates WHERE region=%s", (region,))
            tax_row = cursor.fetchone()
            tax_rate = float(tax_row["tax_rate"]) if tax_row else 0.0

            price_with_tax = price_after_discount * (1 + tax_rate / 100)

            itemized.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": base_price,
                "discount_percentage": discount,
                "tax_rate": tax_rate,
                "total_price": round(price_with_tax, 2)
            })

            total += price_with_tax

        return jsonify({
            "status": "success",
            "total_amount": round(total, 2),
            "items": itemized
        }), 200

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as ex:
        return jsonify({"status": "error", "message": str(ex)}), 500

if __name__ == "__main__":
    app.run(port=5003, debug=True)
