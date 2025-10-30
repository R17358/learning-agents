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
from object_detection import detect_using_gemini

load_dotenv()

api = os.getenv("GOOGLE_API_KEY")
tavily_api = os.getenv("TAVILY_API_KEY")

@tool
def search_on_internet(query: str) -> str:
    """Search given topic on the internet using Tavily search engine."""
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
            
            output += f"\n{i}. {title}\n   {content}\n   URL: {url}\n"

        return output
    except Exception as e:
        return f"Error performing search: {str(e)}"


@tool
def detect_object():
     """
    Opens the camera to automatically capture an image after 6 seconds and detect objects in it.

    The function waits 6 seconds after opening the camera, captures the image, 
    detects object(s) in the image, searches for relevant information about the detected object online, 
    and returns a descriptive label or summary.

    Use this tool when the agent needs to:
    - Capture a real-time image via camera automatically
    - Recognize or classify an object in the image
    - Retrieve informative details about the detected object

    Returns:
        str: A string describing the detected object, including its label and 
            relevant information retrieved from the internet.
    """
     save_path = os.path.join("images", "capture.jpg")
     print(save_path)
     try:
        thing = detect_using_gemini(save_path)
        print(f"\n Result to pass to agent: {thing}")
        search_result_thing = search_on_internet(f"search important information about given object on internet:{thing} , but concise it to 5 lines.")
        save_note(f"{thing}: {search_result_thing}")
        return f"{thing}: {search_result_thing}"
    
     except Exception as e:
        print(e)
        return None


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
        return f" Error saving note: {str(e)}"



tools = [
    detect_object,
    search_on_internet,
    get_current_time,
    calculator,
    save_note  
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
        - You can perform calculations, open the camera and detect object, tell the current time, and save notes.
        - You can also search the internet using the Tavily Search Tool when the user asks for information that requires web results.
        - You remember previous user interactions and can use past context to give better, personalized answers.
        - You communicate naturally in Hinglish (English + Hindi mixed), keeping responses friendly, clear, and human-like.

         When NOT to use tools:
        - If the user asks you to **write a poem, story, article, script, song, or any creative content**, do NOT call any tools.
        - In such cases, directly generate the response using your LLM creative reasoning.
        - Never try to find a tool for creative, conversational, or reasoning-based tasks.

         When to use tools:
        - For math operations ➜ use `calculator`
        - For opening the webcam, capturing photo or detecting object ➜ use `detect_object`
        - For checking current time ➜ use `get_current_time`
        - For saving notes ➜ use `save_note`
        - For searching topics on the internet ➜ use `tavily_search_tool`

         Response Style:
        - Be concise but conversational.
        - Use Hinglish where it fits naturally (e.g., “Sure bhai, ye raha tumhara result 👇”).
        - If you need clarification, politely ask the user.
        - Always ensure the response feels human, context-aware, and emotionally intelligent.

         Important Behavioral Rule:
        If a task doesn't require any tool, respond directly using your own knowledge and reasoning.
        Never say “I don't know” unless the information is truly unavailable.
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
    print(" LangChain Agent with Memory and Tools)")
    print("=" * 60)
    print("\n Available capabilities:")
    print("\n Search topic on internet")
    print("\n Answer questions and have conversations")
    print("\n Open camera, capture photo and detect image")
    print("\n Calculate mathematical calculations")
    print("\n Save notes to file")
    print("\n Remember conversation history")
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
            print(f"\n Agent: {response['output']}")
            
            
        except KeyboardInterrupt:
            print("\n\n Interrupted! Agent band ho raha hai...")
            break
        except Exception as e:
            print(f"\n Error: {str(e)}")
            print("Koi baat nahi, dobara try karo!")


if __name__ == "__main__":
    
    main()