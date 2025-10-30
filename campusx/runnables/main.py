from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableParallel, RunnableSequence
from langchain_core.runnables import RunnableWithMessageHistory

load_dotenv()
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

parser = StrOutputParser()

prompt_notes = ChatPromptTemplate.from_messages([
    ('system', """You are a helpful assistant that can create notes about given text"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', 'Text for note creation: {text}')
])

prompt_quiz = ChatPromptTemplate.from_messages([
    ('system', """You are a helpful assistant that can make 5 quiz based on given text"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', 'Text for quiz creation: {text}')
])

prompt_result = ChatPromptTemplate.from_messages([
    ('system', """You are a helpful assistant that can give output in proper format quiz after notes."""),
    ('human', 'notes {notes} and quiz {quiz}')
])

parallel_chain = RunnableParallel(
    {
        'notes': prompt_notes | llm | parser,
        'quiz': prompt_quiz | llm | parser
    }
)

chain_merger = prompt_result | llm | parser

# chain_merger = RunnableSequence(prompt_result , llm , parser)

combined_chain = parallel_chain | chain_merger

final_chain = RunnableWithMessageHistory(
    combined_chain,
    get_session_history,
    input_messages_key="text",
    history_messages_key="chat_history"
)


text = input("Enter text: ")

result = final_chain.invoke(
    {'text': text}, 
    config={"configurable": {"session_id": "ram"}}
)

print(result)