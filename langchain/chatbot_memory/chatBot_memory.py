
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

api = os.getenv("GOOGLE_API_KEY")
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=api)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


conversation = ConversationChain(
    llm=model,
    memory=memory,
    verbose=False 
)

def chat(prompt:str)->str:
    response = conversation.predict(input=prompt)
    return response

# while True:
#     prompt = input("\n\nuser: ")
#     output = chat(prompt)
#     print(f"\n\n\nAI: {output}")
