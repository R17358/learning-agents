from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from typing import List, Optional
import json

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
# Step 2: Define Pydantic model
# ----------------------------
class ResumeInfo(BaseModel):
    name: str = Field(..., description="Full name of the candidate")    #  ... means required
    email: str = Field(..., description="Email address")                #   None -> Optional
    phone: str = Field(..., description="Phone number")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio or personal website")
    skills: List[str] = Field(default_factory=list, description="List of all skills combined")
    education: Optional[str] = Field(None, description="Education details as single string")
    experience: Optional[str] = Field(None, description="Experience summary as single string")
    projects: List[str] = Field(default_factory=list, description="List of project names")


# ----------------------------
# Step 3: Load model and environment
# ----------------------------
load_dotenv()
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
structured_llm = model.with_structured_output(ResumeInfo)

# ----------------------------
# Step 4: Prompt setup
# ----------------------------
chat_template = ChatPromptTemplate.from_messages([
    ("system", """You are a professional resume analyzer. 
Extract structured information from the resume and flatten all nested data.
Combine all skills into a single list."""),
    ("human", "Resume text:\n{resume_text}")
])

# ----------------------------
# Step 5: Run analyzer
# ----------------------------
pdf_path = input("Enter PDF path: ").strip()
resume_text = extract_text_from_pdf(pdf_path)

# Create chain and invoke
chain = chat_template | structured_llm
resume_obj = chain.invoke({"resume_text": resume_text})

print("\n--- Pydantic Object ---")
print(resume_obj)

# ----------------------------
# Step 6: Access data in multiple ways
# ----------------------------

# Method 1: Direct attribute access (recommended)
print("\n--- Method 1: Attribute Access ---")
print(f"Name: {resume_obj.name}")
print(f"Email: {resume_obj.email}")
print(f"Phone: {resume_obj.phone}")
print(f"Skills: {resume_obj.skills}")

# # Method 2: Convert to dictionary
# print("\n--- Method 2: Dictionary Access ---")
# resume_dict = resume_obj.model_dump()  # or dict(resume_obj)
# print(f"Name: {resume_dict['name']}")
# print(f"Email: {resume_dict['email']}")
# print(f"Skills count: {len(resume_dict['skills'])}")

# Method 3: Convert to JSON string
print("\n--- Method 3: JSON String ---")
json_string = resume_obj.model_dump_json(indent=2)
print(json_string)

# # Method 4: Parse JSON string back to dict (if you need it)
# print("\n--- Method 4: JSON → Dict ---")
# data = json.loads(json_string)
# print(f"Name from parsed JSON: {data['name']}")
# print(f"Projects: {data['projects']}")

# ----------------------------
# Step 7: Complete example
# ----------------------------
print("\n--- Complete Resume Summary ---")
print(f"Candidate: {resume_obj.name}")
print(f"Contact: {resume_obj.email} | {resume_obj.phone}")
print(f"LinkedIn: {resume_obj.linkedin or 'Not provided'}")
print(f"GitHub: {resume_obj.github or 'Not provided'}")
print(f"\nSkills ({len(resume_obj.skills)}): {', '.join(resume_obj.skills[:10])}...")
print(f"\nEducation: {resume_obj.education}")
print(f"\nExperience: {resume_obj.experience}")
print(f"\nProjects ({len(resume_obj.projects)}):")
for i, project in enumerate(resume_obj.projects, 1):
    print(f"  {i}. {project}")