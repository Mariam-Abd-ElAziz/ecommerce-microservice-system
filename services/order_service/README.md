# Order Service

Flask-based Order Service for the ecommerce-project microservices demo.

**What it does:**
- Receives order creation requests and persists orders to MySQL.
- Inserts order line items and notifies other services (inventory, customers, notifications).

**Files:**
- `app.py` — Flask application and HTTP endpoints.
- `db.py` — MySQL connection helper.
- `requirements.txt` — Python dependencies.

## Dependencies
Install dependencies into your environment:

```bash
pip install -r requirements.txt
```

## Configuration
`db.py` contains default local MySQL connection settings; move credentials to environment variables before production.

## Run
Start the service (development):

```bash
python app.py
```

Runs on port `5001` by default.

## Endpoints
- `GET /` — health check
- `POST /api/orders/create` — create an order (JSON body)
- `GET /api/orders/<order_id>` — fetch order and its products

Example `POST /api/orders/create` payload:

```json
{
  "customer_id": 1,
  "products": [ { "product_id": 10, "quantity": 2 } ],
  "total_amount": 39.98
}
```

## Notes
- The service calls other local services for inventory, loyalty, and notifications at ports `5002`, `5004`, and `5005` — ensure those services are running or update the URLs.
- For production, secure DB credentials, add retries/timeouts and better error handling, and consider using a message queue for durable inter-service communication.
