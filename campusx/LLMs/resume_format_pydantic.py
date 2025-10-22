from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from typing import List, Optional
import os
import json
import re

# ----------------------------
# Step 1: PDF text extractor
# ----------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


# ----------------------------
# Step 2: Safe JSON parser
# ----------------------------
def parse_json_from_string(input_str: str):
    """
    Safely parse a JSON string, removing Markdown ```json fences if present.
    """
    cleaned_str = re.sub(r"```json\s*|\s*```", "", input_str, flags=re.IGNORECASE).strip()
    try:
        return json.loads(cleaned_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


# ----------------------------
# Step 3: Define Pydantic model
# ----------------------------
class ResumeInfo(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio or personal website")
    skills: List[str] = Field(default_factory=list, description="List of skills")
    education: Optional[str] = Field(None, description="Education details")
    experience: Optional[str] = Field(None, description="Experience summary")
    projects: List[str] = Field(default_factory=list, description="List of project names")


# ----------------------------
# Step 4: Load model and environment
# ----------------------------
load_dotenv()
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# ----------------------------
# Step 5: Prompt setup
# ----------------------------
chat_template = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a professional resume analyzer. "
     "Extract structured information from the given resume text and "
     "return data that exactly matches this JSON schema:\n\n"
     "{\n"
     "  'name': str,\n"
     "  'email': str,\n"
     "  'phone': str,\n"
     "  'linkedin': str,\n"
     "  'github': str,\n"
     "  'portfolio': str,\n"
     "  'skills': list of strings,\n"
     "  'education': str,\n"
     "  'experience': str,\n"
     "  'projects': list of strings\n"
     "}\n\n"
     "Return only valid JSON."),
    ("human", "Here is the resume text:\n{resume_text}")
])

# ----------------------------
# Step 6: Run analyzer
# ----------------------------
pdf_path = input("Enter PDF path: ").strip()
resume_text = extract_text_from_pdf(pdf_path)

formatted_prompt = chat_template.invoke({
    "resume_text": resume_text
})

result = model.invoke(formatted_prompt)
print("\n--- Raw Model Output ---\n")
print(result.content)

# ----------------------------
# Step 7: Validate with Pydantic
# ----------------------------
print("\n--- Parsed and Validated Output ---\n")
try:
    parsed_resume = parse_json_from_string(result.content)
    resume_obj = ResumeInfo(**parsed_resume)  # Validate with Pydantic
    print(resume_obj.json(indent=2))
except ValueError as e:
    print(f"JSON parsing error: {e}")
except ValidationError as e:
    print("Validation error:\n", e.json(indent=2))
