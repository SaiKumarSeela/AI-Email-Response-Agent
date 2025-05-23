from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class EmailQuery(BaseModel):
    subject: str
    email_body: str
    
    # model_config = {
    #     "json_schema_extra": {
    #         "example": {
    #             "subject": "Inquiry About Product Availability",
    #             "email_body": "Hello, I am interested in purchasing the XYZ Smartwatch. Can you confirm if it's available in stock and provide details on the delivery time?"
    #         }
    #     }
    # }

class EmailResponse(BaseModel):
    ai_response: str
    response_time: float
    accuracy: int = Field(..., ge=1, le=5)
    response_id: str
    
    # model_config = {
    #     "json_schema_extra": {
    #         "example": {
    #             "ai_response": "Hello, thank you for your interest in the XYZ Smartwatch! Yes, the product is currently in stock. Standard delivery takes 3-5 business days, while express shipping takes 1-2 business days. Let us know if you need further assistance.",
    #             "response_time": 1.45,
    #             "accuracy": 4,
    #             "response_id": "65f3c1xxxxxxxxxxxx"
    #         }
    #     }
    # }

class FeedbackModel(BaseModel):
    # response_id: str
    user_rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None