# Customer Service

Flask-based Customer Service for the ecommerce-project microservices demo.

What it does:
- Exposes customer lookup and loyalty management endpoints backed by MySQL.

Files:
- `app.py` — Flask HTTP endpoints.
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

Default port: `5004`.

Endpoints:
- `GET /` — health check
- `GET /api/customers/<customer_id>` — get customer info
- `GET /api/customers/<customer_id>/orders` — proxy to order service to fetch customer orders
- `PUT /api/customers/<customer_id>/loyalty` — add loyalty points (expects JSON with `points`)

Notes:
- Update DB credentials in `db.py` or use environment variables for production.
- The service calls the Order Service at `http://localhost:5001/api/orders` — adjust if needed.
