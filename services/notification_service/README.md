# Notification Service

Flask-based Notification Service for the ecommerce-project microservices demo.

What it does:
- Sends order confirmation notifications (logs email/SMS) and records them in MySQL.

Files:
- `app.py` — Flask endpoints and notification logic.
- `db.py` — MySQL connection helper.
- `requirements.txt` — Python dependencies.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run (development):

```bash
python app.py
```

Default port: `5005`.

Endpoints:
- `GET /` — health check
- `POST /api/notifications/send` — send a notification for an order (expects `order_id` and `customer_id`)

Example `POST /api/notifications/send` payload:

```json
{
  "order_id": 123,
  "customer_id": 1
}
```

Notes:
- The service queries Customer Service at `http://localhost:5004` and Inventory Service at `http://localhost:5002`.
- Update DB credentials in `db.py` or use environment variables for production.
