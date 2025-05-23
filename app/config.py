import os
from dotenv import load_dotenv
import urllib.parse
import motor.motor_asyncio
from datetime import datetime

# Define username and password for MongoDB Atlas
username = "shivansus848"
password = "Shivan12345"


# Escape the username and password for URL safety
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URL = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.dqcdowc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = os.getenv("DB_NAME", "email_response_agent")

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")

