"""
RAGbot: Retrieval-Augmented Generation Chatbot using LangGraph, LangChain, and MongoDB

Dependencies:
    pip install langchain langgraph langchain_community tiktoken langchain-groq langchainhub chromadb langchain_huggingface arxiv wikipedia pymongo

Environment Variables:
    MONGODB_URI: MongoDB connection string (e.g., mongodb://localhost:27017)
    MONGODB_DB: Database name
    MONGODB_COLLECTION: Collection name for vector store
    GROQ_API_KEY: Your Groq API key for LLM routing
"""
import os
from typing import List, Literal
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langgraph.graph import END, StateGraph, START
from langchain.schema import Document
from pymongo import MongoClient

# --- Environment Variables ---
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.environ.get("MONGODB_DB", "ragbot_db")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "ragbot_vectors")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Set up pymongo client and collection
mongo_client = MongoClient(MONGODB_URI)
mongo_collection = mongo_client[MONGODB_DB][MONGODB_COLLECTION]

# --- 1. Load and Split Documents ---
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]
print("Loading documents from web...")
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)
print(f"Loaded and split {len(doc_splits)} documents.")

# --- 2. Embeddings ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- 3. MongoDB Vector Store ---
print("Setting up MongoDB vector store...")
vectorstore = MongoDBAtlasVectorSearch(
    collection=mongo_collection,
    embedding=embeddings,
)
vectorstore.add_documents(doc_splits)
print(f"Inserted {len(doc_splits)} documents into MongoDB vector store.")

astra_vector_index = VectorStoreIndexWrapper(vectorstore=vectorstore)
retriever = vectorstore.as_retriever()

# --- 4. LLM Router ---
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vectorstore", "wiki_search"] = Field(
        ...,
        description="Given a user question choose to route it to wikipedia or a vectorstore.",
    )

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")
structured_llm_router = llm.with_structured_output(RouteQuery)
system = """You are an expert at routing a user question to a vectorstore or wikipedia.\nThe vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.\nUse the vectorstore for questions on these topics. Otherwise, use wiki-search."""
route_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "{question}"),
])
question_router = route_prompt | structured_llm_router

# --- 5. Wikipedia and Arxiv Tools ---
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# --- 6. LangGraph State and Nodes ---
from typing_extensions import TypedDict
class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]

def retrieve(state):
    print("---RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

def wiki_search(state):
    print("---wikipedia---")
    question = state["question"]
    docs = wiki.invoke({"query": question})
    wiki_results = Document(page_content=docs)
    return {"documents": [wiki_results], "question": question}

def route_question(state):
    print("---ROUTE QUESTION---")
    question = state["question"]
    source = question_router.invoke({"question": question})
    if source.datasource == "wiki_search":
        print("---ROUTE QUESTION TO Wiki SEARCH---")
        return "wiki_search"
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return "retrieve"

# --- 7. Build LangGraph Workflow ---
workflow = StateGraph(GraphState)
workflow.add_node("wiki_search", wiki_search)
workflow.add_node("retrieve", retrieve)
workflow.add_conditional_edges(
    START,
    route_question,
    {
        "wiki_search": "wiki_search",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge("retrieve", END)
workflow.add_edge("wiki_search", END)
app = workflow.compile()

# --- 8. Main Function ---
def answer_question(question: str) -> str:
    """Run the workflow for a given question and return the answer as a string."""
    inputs = {"question": question}
    value = None
    for output in app.stream(inputs):
        for key, val in output.items():
            value = val  # capture the last value
    docs = value["documents"] if value else []
    if docs:
        if isinstance(docs[0], Document):
            return docs[0].page_content
        else:
            return str(docs)
    return "No answer found."

def main():
    import sys
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Enter your question: ")
    answer = answer_question(question)
    print(answer)

if __name__ == "__main__":
    main() 