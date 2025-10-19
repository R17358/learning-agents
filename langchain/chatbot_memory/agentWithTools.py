import os
from dotenv import load_dotenv
import cv2
from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage

load_dotenv()


api = os.getenv("GOOGLE_API_KEY")

model = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", api_key=api
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def open_camera(tool_input=None):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Camera not accessible"

    print("Camera is opened! Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed...")
            break

        cv2.imshow("Camera", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Camera closed!"

def multiplication_table(number: str):
   
    try:
        number = int(number)
    except:
        return "Please provide a valid number."
    
    table = [f"{number} x {i} = {number * i}" for i in range(1, 11)]
    return "\n".join(table)

def answer_question(question: str):
    output_file = "output.txt"
    ans = model.invoke([HumanMessage(content=question)])
    with open(output_file, "w") as f:
        f.write(ans.content)
    return ans.content


tools = [
    Tool(
        name="OpenCamera",
        func=open_camera,
        description="Opens the camera and shows live video. Press 'q' to close."
    ),
    Tool(
        name="MultiplicationTable",
        func=multiplication_table,
        description="Generates multiplication table for a given number."
    ),
    Tool(
        name="AnswerQuestion",
        func=answer_question,
        description="Answers general questions."
    ),
]

agent = initialize_agent(
    tools,
    llm=model,
    agent_type=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
    memory=memory,
    verbose=True
)

while True:
    prompt = input("\nEnter command: ")
    if prompt.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    response = agent.run(prompt)
    print("\n" + response)

    