import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

class Config:
    DB_HOST=os.getenv("MYSQL_HOST", "localhost")
    DB_USER=os.getenv("MYSQL_USER", "root")
    DB_PW=os.getenv("MYSQL_PASSWORD", "rootpassword")
    DB_NAME=os.getenv("MYSQL_DB", "mydb")
    
    API_URL=os.getenv("API_URL", "127.0.0.1")
    API_PORT=os.getenv("API_HOST", "8000")
    
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "jwt_sercret_key")
    