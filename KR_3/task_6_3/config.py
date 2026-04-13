import os

from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE", "DEV").upper()
DOCS_USER = os.getenv("DOCS_USER", "docs_admin")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "docs_password")

if MODE not in {"DEV", "PROD"}:
    raise ValueError("MODE must be either DEV or PROD")
