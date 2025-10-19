
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import init_chat_model
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import cv2
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("GOOGLE_API_KEY")

def create_multiplication_table(n: str) -> str:
    
    try:
        num = int(n)
        table = f"\n Multiplication Table for {num}:\n"
        table += "=" * 30 + "\n"
        for i in range(1, 11):
            table += f"{num} x {i:2d} = {num * i:3d}\n"
        return table
    except ValueError:
        return " Please provide a valid number!"

def open_camera(duration: str = "5") -> str:
    
    try:
        seconds = int(duration)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            return " Camera nahi khul raha! Check karo camera connected hai ya nahi."
        
        print(f"\n📸 Camera khul gaya! {seconds} seconds ke liye...")
        print("Press 'q' to quit early")
        
        start_time = datetime.now()
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Display frame count and time
            elapsed = (datetime.now() - start_time).total_seconds()
            cv2.putText(frame, f"Time: {elapsed:.1f}s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Camera Feed', frame)
            
            frame_count += 1
            
            # Check for 'q' key or time limit
            if cv2.waitKey(1) & 0xFF == ord('q') or elapsed >= seconds:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return f"✅ Camera band ho gaya! Total {frame_count} frames captured in {elapsed:.1f} seconds."
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_current_time(dummy: str = "") -> str:
    """Returns current date and time"""
    now = datetime.now()
    return f" Current Time: {now.strftime('%d-%m-%Y %H:%M:%S')}"

def calculate(expression: str) -> str:
   
    try:
        
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return " Invalid characters in expression!"
        
        result = eval(expression)
        return f"🧮 Result: {expression} = {result}"
    except Exception as e:
        return f" Calculation error: {str(e)}"



tools = [
    Tool(
        name="multiplication_table",
        func=create_multiplication_table,
        description="Creates a multiplication table for a given number. Input should be a single number like '5' or '12'."
    ),
    Tool(
        name="open_camera",
        func=open_camera,
        description="Opens the camera for a specified duration in seconds. Input should be number of seconds like '5' or '10'. Default is 5 seconds if not specified."
    ),
    Tool(
        name="current_time",
        func=get_current_time,
        description="Returns the current date and time. No input needed."
    ),
    Tool(
        name="calculator",
        func=calculate,
        description="Evaluates mathematical expressions. Input should be a valid mathematical expression like '25 + 17' or '100 * 5'."
    )
]


def create_agent():
    
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=api)
    

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )
    

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant with access to various tools. 
        You can help with calculations, create multiplication tables, open camera, and tell time.
        Always be friendly and respond in a mix of English and Hindi (Hinglish) when appropriate.
        Remember previous conversations and provide contextual responses."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
   
    agent = create_openai_functions_agent(
        llm=model,
        tools=tools,
        prompt=prompt
    )
    
    # Create executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,  # Ye debug ke liye helpful hai
        handle_parsing_errors=True,
        max_iterations=3
    )
    
    return agent_executor


def main():
    
    print("=" * 60)
    print("🤖 LangChain Agent with Memory and Custom Tools")
    print("=" * 60)
    print("\n📌 Available capabilities:")
    print("   • Answer questions and have conversations")
    print("   • Create multiplication tables")
    print("   • Open camera")
    print("   • Calculate math expressions")
    print("   • Tell current time")
    print("   • Remember conversation history")
    print("\n💡 Type 'exit' or 'quit' to stop\n")
    
    # Create agent
    agent = create_agent()
    
    # Chat loop
    while True:
        try:
            user_input = input("\n You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n Goodbye! Agent band ho raha hai...")
                break
            
            if not user_input:
                continue
            
            
            response = agent.invoke({"input": user_input})
            print(f"\n Agent: {response['output']}")
            
        except KeyboardInterrupt:
            print("\n\n Interrupted! Agent band ho raha hai...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Koi baat nahi, dobara try karo!")

if __name__ == "__main__":
    
    main()