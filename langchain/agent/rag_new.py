from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
import numpy as np
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


load_dotenv()

api = os.getenv("GOOGLE_API_KEY")

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=api)


memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True,
    # output_key="output"
)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)


def create_embeddings(text:str):
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    all_splits = text_splitter.split_text(text)
    
    return all_splits

def text_extraction_from_pdf(pdf):
    
    reader = PdfReader(pdf)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # print(text)
    
    return text
    
def creating_vector_store(all_splits):
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}

    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    # Create FAISS index
    sample_embedding = np.array(hf_embeddings.embed_query("sample text"))
    dimension = sample_embedding.shape[0]
    index = faiss.IndexFlatL2(dimension)
    # Create FAISS vector store with the embedding function
    vector_store = FAISS(
        embedding_function=hf_embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    vector_store.add_texts(all_splits)  # Add documents to the vector store
    return vector_store

def retrieve_from_vector_store(vectorstore, query):
    
    # Retrieve relevant documents from the vectorstore
    retriever = vectorstore.as_retriever()
    # relevant_docs = retriever.get_relevant_documents(query)
    relevant_docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in relevant_docs])
    return context

def answering_question(query, context):
    try:   
        response = conversation.invoke(
            f"Based on the following context, answer the question:\n\nContext:\n{context}\n\nQuestion: {query}"
        )
        # Extract the response text
        return response.get('response') if isinstance(response, dict) else response
    except Exception as e:
        print(f"Error generating answer: {e}")
        return None
    
    
def start_rag(pdf):   
    all_splits = text_extraction_from_pdf(pdf)
    all_splits = create_embeddings(all_splits)
    vector_store = creating_vector_store(all_splits)
    while True:
        query = input("\nEnter query: ")
        if query.lower() in ['exit', 'bye', 'quit']:
            print("Exiting....")
            break
        context = retrieve_from_vector_store(vector_store, query)  
        ans = answering_question(query, context)
        print(ans)
        


if __name__=="__main__":
    
    pdf_path=input("\nEnter PDF path: ")
    
    start_rag(pdf_path)
    
    
   