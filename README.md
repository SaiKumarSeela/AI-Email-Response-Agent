# Email_Agent
# AI Email Response Agent

This project is an AI-powered email response agent that automatically generates replies to incoming emails. It leverages a large language model (LLM) to understand the context of emails and craft relevant, professional responses. The system also includes features for storing responses, and providing dashboard statistics.

## Features

-   **Automated Email Response:** Uses the Mistral-7B-Instruct-v0.1 LLM to generate intelligent responses to email queries.
-   **Response Time Tracking:** Measures and records the time taken to generate each response.
-   **Accuracy Evaluation:** Employs an accuracy evaluation mechanism to assess the quality of the generated responses.
-   **Data Storage:** Stores email queries, AI responses, response times, and accuracy ratings in a MongoDB database.
-   **Asynchronous Operations:** Uses background tasks to handle database storage without blocking the main application flow.

## Technologies Used

-   **FastAPI:** For building the web API.
-   **Uvicorn:** For running the ASGI server.
-   **MongoDB:** For storing email data.
-   **Motor:** For asynchronous MongoDB operations.
-   **LangChain:** For interacting with the LLM.
-   **Hugging Face Transformers:** For the Mistral-7B-Instruct-v0.1 model.
-   **Python-dotenv:** For managing environment variables.
-   **Pydantic:** For data validation and settings management.
-   **Torch:** For tensor operations with the LLM.
-   **Accelerate:** For model acceleration.

## Project Structure
```
Email-Agent/
├── app/
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Environment variable configuration
│   ├── models/               # Pydantic models for validation
│   │   └── schemas.py        # Data schemas (EmailQuery)
│   ├── services/             # Core services (LLM, DB)
│   │   ├── llm_service.py
│   │   └── db_service.py
│   └── utils/                # Utility scripts (Evaluator)
├── .env                      # Environment variables
├── requirements.txt          # Dependencies list
└── README.md                 # Project documentation
```
 

## Setup and Installation

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd Email
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**

    -   Create a `.env` file in the root directory of the project.
    -   Add the following environment variables (replace with your actual values):

    ```properties
    # MongoDB Configuration
    MONGODB_URL=mongodb://localhost:27017
    DB_NAME=Simple_email_response_agent

    # Model Configuration
    MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
    MODEL_API_KEY=your_huggingface_api_key
    ```
    -   **Note:** For `MODEL_API_KEY`, you need to create a Hugging Face account and get an API key from your settings.

5.  **Run MongoDB:**

    -   Ensure that MongoDB is running on your local machine (or update `MONGODB_URL` in `.env` if using a remote instance).

6.  **Run the Application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    -   This will start the FastAPI application. You can access the API at `http://127.0.0.1:8000`.

## API Endpoints

-   **`POST /api/generate-response`**
    -   **Description:** Processes an email query and generates an AI response.
    -   **Request Body:**

        ```json
        {
            "subject": "Inquiry About Product Availability",
            "email_body": "Hello, I am interested in purchasing the XYZ Smartwatch. Can you confirm if it's available in stock and provide details on the delivery time?"
        }
        ```

    -   **Response Body:**

        ```json
        {
            "ai_response": "Hello, thank you for your interest in the XYZ Smartwatch! Yes, the product is currently in stock. Standard delivery takes 3-5 business days, while express shipping takes 1-2 business days. Let us know if you need further assistance.",
            "response_time": 1.45,
            "accuracy": 4,
            "response_id": "65xythjlxx9xx"
        }
        ```

---

## MongoDB Setup
### Database Connection
**File**: `app/services/db_service.py`

```python
 import motor.motor_asyncio
 from app.config import MONGODB_URL, DB_NAME
 
 # Connect to MongoDB
 client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
 db = client[DB_NAME]
 responses_collection = db["email_responses"]
```
## Database Schema
### email_responses Collection:
 ```python 
 response_doc = {
     "subject": subject,
     "email_body": email_body,
     "ai_response": ai_response,
     "response_time": response_time,
     "accuracy": accuracy,
     "timestamp": datetime.utcnow()
 }
```
- subject: (string) Email subject.
- email_body: (string) Email content.
- ai_response: (string) AI-generated response.
- response_time: (float) Time taken to generate response.
- accuracy: (integer) AI response accuracy (1-5).
- timestamp: (datetime) Time response was generated.

## Storing Data
### Function: store_response()
 ```python 
 async def store_response(subject, email_body, ai_response, response_time, accuracy):
     result = await responses_collection.insert_one(response_doc)
     return str(result.inserted_id)
```
- Stores AI responses in MongoDB.
- Returns the document ID of the stored response.

----------------
## To view a MongoDB database on your computer using its database name, follow these steps:

 - ## Using MongoDB Compass (GUI)

   1. Download & Install MongoDB Compass.

   2. Connect to MongoDB

      - Open Compass and enter your MongoDB connection string:

        ```
        mongodb://localhost:27017
        ```
      - Click "Connect".

   3. Select Your Database

      - Find your database in the left panel.

      - Click on it to explore collections and documents.

-----------
**Email Responses**
![Image](https://github.com/user-attachments/assets/b568828a-263e-4bd5-a107-02ffbe730e6f)


**Project Video Demo**

https://github.com/user-attachments/assets/398d26e3-70dc-4bb8-9dc5-6ec104990f53


------
## Future Improvements
- Advanced Accuracy Evaluation: Implement a more sophisticated model for evaluating response accuracy.
- Model Fine-tuning: Fine-tune the LLM on a dataset of email responses to improve performance.
- Error Handling: Add more robust error handling and logging.
- Security: Implement security measures for the API and data storage.
- UI: Create a user interface for interacting with the system.
- More Dashboard Stats: Add more stats to the dashboard.

----

### Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.

--------
### License
MIT License (or specify your preferred license)


