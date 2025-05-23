from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    temperature=0.8,
    max_new_tokens=512,
    top_p=0.95,
    repetition_penalty=1.15,
    huggingfacehub_api_token=os.getenv("MODEL_API_KEY")
)

# Prompt template for when relevant FAQs are found
faq_response_prompt = PromptTemplate(
    input_variables=["subject", "combined_content"],
    template="""
    You are an AI assistant for a company. Your task is to respond to customer emails professionally and accurately.
    
    Email Subject: {subject}
    Context: {combined_content}
    
    Please write a concise, helpful, friendly, and professional response to this email.
    """ 
)

# Prompt template for when no relevant FAQs are found
generic_response_prompt = PromptTemplate(
    input_variables=["subject", "email_body"],
    template="""
    You are an AI assistant for a company. Your task is to respond to customer emails professionally and accurately.
    
    Extract the username from the email body if present and use it in the greeting.
    
    Email Subject: {subject}
    Email Body: {email_body}
    
    Please write a generic, helpful, friendly, and professional response to this email.
    """ 
)

faq_prompt = PromptTemplate(
            input_variables=["content"],
            template="""
            Extract all Frequently Asked Questions (FAQs) from the following website content. 
            Provide the output in  format like 'Question' and 'Answer' .
            If no FAQs are found, return an empty list.

            Website Content:
            {content}
            """
        )

# Create LLM chains using Runnable Sequence
faq_response_chain = faq_response_prompt | llm | StrOutputParser()
generic_response_chain = generic_response_prompt | llm | StrOutputParser()
faq_web_response_chain = faq_prompt | llm | StrOutputParser()

async def generate_response_with_faq(subject: str, combined_content: str) -> str:
    """Generate AI response using LangChain and Hugging Face model with FAQ context"""
    try:
        response = await faq_response_chain.ainvoke({"subject": subject, "combined_content": combined_content})
        return response.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "We apologize, but we encountered an issue processing your request. Our team will get back to you shortly."

async def generate_generic_response(subject: str, email_body: str) -> str:
    """Generate AI response using LangChain and Hugging Face model without FAQ context"""
    try:
        response = await generic_response_chain.ainvoke({"subject": subject, "email_body": email_body})
        return response.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "We apologize, but we encountered an issue processing your request. Our team will get back to you shortly."


async def generate_faqs_from_web(content: str) -> str:
    """Generate AI response using LangChain and Hugging Face model without FAQ context"""
    try:
        response = await faq_web_response_chain.ainvoke({"content": content})
        return response.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "We apologize, but we encountered an issue processing your request. Our team will get back to you shortly."