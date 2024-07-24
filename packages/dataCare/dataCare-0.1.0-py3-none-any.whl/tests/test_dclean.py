# tests/test_dclean.py

import pytest
import pandas as pd
from dclean import clean_data, preprocess_data, label_data, anonymize_data

def test_clean_data():
    df = pd.DataFrame({
        'CustomerID': [1, 2, 2, 4, 5, None],
        'Name': ['Alice', 'Bob', 'Bob', 'David', 'Eva', 'Frank'],
        'Age': [25, 30, 30, None, 40, 50],
        'Income': [50000, 60000, 60000, 70000, None, 80000]
    })
    cleaned_df = clean_data(df)
    assert cleaned_df.shape[0] == 5

def test_preprocess_data():
    df = pd.DataFrame({
        'Age': [25, 30, None, 40],
        'Income': [50000, None, 60000, 80000]
    })
    preprocessed_df = preprocess_data(df, strategy='median')
    assert preprocessed_df.isnull().sum().sum() == 0

def test_anonymize_data():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie']
    })
    anonymized_df = anonymize_data(df)
    assert anonymized_df['Name'].str.startswith('Anon_').all()
