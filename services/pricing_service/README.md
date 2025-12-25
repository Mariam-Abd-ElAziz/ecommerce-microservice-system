# Pricing Service

Flask-based Pricing Service for the ecommerce-project microservices demo.

What it does:
- Calculates itemized pricing for a list of products, applying pricing rules (discounts) and regional taxes.
- Calls Inventory Service to fetch current unit prices and availability.

Files:
- `app.py` — Flask endpoint `/api/pricing/calculate`.
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

Default port: `5003`.

Endpoint:
- `POST /api/pricing/calculate` — expects JSON:

```json
{
  "products": [ { "product_id": 1, "quantity": 2 } ],
  "region": "Cairo"
}
```

Response includes itemized prices, applied discounts, tax rates, and a total amount.

Notes:
- Ensure Inventory Service (port `5002`) is running and MySQL contains `pricing_rules` and `tax_rates` tables.
- For production, move DB credentials into environment variables and add retries/timeouts and caching for inventory calls.
