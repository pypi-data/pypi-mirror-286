# dclean/labeling.py

import pandas as pd

def label_data(df: pd.DataFrame, labels: dict) -> pd.DataFrame:
    for col, label in labels.items():
        if col in df.columns:
            df[col] = df[col].map(label)
    return df
