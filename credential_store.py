from pathlib import Path

import pandas as pd


MAX_CREDENTIAL_LENGTH = 16
CREDENTIALS_PATH = Path(__file__).resolve().parent / "users.csv"
CREDENTIAL_COLUMNS = ["username", "password"]


def save_credentials(username: str, password: str) -> None:
    if not username or not password:
        raise ValueError("Both username and password are required.")
    if len(username) > MAX_CREDENTIAL_LENGTH or len(password) > MAX_CREDENTIAL_LENGTH:
        raise ValueError("Username and password must be 16 characters or fewer.")

    if CREDENTIALS_PATH.exists() and CREDENTIALS_PATH.stat().st_size > 0:
        credentials = pd.read_csv(
            CREDENTIALS_PATH,
            dtype=str,
            keep_default_na=False,
        )
        if list(credentials.columns) != CREDENTIAL_COLUMNS:
            raise ValueError("The credentials CSV has an unexpected format.")
    else:
        credentials = pd.DataFrame(columns=CREDENTIAL_COLUMNS)

    new_credential = pd.DataFrame(
        [{"username": username, "password": password}],
        columns=CREDENTIAL_COLUMNS,
    )
    credentials = pd.concat([credentials, new_credential], ignore_index=True)
    credentials.to_csv(CREDENTIALS_PATH, index=False)