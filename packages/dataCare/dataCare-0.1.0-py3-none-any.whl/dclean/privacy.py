# dclean/privacy.py

import pandas as pd
from cryptography.fernet import Fernet

def generate_key() -> bytes:
    return Fernet.generate_key()

def encrypt_data(data: str, key: bytes) -> str:
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

def anonymize_data(df: pd.DataFrame) -> pd.DataFrame:
    df['Name'] = df['Name'].apply(lambda x: f'Anon_{hash(x)}')
    return df
