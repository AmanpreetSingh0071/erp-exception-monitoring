import pandas as pd

# ERP-style thresholds
MAX_PROCESSING_TIME_MS = 3000
MAX_RETRY_COUNT = 2


def apply_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply deterministic ERP rules to integration logs
    and flag known exception scenarios.
    """

    df = df.copy()
    df["exception_flag"] = False
    df["exception_types"] = ""

    for idx, row in df.iterrows():
        exceptions = []

        # Rule 1: Failed transaction
        if row["status"] == "FAILED":
            exceptions.append("FAILED_TRANSACTION")

        # Rule 2: Pending transaction exceeding SLA
        if row["status"] == "PENDING" and row["processing_time_ms"] > MAX_PROCESSING_TIME_MS:
            exceptions.append("PENDING_SLA_BREACH")

        # Rule 3: Processing time exceeded
        if row["processing_time_ms"] > MAX_PROCESSING_TIME_MS:
            exceptions.append("PROCESSING_TIME_EXCEEDED")

        # Rule 4: Excessive retries
        if row["retry_count"] > MAX_RETRY_COUNT:
            exceptions.append("RETRY_LIMIT_EXCEEDED")

        # Rule 5: Missing critical data
        if not row["order_id"]:
            exceptions.append("MISSING_ORDER_ID")

        if row["status"] == "FAILED" and not row["error_code"]:
            exceptions.append("MISSING_ERROR_CODE")

        if exceptions:
            df.at[idx, "exception_flag"] = True
            df.at[idx, "exception_types"] = ",".join(exceptions)

    return df