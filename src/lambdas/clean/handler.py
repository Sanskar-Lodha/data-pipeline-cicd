import csv
import io


def clean_rows(rows):
    """Pure logic: takes a list of dicts, returns cleaned list of dicts."""
    seen = set()
    cleaned = []
    for row in rows:
        # standardize column names: lowercase, underscores
        row = {k.strip().lower().replace(" ", "_"): v.strip() for k, v in row.items()}

        # drop rows missing required fields
        if not row.get("order_id") or not row.get("amount"):
            continue

        # validate amount is a positive number
        try:
            row["amount"] = float(row["amount"])
        except ValueError:
            continue
        if row["amount"] < 0:
            continue

        # remove duplicates by order_id
        if row["order_id"] in seen:
            continue
        seen.add(row["order_id"])

        cleaned.append(row)
    return cleaned


def parse_csv(text):
    return list(csv.DictReader(io.StringIO(text)))


def lambda_handler(event, context):
    """AWS plumbing: thin wrapper. Real S3 I/O comes in a later step."""
    rows = parse_csv(event["csv_text"])
    cleaned = clean_rows(rows)
    return {"cleaned_count": len(cleaned)}