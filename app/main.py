from fastapi import FastAPI, HTTPException, UploadFile, Form, File
from app.models.schemas import EmailQuery, EmailResponse
from app.services.llm_service import generate_response_with_faq, generate_generic_response, generate_faqs_from_web
from app.services.db_service import store_response, store_faq, get_all_faqs
from app.utils.evaluator import evaluate_response_accuracy
from app.services.file_handler import parse_faq_file, download_and_parse_public_google_drive_file, extract_website_content
from app.services.faiss_service import faq_indexer
import time
import asyncio
from dotenv import load_dotenv
import os
# from concurrent.futures import ThreadPoolExecutor
from typing import Optional
# from crawl4ai import AsyncWebCrawler
app = FastAPI(title="AI Email Response Agent")
from fastapi import HTTPException, Form, APIRouter
global web_content
global is_web
is_web = False
web_content = ""

# Load environment variables
load_dotenv()

@app.post("/api/upload-faq-file")
async def upload_faq_file(file: UploadFile = File(...)):
    """
    Upload a CSV or Excel file containing FAQ data.
    
    :param file: Uploaded file containing FAQs
    :return: Success message after processing FAQs
    """
    try:
        # Validate file is not empty
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        # Parse the uploaded file
        faq_data = parse_faq_file(file)
        
        # Validate parsed data
        if not faq_data:
            raise HTTPException(status_code=400, detail="Failed to parse FAQ data from file")
        
        # Store FAQs in MongoDB
        for faq in faq_data:
            await store_faq(faq['Question'], faq['Answer'])
        
        # Index FAQs in FAISS
        faq_indexer.index_faqs(faq_data)
        
        return {
            "message": "FAQs uploaded from file, stored, and indexed successfully",
            "total_faqs": len(faq_data)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
#file: UploadFile = File(None)
@app.post("/api/upload-faq")
async def upload_faq(google_drive_link: str = Form(None), website_link: str = Form(None)):
    """
    Upload a CSV or Excel file, or provide a Google Drive link containing FAQ data.
    """
    try:
        print("workingg")
        faq_data = None
        # if file and file.filename:
        #     faq_data = parse_faq_file(file)
        if google_drive_link:
            # Extract file ID from Google Drive link
            file_id = google_drive_link.split('/')[-2]
            faq_data = download_and_parse_public_google_drive_file(file_id)
        elif website_link:
            web_content = extract_website_content(website_link)
            print("content", web_content)
            is_web = True
            return {"message": "Web Content successfully extracted."}
        else:
            raise HTTPException(status_code=400, detail="No file or Google Drive link provided.")

        if faq_data is None:
            raise HTTPException(status_code=400, detail="Failed to parse FAQ data.")

        # Store FAQs in MongoDB
        for faq in faq_data:
            await store_faq(faq['Question'], faq['Answer'])

        # Index FAQs in FAISS
        faq_indexer.index_faqs(faq_data)

        return {"message": "FAQs uploaded, stored, and indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-response", response_model=EmailResponse)
async def generate_ai_response(query: EmailQuery):
    """
    Generates an AI response to an email query.

    Args:
        query: The email query containing the subject and body.

    Returns:
        An EmailResponse object containing the AI response, response time, accuracy, and response ID.
    """
    start_time = time.time()

    try:
        if is_web:
           web_faqs =  generate_faqs_from_web(content=web_content)
           combined_content = f"{web_faqs}\n\nEmail Subject: {query.subject}\nEmail Body: {query.email_body}"
           ai_response = await generate_response_with_faq(query.subject, combined_content)
           print("Response from web content: ", ai_response)
        else:
            # Check if FAQs are indexed, if not, retrieve from MongoDB and index them
            if not faq_indexer.faqs:
                stored_faqs = await get_all_faqs()
                if stored_faqs:
                    faq_indexer.index_faqs(stored_faqs)
                else:
                    raise HTTPException(status_code=404, detail="No FAQs available in the database.")

            # Retrieve relevant FAQs
            relevant_faqs = faq_indexer.retrieve_faqs(query.email_body)

            # Generate response based on whether relevant FAQs are found
            if relevant_faqs:
                faq_context = "\n".join([f"Q: {faq['Question']}\nA: {faq['Answer']}" for faq in relevant_faqs])
                combined_content = f"{faq_context}\n\nEmail Subject: {query.subject}\nEmail Body: {query.email_body}"
                ai_response = await generate_response_with_faq(query.subject, combined_content)
            else:
                ai_response = await generate_generic_response(query.subject, query.email_body)

        # Calculate response time
        response_time = round(time.time() - start_time, 2)

        # Evaluate response accuracy (simplified version)
        accuracy = await evaluate_response_accuracy(query.email_body, ai_response)

        # Store in MongoDB (asynchronously)
        response_id = await store_response(
            query.subject,
            query.email_body,
            ai_response,
            response_time,
            accuracy
        )

        # Create response object
        response = EmailResponse(
            ai_response=ai_response,
            response_time=response_time,
            accuracy=accuracy,
            response_id=response_id
        )

        return response

    except IndexError as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing FAQs: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

