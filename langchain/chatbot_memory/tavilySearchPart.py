import getpass
import os
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import json


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=api_key)

output_file = "output.txt"

tavily_search_tool = TavilySearch(
    max_results=2,
    topic="general",
)

agent = create_react_agent(llm, [tavily_search_tool])

user_input = input("Enter topic:")

final_output = ""

for step in agent.stream(
    {"messages": user_input},
    stream_mode="values",
):
    last_output = step["messages"][-1]
    final_output += last_output.content
        

# Save structured output as JSON
with open(output_file, "w") as f:
    json.dump(final_output, f, indent=4, ensure_ascii=False)
