import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

class RAGEngine:
    def __init__(self):
        # 1. Define a LOCAL folder for the model (Bypassing Windows Temp issues)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        local_cache_path = os.path.join(current_dir, "local_model_cache")

        print(f"🔌 Loading model from local cache: {local_cache_path}")
        
        # 2. Initialize FastEmbed with the specific cache folder
        self.embeddings = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5", 
            cache_dir=local_cache_path
        ) 
        self.persist_directory = "chroma_db"

    def ingest_data(self):
        print("📚 RAG Engine: Checking for new PDFs...")
        
        if not os.path.exists("knowledge"):
            os.makedirs("knowledge")
            
        documents = []
        pdf_files = [f for f in os.listdir("knowledge") if f.endswith(".pdf")]
        
        if not pdf_files:
            print("⚠️ No PDFs found. Please drop a file in 'knowledge/'.")
            return

        print(f"   -> Found {len(pdf_files)} PDFs: {pdf_files}")
        
        # Load Data
        for file in pdf_files:
            file_path = os.path.join("knowledge", file)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

        # Split Data
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        print(f"   -> Created {len(chunks)} text chunks.")

        # Store in ChromaDB
        print("   -> 🧠 Creating Vector Database locally...")
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings, 
            persist_directory=self.persist_directory
        )
        print("✅ Success! Knowledge Base created locally.")

    def search(self, query):
        if not os.path.exists(self.persist_directory):
            return "No knowledge base found."
            
        vectorstore = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        docs = vectorstore.similarity_search(query, k=3)
        return [doc.page_content for doc in docs]

if __name__ == "__main__":
    engine = RAGEngine()
    engine.ingest_data()