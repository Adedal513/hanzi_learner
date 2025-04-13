import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not TELEGRAM_TOKEN:
        raise ValueError("Missing TELEGRAM TOKEN in environment variables.")
    

settings = Config()