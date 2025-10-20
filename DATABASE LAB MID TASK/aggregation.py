from database import orders_col, products_col
from datetime import datetime, timedelta
from bson import ObjectId

reference_date = datetime(2025, 11, 20)
last_month = reference_date - timedelta(days=30)

def parse_timestamp(ts_field):
    """Parse timestamp field which may be a dict like {'$date': '...Z'} or a datetime."""
    if isinstance(ts_field, dict) and "$date" in ts_field:
        s = ts_field["$date"]
        # expect format like 2025-11-05T14:00:00Z
        try:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            try:
                return datetime.fromisoformat(s)
            except Exception:
                return None
    if isinstance(ts_field, datetime):
        return ts_field
    return None

print("Reference date:", reference_date)
print("Looking for orders after:", last_month)

# Count product occurrences for orders within the last month
counts = {}
for order in orders_col.find():
    ts = parse_timestamp(order.get("timestamp"))
    if not ts or ts < last_month:
        continue
    for p in order.get("products", []):
        pid_field = p.get("product_id")
        if isinstance(pid_field, dict) and "$oid" in pid_field:
            pid = pid_field["$oid"]
        else:
            # fallback to string representation
            pid = str(pid_field)
        qty = p.get("quantity", 1) or 1
        counts[pid] = counts.get(pid, 0) + int(qty)

top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

print("\nTop products (product_id - count - product name if found):")
if not top:
    print("No orders found in the last 30 days based on the reference date.")
for pid, cnt in top:
    name = None
    try:
        # try to lookup product by ObjectId if possible
        prod = products_col.find_one({"_id": ObjectId(pid)})
        if prod:
            name = prod.get("name")
    except Exception:
        # pid is not a valid ObjectId or lookup failed
        prod = None
    if not name:
        # try to match by string id stored in _id (in case products were inserted with string _id)
        prod = products_col.find_one({"_id": pid})
        if prod:
            name = prod.get("name")
    print(f"{pid} - {cnt} - {name or '(name not found)'}")