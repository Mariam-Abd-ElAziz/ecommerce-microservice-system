# Inventory Service

Lightweight Flask-based Inventory Service for the ecommerce-project microservices demo.

**What it does:**
- Exposes inventory lookup and update endpoints backed by MySQL.

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
By default `db.py` contains connection settings for a local MySQL instance. Update `db.py` or move credentials to environment variables before production use.

## Run
Start the service (development):

```bash
python app.py
```

The service runs on port `5002` by default.

## Endpoints
- `GET /` — health check
- `GET /api/inventory/products` — list available products
- `GET /api/inventory/check/<product_id>` — check a product's stock
- `POST /api/inventory/update` — decrement inventory for ordered products (expects JSON list of products)

Example `POST /api/inventory/update` payload:

```json
{
  "products": [ { "product_id": 1, "quantity": 2 } ]
}
```

## Notes
- Ensure a MySQL server with the expected schema is available and reachable.
- The service is intended for development/demo use; add retries, auth, and configuration management for production.
