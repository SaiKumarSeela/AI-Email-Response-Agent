import pandas as pd
from fastapi import UploadFile
import io
import requests
from bs4 import BeautifulSoup  # Add this import for web scraping
import asyncio
# from crawl4ai import AsyncWebCrawler
from firecrawl import FirecrawlApp

def parse_faq_file(file: UploadFile):
    """Parse the uploaded CSV or Excel file to extract FAQ data."""
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file.file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file.file)
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")

    if 'Question' not in df.columns or 'Answer' not in df.columns:
        raise ValueError("The file must contain 'Question' and 'Answer' columns.")

    return df[['Question', 'Answer']].to_dict(orient='records')

def download_and_parse_public_google_drive_file(file_id: str):
    """Download and parse a public Google Drive file to extract FAQ data."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    response.raise_for_status()

    file_io = io.BytesIO(response.content)
    # Check if the file is CSV or Excel by trying to read it as CSV first
    try:
        df = pd.read_csv(file_io)
    except pd.errors.ParserError:
        # If CSV parsing fails, try reading as Excel
        file_io.seek(0)  # Reset the BytesIO object to the beginning
        df = pd.read_excel(file_io)

    if 'Question' not in df.columns or 'Answer' not in df.columns:
        raise ValueError("The file must contain 'Question' and 'Answer' columns.")

    return df[['Question', 'Answer']].to_dict(orient='records')

# async def extract_website_content(url: str) -> str:
#         async with AsyncWebCrawler() as crawler:
#             result = await crawler.arun(
#                 url,
#             )
#             return result.markdown[:500] 

def extract_website_content(url: str) -> str:
    app = FirecrawlApp(api_key="fc-85be9a11d01d4885a7b39c2f26f47826")

    # Scrape a website:
    scrape_status = app.scrape_url(
    url, 
    params={'formats': ['markdown', 'html']}
    )
    print(scrape_status["markdown"])
    return scrape_status["markdown"]

# def extract_website_content(url: str) -> str:
#     """Extract content from a website synchronously."""
#     response = requests.get(url)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.content, 'html.parser')
#     # Extract text content from the website
#     text_content = soup.get_text(separator='\n', strip=True)

#     return text_content[:500]  # Return the first 500 characters of the extracted text
        
