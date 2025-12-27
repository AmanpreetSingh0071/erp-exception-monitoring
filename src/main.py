import pandas as pd
from rule_engine import apply_rules
from anomaly_detector import detect_anomalies


def main():
    # Load data
    df = pd.read_csv("data/integration_logs.csv")

    # Step 1: Rule-based ERP validation
    df = apply_rules(df)

    # Step 2: Anomaly detection
    df = detect_anomalies(df)

    # Final exception decision
    df["final_exception"] = df["exception_flag"] | df["anomaly_flag"]

    exceptions = df[df["final_exception"] == True]

    # Save outputs
    exceptions.to_csv("data/final_exceptions_report.csv", index=False)

    print(f"Total Transactions: {len(df)}")
    print(f"Rule-based Exceptions: {df['exception_flag'].sum()}")
    print(f"AI Anomalies: {df['anomaly_flag'].sum()}")
    print(f"Final Exceptions: {len(exceptions)}")


if __name__ == "__main__":
    main()