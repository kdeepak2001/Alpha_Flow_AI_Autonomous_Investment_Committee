import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class RAGEngine:
    def __init__(self):
        # 1. Point to the folder we just created manually
        model_path = os.path.join(os.getcwd(), "my_local_model")
        
        print(f"🔌 Loading model from local folder: {model_path}")
        
        if not os.path.exists(model_path):
            raise ValueError("Model not found! Please run 'python setup_model.py' first.")

        # 2. Load the embeddings from that specific folder
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs={'device': 'cpu'}
        )
        self.persist_directory = "chroma_db"

    def ingest_data(self):
        print("📚 RAG Engine: Checking for new PDFs...")
        
        # Clear old DB
        if os.path.exists(self.persist_directory):
            try:
                shutil.rmtree(self.persist_directory)
            except:
                pass

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
        print("   -> 🧠 Creating Vector Database...")
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