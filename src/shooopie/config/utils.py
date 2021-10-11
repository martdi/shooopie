import os
import secrets
from pathlib import Path

SECRET_FILE = 'secret.txt'

def get_or_generate_secret():
    settings_dir = Path(__file__).resolve().parent
    secret_file_path = settings_dir / SECRET_FILE

    if not os.path.isfile(secret_file_path):
        with open(secret_file_path, 'w') as f:
            f.write(secrets.token_hex(256))

    with open(secret_file_path) as f:
        return f.read().strip()


