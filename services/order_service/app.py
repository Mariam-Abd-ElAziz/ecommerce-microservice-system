from flask import Flask, request, jsonify
from mysql.connector import Error, IntegrityError
import requests
from db import get_db_connection

app = Flask(__name__)

@app.route('/api/orders/review', methods=['POST'])
def review_order():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        customer_id = data.get('customer_id')
        products = data.get('products') or data.get('items')

        if not customer_id:
            return jsonify({"error": "Customer ID is required"}), 400

        if not products or len(products) == 0:
            return jsonify({"error": "No products selected"}), 400

        # Check stock
        for p in products:
            if p['quantity'] <= 0:
                return jsonify({"error": f"Quantity must be > 0 for product {p['product_id']}"}), 400
            try:
                inventory_res = requests.get(f"http://localhost:5002/api/inventory/check/{p['product_id']}")
                inventory_res.raise_for_status()
                available_qty = inventory_res.json().get("quantity_available")
                if p['quantity'] > available_qty:
                    return jsonify({
                        "error": "OutOfStock",
                        "message": f"Product {p['product_id']} has only {available_qty} items available, you requested {p['quantity']}."
                    }), 400
            except requests.exceptions.RequestException as e:
                return jsonify({"error": "Inventory service unavailable", "details": str(e)}), 500

        # Get total amount
        try:
            pricing_payload = {"products": products, "region": data.get("region", "Cairo")}
            pricing_res = requests.post("http://localhost:5003/api/pricing/calculate",
                                        json=pricing_payload, timeout=5)
            pricing_res.raise_for_status()
            pricing_json = pricing_res.json()
            if pricing_json.get("status") != "success":
                return jsonify({
                    "error": "Pricing calculation failed",
                    "message": pricing_json.get("message", "Unknown error")
                }), 400

            total_amount = float(pricing_json["total_amount"])
            itemized_prices = pricing_json["items"]

        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Pricing service unavailable", "details": str(e)}), 500

        return jsonify({"status": "success", "items": itemized_prices, "total_amount": total_amount})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500






@app.route('/api/orders/create', methods=['POST'])
def create_order():
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        customer_id = data.get('customer_id')
        products = data.get('products') or data.get('items')

        if not customer_id:
            return jsonify({"error": "Customer ID is required"}), 400

        if not products or len(products) == 0:
            return jsonify({"error": "No products selected"}), 400


        # ------------------------------
        # 2️⃣ Get total amount from Pricing Service
        # ------------------------------
        try:
            pricing_payload = {
                "products": products,
                "region": data.get("region", "Cairo")
            }
            pricing_res = requests.post(
                "http://localhost:5003/api/pricing/calculate",
                json=pricing_payload,
                timeout=5
            )
            pricing_res.raise_for_status()  # Raise exception if status != 200

            pricing_json = pricing_res.json()
            if pricing_json.get("status") != "success":
                return jsonify({
                    "error": "Pricing calculation failed",
                    "message": pricing_json.get("message", "Unknown error")
                }), 400

            total_amount = float(pricing_json["total_amount"])
            # Optionally, store itemized prices per product if needed
            itemized_prices = pricing_json["items"]

        except requests.exceptions.RequestException as e:
            return jsonify({
                "error": "Pricing service unavailable",
                "details": str(e)
            }), 500


        # ------------------------------
        # 3️⃣ Insert order
        # ------------------------------
        try:
            cursor.execute(
                "INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)",
                (customer_id, total_amount)
            )
            db_conn.commit()
            order_id = cursor.lastrowid
        except IntegrityError:
            return jsonify({"error": "Invalid customer ID. Please check your entries."}), 400

        # ------------------------------
        # 4️⃣ Insert products for the order
        # ------------------------------
        for p in products:
            if p['quantity'] <= 0:
                return jsonify({"error": "Quantity must be greater than 0"}), 400
            try:
                cursor.execute(
                    "INSERT INTO orders_products (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, p['product_id'], p['quantity'])
                )
            except IntegrityError:
                return jsonify({
                    "error": f"Product ID {p['product_id']} is invalid or does not exist."
                }), 400
        db_conn.commit()

        # ------------------------------
        # 5️⃣ Automatically update inventory
        # ------------------------------
        try:
            inv_update_res = requests.post(
                "http://localhost:5002/api/inventory/update",
                json={"products": products}
            )
            print("Inventory update response:", inv_update_res.json())
        except Exception as e:
            print("Inventory update failed:", e)

        # ------------------------------
        # 6️⃣ Update loyalty points
        # ------------------------------
        try:
            requests.put(
                f"http://localhost:5004/api/customers/{customer_id}/loyalty",
                json={"points": 10},
                timeout=3
            )
        except Exception as e:
            print("Loyalty update failed:", e)

        # ------------------------------
        # 7️⃣ Send notification
        # ------------------------------
        try:
            requests.post(
                "http://localhost:5005/api/notifications/send",
                json={"order_id": order_id, "customer_id": customer_id},
                timeout=3
            )
        except Exception as e:
            print("Notification failed:", e)

        # ------------------------------
        # 8️⃣ Return success
        # ------------------------------
        return jsonify({"order_id": order_id, "total_amount": total_amount, "items": itemized_prices, "status": "success"}), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        db_conn.close()




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
    