import chromadb
from chromadb.config import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core.text_splitter import TokenTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

class ChromaDatabase:
    def __init__(self, database_name: str, host: str = 'localhost', port: int = 8000, 
                 model_name: str = "BAAI/bge-m3"):
        """
        Initialize the ChromaDatabase instance.

        Args:
            database_name (str): The name of the collection.
            host (str): The host where ChromaDB is running.
            port (int): The port for ChromaDB.
            model_name (str): The name of the embedding model to use.
        """
        try:
            self.client = chromadb.HttpClient(host=host, port=port)
            self.collection = self.client.get_or_create_collection(name=database_name)
            self.embed_model = HuggingFaceEmbedding(model_name=model_name)
            print(f"Database setup complete using {model_name} embedding model.")
        except Exception as e:
            print(f"Error setting up database: {e}")
            raise

    def store_documents(self, directory_path: str, chunk_size: int = 1024, chunk_overlap: int = 100):
        """
        Store documents from a directory into ChromaDB.

        Args:
            directory_path (str): The path to the directory containing documents.
            chunk_size (int): The size of each text chunk.
            chunk_overlap (int): The overlap between consecutive text chunks.
        """
        try:
            reader = SimpleDirectoryReader(input_dir=directory_path)
            documents = reader.load_data()
            splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks = []
            for doc in documents:
                text_chunks = splitter.split_text(doc.text)
                chunks.extend(text_chunks)

            for i, chunk in enumerate(chunks):
                embedding = self.embed_model.get_text_embedding(chunk)
                self.collection.add(documents=[chunk], embeddings=[embedding], ids=[str(i)])
            print(f"Documents stored successfully. Processed {len(chunks)} chunks.")
        except Exception as e:
            print(f"Error storing documents: {e}")
            raise

    def query_rag(self, query: str, top_n: int = 5):
        """
        Query the ChromaDB collection and retrieve top results.

        Args:
            query (str): The query string.
            top_n (int): The number of top results to retrieve.
        """
        try:
            query_embedding = self.embed_model.get_text_embedding(query)
            results = self.collection.query(query_embeddings=[query_embedding], n_results=top_n)
            print("Top Results:")
            print(results)
            for i, doc in enumerate(results['documents'][0]):
                print(f"\nResult {i+1}:")
            return results
        except Exception as e:
            print(f"Error querying database: {e}")
            raise