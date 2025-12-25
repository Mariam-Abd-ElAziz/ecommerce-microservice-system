from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import requests
from db import get_db_connection

app = Flask(__name__)

@app.route('/api/pricing/calculate', methods=['POST'])
def calculate_pricing():
    try:
        data = request.get_json()
        products = data.get("products")
        region = data.get("region", "Cairo")

        if not products or not isinstance(products, list):
            return jsonify({"status": "error", "message": "No products provided"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        itemized = []
        total = 0.0

        for item in products:
            if "product_id" not in item or "quantity" not in item:
                return jsonify({"status": "error", "message": "Invalid product format"}), 400

            product_id = item["product_id"]
            quantity = item["quantity"]

            # Call Inventory Service
            inventory_response = requests.get(
                f"http://localhost:5002/api/inventory/check/{product_id}"
            )
            if inventory_response.status_code != 200:
                return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404

            product_data = inventory_response.json()
            base_price = float(product_data["unit_price"])

            subtotal = base_price * quantity

            # Discount
            cursor.execute(
                """
                SELECT discount_percentage
                FROM pricing_rules
                WHERE product_id=%s AND min_quantity <= %s
                ORDER BY min_quantity DESC
                LIMIT 1
                """,
                (product_id, quantity)
            )
            discount_row = cursor.fetchone()
            discount = float(discount_row["discount_percentage"]) if discount_row else 0.0

            discounted_price = subtotal * (1 - discount / 100)

            # Tax
            cursor.execute("SELECT tax_rate FROM tax_rates WHERE region=%s", (region,))
            tax_row = cursor.fetchone()
            tax_rate = float(tax_row["tax_rate"]) if tax_row else 0.0

            tax_amount = discounted_price * (tax_rate / 100)
            final_price = discounted_price + tax_amount

            itemized.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": base_price,
                "discount_percentage": discount,
                "tax_rate": tax_rate,
                "total_price": round(final_price, 2)
            })

            total += final_price

        cursor.close()
        conn.close()

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
