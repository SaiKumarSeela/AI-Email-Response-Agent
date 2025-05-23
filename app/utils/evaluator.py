from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

# We'll use the same LLM as in llm_service.py
# This is a simplified example - In production you might use a different model
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.7,
    max_new_tokens=512,
    top_p=0.95,
    repetition_penalty=1.15,
    huggingfacehub_api_token=os.getenv("MODEL_API_KEY")
)

async def evaluate_response_accuracy(query, response):
    """
    Evaluate the accuracy of an AI-generated response on a scale of 1-5
    """
    eval_prompt = PromptTemplate(
        input_variables=["query", "response"],
        template="""
        You are an evaluator for AI-generated email responses. 
        Please rate the following response on a scale of 1-5, where:
        1 = Poor (irrelevant or incorrect)
        2 = Fair (partially relevant but missing key information)
        3 = Good (relevant but could be more comprehensive)
        4 = Very Good (comprehensive and accurate)
        5 = Excellent (perfect response addressing all aspects)
        
        Original Query: {query}
        AI Response: {response}
        
        Provide only a single number rating (1-5):
        """
    )
    
    eval_chain = eval_prompt | llm | StrOutputParser()
    result = await eval_chain.ainvoke({"query": query, "response": response})
    
    try:
        # Extract the rating from the response
        rating = int(result.strip())
        # Ensure rating is between 1-5
        rating = max(1, min(5, rating))
        return rating
    except:
        # Default to 3 if parsing fails
        return 3
