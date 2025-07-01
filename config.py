from dotenv import load_dotenv
import os

# Muat variabel dari .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    QUEUE_RESET_INTERVAL = 86400  # seconds -- 24 hours