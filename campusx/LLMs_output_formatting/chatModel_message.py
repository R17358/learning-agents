from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os 

load_dotenv()

# Initialize the model
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# Create chat template with memory placeholder
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a magician who knows all the magic tricks and guides anyone to do magic"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Store conversation history
chat_history = []

print("Magic Chat Assistant (type 'exit' or 'quit' to end)")
print("-" * 50)

while True:
    
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("\nGoodbye! Keep practicing your magic tricks! 🎩✨")
        break
    
    formatted_prompt = chat_template.invoke({
        "chat_history": chat_history,
        "input": user_input
    })
    
    result = model.invoke(formatted_prompt)
    
    print(f"\nMagician: {result.content}")
    
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=result.content))
    
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]