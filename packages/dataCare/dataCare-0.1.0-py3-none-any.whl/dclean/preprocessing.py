# dclean/preprocessing.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(df: pd.DataFrame, strategy='median', scale='standard') -> pd.DataFrame:
    if strategy == 'median':
        df = df.fillna(df.median())
    elif strategy == 'mean':
        df = df.fillna(df.mean())
    elif strategy == 'mode':
        df = df.fillna(df.mode().iloc[0])
    
    if scale == 'standard':
        scaler = StandardScaler()
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    return df
