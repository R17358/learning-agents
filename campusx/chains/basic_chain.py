from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
from pydantic import BaseModel, Field

class Output(BaseModel):
    elaboration: str = Field(..., description="Elaboration of the translated text to 5 lines")

load_dotenv()

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

structured_model = model.with_structured_output(Output)

memory = ConversationBufferMemory(memory_key="history")

prompt = ChatPromptTemplate([
    ("system", "You are a helpful assistant that has ability to translate any text to {language} language."),
     MessagesPlaceholder(variable_name="history"),
    ("human", "Translate the given {text}")
])

prompt_elaborate = ChatPromptTemplate([
    ("system", "You are a helpful assistant that has ability to elaborate any text to more 5 lines."),
     MessagesPlaceholder(variable_name="history"),
    ("human", "elaborate the given {text}")
])

def pass_content(ai_msg):
    return {"text": ai_msg.content, "history": []}


chain = prompt | model

chain_2 = prompt_elaborate | structured_model

main_chain = chain | RunnableLambda(pass_content) | chain_2


while True:
    lang = input("Enter language: ").strip()
    text = input("Write some text: ").strip()
    
    chat_history = memory.chat_memory.messages

    result = main_chain.invoke({"language":lang,"history":chat_history, "text": text})
    print(result)
    
    memory.chat_memory.add_user_message(f"Translate to {lang}: {text}")
    memory.chat_memory.add_ai_message(f"\nElaboration: {result.elaboration}")



