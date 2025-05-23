import urllib.parse
import motor.motor_asyncio
from datetime import datetime
from app.config import MONGODB_URL, DB_NAME

# Define username and password for MongoDB Atlas
username = "shivankumar"
password = "Shivan123"


# Escape the username and password for URL safety
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# MongoDB Atlas Connection URI
MONGODB_ATLAS_URL = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.veyqf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Connect to MongoDB Atlas
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_ATLAS_URL)
db = client[DB_NAME]

# Define collection
responses_collection = db["email_responses"]
faqs_collection  = db["store_faqs"]

async def store_faq(question, answer):
    """Stores the FAQ in MongoDB Atlas."""
    faqs_doc = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.utcnow()
    }
    result = await faqs_collection.insert_one(faqs_doc)
    return str(result.inserted_id)


async def store_response(subject, email_body, ai_response, response_time, accuracy):
    """Stores the AI response in MongoDB Atlas."""
    response_doc = {
        "subject": subject,
        "email_body": email_body,
        "ai_response": ai_response,
        "response_time": response_time,
        "accuracy": accuracy,
        "timestamp": datetime.utcnow()
    }
    result = await responses_collection.insert_one(response_doc)
    return str(result.inserted_id)

async def clean_collection(collection_name):
    """Deletes all documents from the specified collection in MongoDB Atlas."""
    collection = db[collection_name]
    result = await collection.delete_many({})
    return result.deleted_count

async def get_all_faqs():
    """Retrieve all FAQs from MongoDB Atlas."""
    faqs_cursor = faqs_collection.find({})
    faqs = await faqs_cursor.to_list(length=None)
    return [{"Question": faq["question"], "Answer": faq["answer"]} for faq in faqs]

if __name__ == "__main__":
    import asyncio

    async def main():
        deleted_count = await clean_collection("store_faqs")
        print(f"Cleaned Successfully, {deleted_count} documents deleted.")

    asyncio.run(main())