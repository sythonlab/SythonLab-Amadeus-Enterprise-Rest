import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

AMADEUS_CONFIG = {
    'API_URL': os.getenv('AMADEUS_API_URL'),
    'CLIENT_ID': os.getenv('AMADEUS_CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('AMADEUS_CLIENT_SECRET'),
}
