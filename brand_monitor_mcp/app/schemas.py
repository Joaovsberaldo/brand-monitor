from pydantic import BaseModel, Field
from typing import List

class SearchOutput(BaseModel):
    text: str = Field(description="The text of the news/post about the brand.")
    source: str = Field(description="The source or URL of the text.")
    company_name: str = Field(description="The brand/company that was searched.")
    
class AnalyzeOutput(BaseModel):
    sentiment: str = Field(description="The predominant sentiment of people in mentions and news about the company.")
    topics: List[str] = Field(description="The main topics mentioned by people about the company.")
    issues: List[str] = Field(description="The most mentioned issues by people about the company.")
