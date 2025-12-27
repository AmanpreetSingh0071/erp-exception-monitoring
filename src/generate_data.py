import pandas as pd
import random
from datetime import datetime, timedelta

rows = []

integration_types = ["EDI_850", "EDI_856", "API_ORDER", "API_INVOICE"]
statuses = ["SUCCESS", "FAILED", "PENDING"]
error_codes = ["ERR_MISSING_FIELD", "ERR_TIMEOUT", "ERR_INVALID_VALUE", ""]

start_time = datetime(2024, 11, 1, 9, 0)

for i in range(10000):
    status = random.choices(
        statuses, weights=[0.85, 0.1, 0.05], k=1
    )[0]

    error = random.choice(error_codes) if status == "FAILED" else ""

    rows.append({
        "transaction_id": f"TXN{i+10000}",
        "order_id": f"SO{random.randint(30000, 40000)}",
        "integration_type": random.choice(integration_types),
        "status": status,
        "error_code": error,
        "processing_time_ms": random.randint(500, 6000),
        "retry_count": random.randint(0, 5) if status != "SUCCESS" else 0,
        "transaction_date": start_time + timedelta(seconds=i * 3)
    })

df = pd.DataFrame(rows)
df.to_csv("data/integration_logs.csv", index=False)

print("integration_logs.csv generated successfully")