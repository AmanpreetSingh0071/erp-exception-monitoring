import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply anomaly detection to ERP integration logs
    to flag unusual transaction behaviour.
    """

    df = df.copy()

    # Encode categorical values
    le = LabelEncoder()
    df["integration_type_encoded"] = le.fit_transform(df["integration_type"])
    df["status_encoded"] = le.fit_transform(df["status"])

    features = df[
        [
            "processing_time_ms",
            "retry_count",
            "integration_type_encoded",
            "status_encoded",
        ]
    ]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.03,
        random_state=42
    )

    df["anomaly_flag"] = model.fit_predict(features)
    df["anomaly_flag"] = df["anomaly_flag"].map({1: False, -1: True})

    return df