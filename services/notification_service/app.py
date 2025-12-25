from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import requests
from db import get_db_connection
import logging
logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "notification Service running!"})

@app.route('/api/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()

    try:
        order_id = data['order_id']
        customer_id = data['customer_id']
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid input"}), 400
    
    customer_response = requests.get(
        f"http://localhost:5004/api/customers/{customer_id}"
    )

    if customer_response.status_code != 200:
        return jsonify({"error": "Customer not found"}), 404

    customer_data = customer_response.json()
    customer_email = customer_data['email']
    customer_phone = customer_data['phone']   
    
    inventory_response = requests.get(
        "http://localhost:5002/api/inventory/products"
    )

    inventory_status = "Items available"
    if inventory_response.status_code != 200:
        inventory_status = "Inventory status unavailable"
    
    notification_message = (
    f"Your order #{order_id} has been confirmed.\n"
    f"Status: {inventory_status}\n"
    f"Thank you for shopping with us!"
    )

    logging.info(f"EMAIL SENT TO: {customer_email}")
    logging.info(f"Subject: Order #{order_id} Confirmation")
    logging.info(f"Body: {notification_message}")

    logging.info(f"SMS SENT TO: {customer_phone}")
    logging.info(f"Message: Order #{order_id} confirmed.")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notification_log 
        (order_id, customer_id, notification_type, message)
        VALUES (%s, %s, %s, %s)
    """, (order_id, customer_id, "ORDER_CONFIRMATION", notification_message))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
    "status": "Notification sent successfully",
    "order_id": order_id,
    "customer_id": customer_id
    }), 200

if __name__ == '__main__':
    app.run(port=5005, debug=True)