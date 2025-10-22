from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from typing import List, TypedDict
import os
import json
import re
# ----------------------------
# Step 1: PDF text extractor
# ----------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()



def parse_json_from_string(input_str):
    """
    Safely parse a JSON string, removing Markdown ```json fences if present.
    
    Args:
        input_str (str): The input string that may contain JSON.
    
    Returns:
        dict/list: Parsed JSON object or array.
    
    Raises:
        ValueError: If the string cannot be parsed as JSON.
    """
    # Remove ```json and ``` fences if they exist
    cleaned_str = re.sub(r"```json\s*|\s*```", "", input_str, flags=re.IGNORECASE).strip()
    
    try:
        parsed = json.loads(cleaned_str)
        return parsed
    except json.JSONDecodeError as e:
        # You can handle edge cases here or give a detailed error
        raise ValueError(f"Invalid JSON: {e}")


# ----------------------------
# Step 2: Define TypedDict schema
# ----------------------------
class ResumeInfo(TypedDict):
    name: str
    email: str
    phone: str
    linkedin: str
    github: str
    portfolio: str
    skills: List[str]
    education: str
    experience: str
    projects: List[str]

# ----------------------------
# Step 3: Load model and environment
# ----------------------------
load_dotenv()
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# ----------------------------
# Step 4: Prompt setup
# ----------------------------
chat_template = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a professional resume analyzer. "
     "Extract structured information from the given resume text "
     "and return data that exactly matches the ResumeInfo TypedDict format:\n"
     "Fields: name, email, phone, linkedin, github, portfolio, skills (list), education, experience, projects (list)."),
    ("human", "Here is the resume text:\n{resume_text}")
])

# ----------------------------
# Step 5: Run analyzer
# ----------------------------
pdf_path = input("Enter PDF path: ").strip()
resume_text = extract_text_from_pdf(pdf_path)

formatted_prompt = chat_template.invoke({
    "resume_text": resume_text
})

result = model.invoke(formatted_prompt)

print(result.content)

# Optionally, you can parse this result into a dict safely
# (if model outputs JSON)
try:
    parsed_resume=parse_json_from_string(result.content)
    print(parsed_resume["name"])
    for key, val in parsed_resume.items():
        print(f"{key}: {val}")
except Exception as e:
    print("\n Could not parse JSON, raw output printed above.")
