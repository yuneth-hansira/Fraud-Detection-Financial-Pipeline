from datetime import datetime, timedelta
import random
import csv

# Optional: use Faker/pandas if available, otherwise fall back to stdlib
try:
    # pyrefly: ignore [missing-import]
    from faker import Faker
    fake = Faker()
except Exception:
    fake = None

try:
    # pyrefly: ignore [missing-import]
    import pandas as pd
except Exception:
    pd = None


def generate_nic():
    # Synthetic Sri Lankan-style NIC format
    return f"{random.randint(1950, 2005)}{random.randint(1,366):03d}{random.randint(1000,9999)}"


def random_datetime(start, end):
    delta = end - start
    int_delta = int(delta.total_seconds())
    rand_second = random.randint(0, int_delta)
    return start + timedelta(seconds=rand_second)


def generate_record():
    is_fraud = random.random() < 0.05  # 5% chance of fraud

    if is_fraud:
        amount = round(random.uniform(500000, 5000000), 2)  # Higher transfer amount
    else:
        amount = round(random.uniform(100, 500000), 2)

    # transaction datetime
    if fake:
        tx_dt = fake.date_time_between(start_date='-1y', end_date='now')
    else:
        start = datetime.now() - timedelta(days=365)
        end = datetime.now()
        tx_dt = random_datetime(start, end)
    tx_dt_iso = tx_dt.isoformat()

    return {
        "nic_id": generate_nic(),
        "username": fake.user_name() if fake else f"user{random.randint(1000,9999)}",
        "mobile_number": f"07{random.randint(10000000,99999999)}",
        "bank_account": str(random.randint(100000000000,999999999999)),
        "amount_transferred": amount,
        "transaction_datetime": tx_dt_iso,
        "location": ("Unknown" if is_fraud else (f"{fake.city()}, {fake.country()}" if fake else "Colombo, Sri Lanka")),
        "ip_address": (fake.ipv4() if fake else ".".join(str(random.randint(0,255)) for _ in range(4))),
        "is_fraud": 1 if is_fraud else 0
    }


def main():
    records = [generate_record() for _ in range(1000)]

    if pd:
        df = pd.DataFrame(records)
        df.to_csv("transactions.csv", index=False)
        print("transactions.csv updated successfully with 1000 records.")
    else:
        fieldnames = ["nic_id", "username", "mobile_number", "bank_account", "amount_transferred", "transaction_datetime", "location", "ip_address", "is_fraud"]
        with open("transactions.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(r)
        print("transactions.csv updated successfully with 1000 records.")


if __name__ == "__main__":
    main()
