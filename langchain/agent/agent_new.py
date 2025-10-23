
from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
import cv2
from datetime import datetime
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api = os.getenv("GOOGLE_API_KEY")
tavily_api = os.getenv("TAVILY_API_KEY")

@tool
def search_on_internet(query: str) -> str:
    """Search any topic on the internet using Tavily search engine."""
    try:
        client = TavilyClient(api_key=tavily_api)
        results = client.search(query, max_results=3)
        
        if not results or "results" not in results or not results["results"]:
            return "No results found."

        output = f"Search Results for '{query}':\n"
        for i, r in enumerate(results["results"], start=1):
            title = r.get("title", "No title")
            url = r.get("url", "No URL")
            content = r.get("content", "No description")
            
            # Tavily usually provides well-formatted content already
            output += f"\n{i}. {title}\n   {content}\n   URL: {url}\n"

        return output
    except Exception as e:
        return f"Error performing search: {str(e)}"

@tool
def create_multiplication_table(n: int) -> str:
    """Generate a multiplication table for a given number."""
    try:
        table = f"\n Multiplication Table for {n}:\n"
        table += "=" * 30 + "\n"
        for i in range(1, 11):
            table += f"{n} x {i} = {n * i}\n"
        return table
    except Exception as e:
        return f" Error: {str(e)}"


@tool
def open_camera() -> str:
    """Opens camera"""
    try:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            return " Camera is not openened"
        
        print(f"\n Camera opened!")
        print("Press 'q' to quit early")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow('Camera Feed', frame)
            
            frame_count += 1
            
            # Check for 'q' key or time limit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return f" Camera band ho gaya! Total {frame_count} frames captured"
    
    except Exception as e:
        return f" Error: {str(e)}"


@tool
def get_current_time() -> str:
    """Returns current date and time"""
    now = datetime.now()
    return f" Current Time: {now.strftime('%d-%m-%Y %H:%M:%S')}"


@tool
def calculator(expression: str) -> str:
    """Safely evaluates mathematical expressions"""
    try:
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return " Invalid characters in expression!"
        
        result = eval(expression)
        return f" Result: {expression} = {result}"
    except Exception as e:
        return f" Calculation error: {str(e)}"


@tool
def save_note(note: str) -> str:
    """Save a text note to a file with a timestamp."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"note_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Saved on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(note)
        
        return f" Note saved successfully as '{filename}'"
    except Exception as e:
        return f"❌ Error saving note: {str(e)}"


@tool
def weather_joke() -> str:
    """Returns a random weather-related joke. No input needed."""
    jokes = [
        " Why did the weather want privacy? It was changing!",
        " What did one cloud say to another? You're so cirrus!",
        " What bow can't be tied? A rainbow!",
        " What did the lightning bolt say? I'm shocking!",
    ]
    import random
    return random.choice(jokes)


tools = [
    create_multiplication_table,
    open_camera,
    get_current_time,
    calculator,
    save_note,
    weather_joke,
    search_on_internet  
]


def create_agent():
    """Creates and returns a LangChain agent with memory"""
    
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=api)
    
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an intelligent, friendly AI assistant designed to help users with a variety of tasks. 
        You have access to several tools, but you should only use them when they are clearly required.

        Your Capabilities:
        - You can perform calculations, create multiplication tables, open the camera, tell the current time, save notes, and share jokes.
        - You can also search the internet using the Tavily Search Tool when the user asks for information that requires web results.
        - You remember previous user interactions and can use past context to give better, personalized answers.
        - You communicate naturally in Hinglish (English + Hindi mixed), keeping responses friendly, clear, and human-like.

         When NOT to use tools:
        - If the user asks you to **write a poem, story, article, script, song, or any creative content**, do NOT call any tools.
        - In such cases, directly generate the response using your LLM creative reasoning.
        - Never try to find a tool for creative, conversational, or reasoning-based tasks.

         When to use tools:
        - For math operations ➜ use `calculator`
        - For multiplication tables ➜ use `create_multiplication_table`
        - For opening the webcam ➜ use `open_camera`
        - For checking current time ➜ use `get_current_time`
        - For saving notes ➜ use `save_note`
        - For telling jokes ➜ use `weather_joke`
        - For searching topics on the internet ➜ use `tavily_search_tool`

         Response Style:
        - Be concise but conversational.
        - Use Hinglish where it fits naturally (e.g., “Sure bhai, ye raha tumhara result 👇”).
        - If you need clarification, politely ask the user.
        - Always ensure the response feels human, context-aware, and emotionally intelligent.

         Important Behavioral Rule:
        If a task doesn't require any tool, respond directly using your own knowledge and reasoning.
        Never say “I don’t know” unless the information is truly unavailable.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    # Create agent
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
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3
    )
    
    return agent_executor


def main():
    """Main function to run the agent"""
    print("=" * 60)
    print(" LangChain Agent with Memory (@tool decorator)")
    print("=" * 60)
    print("\n📌 Available capabilities:")
    print("   • Answer questions and have conversations")
    print("   • Create multiplication tables")
    print("   • Open camera")
    print("   • Calculate math expressions")
    print("   • Tell current time")
    print("   • Save notes to file")
    print("   • Share jokes")
    print("   • Remember conversation history")
    print("\n Type 'exit' or 'quit' to stop\n")
    
    
    agent = create_agent()
    
    while True:
        try:
            user_input = input("\n You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n Goodbye! Agent band ho raha hai...")
                break
            
            if not user_input:
                continue
            
            response = agent.invoke({"input": user_input})
            print(f"\n🤖 Agent: {response['output']}")
            
        except KeyboardInterrupt:
            print("\n\n Interrupted! Agent band ho raha hai...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Koi baat nahi, dobara try karo!")


if __name__ == "__main__":
    
    main()