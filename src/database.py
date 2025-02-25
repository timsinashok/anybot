import chromadb
from llama_index import SimpleDirectoryReader
from llama_index.text_splitter import TokenTextSplitter
from llama_index.embeddings import HuggingFaceEmbedding

def setup_database(database_name):
    '''Setup ChromaDB'''
    # Initialize ChromaDB (Persistent Storage)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(database_name)

    return collection


def store_documents(collection, directory_path):
    '''Store documents in ChromaDB'''
    # Load Documents
    reader = SimpleDirectoryReader(input_dir=directory_path)  # Make sure you have a "docs" folder with your files
    documents = reader.load_data()

    # Split into Chunks
    splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Initialize Embedding Model
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Store Chunks in ChromaDB
    for i, chunk in enumerate(chunks):
        embedding = embed_model.get_text_embedding(chunk.text)
        collection.add(ids=[str(i)], documents=[chunk.text], embeddings=[embedding])



def query_rag(collection, embed_model, query: str):
    '''Query ChromaDB'''
    query_embedding = embed_model.get_text_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    
    print("Top Results:")
    for doc in results['documents'][0]:
        print("\n", doc)
