import os
from dotenv import load_dotenv 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# --- Load environment variables ---
# This ensures OPENAI_API_KEY is available when OpenAIEmbeddings() is called below
load_dotenv() 

# Determine the absolute path to knowledge_base.txt relative to this file
# This assumes knowledge_base.txt is in the project root, one level above 'app'
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(script_dir)
KNOWLEDGE_BASE_PATH = os.path.join(project_root, "knowledge_base.txt")

class KnowledgeBase:
    def __init__(self, file_path: str = KNOWLEDGE_BASE_PATH):
        # Check if API key is loaded AFTER load_dotenv() has run
        if not os.getenv("OPENAI_API_KEY"):
             raise ValueError("OPENAI_API_KEY not found in environment variables. Make sure it's set in your .env file.")

        if not os.path.exists(file_path):
             raise FileNotFoundError(f"Knowledge base file not found at: {file_path}")
        self.loader = TextLoader(file_path, encoding='utf-8') 
        # Use RecursiveCharacterTextSplitter for potentially better chunking
        self.text_splitter = CharacterTextSplitter(
            separator="\n\n", 
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        # Now OpenAIEmbeddings() should find the environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"Using API key: {api_key[:5]}...{api_key[-4:] if api_key else 'None'}")
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model="text-embedding-ada-002"  
        )
        self.vectorstore = None
        self._load_documents() 

    def _load_documents(self):
        """Loads and processes documents into the vector store."""
        print(f"Loading documents from: {self.loader.file_path}")
        documents = self.loader.load()
        if not documents:
             print("Warning: No documents loaded from the knowledge base file.")
             return 

        split_docs = self.text_splitter.split_documents(documents)
        print(f"Split into {len(split_docs)} chunks.")
        if split_docs: 
            self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)
            print("Vectorstore created successfully.")
        else:
            print("Warning: No text chunks generated after splitting.")

    def similarity_search(self, query: str, k: int = 1): 
        """Performs similarity search on the loaded vector store."""
        if not self.vectorstore:
            print("Error: Vectorstore not initialized.")
            return [] 

        if not query:
            return [] 

        print(f"Performing similarity search for: '{query}'")
        results = self.vectorstore.similarity_search(query, k=k)
        print(f"Found {len(results)} relevant documents.")
        return results

# Instantiate the knowledge base globally or pass it where needed
# Global instantiation is simpler for this example
kb = KnowledgeBase()