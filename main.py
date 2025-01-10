import os
import configparser
import random
import time
from pymilvus import MilvusClient, DataType
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import dotenv

dotenv.load_dotenv()

class RAG:
    def __init__(self, hf_api_key, model_name="thenlper/gte-large", config_file="config.ini"):
        """Initialize the RAG system with HuggingFace and Milvus."""
        self.hf_api_key = hf_api_key
        self.model_name = model_name
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=self.hf_api_key, model_name=self.model_name
        )

        # Load Milvus configuration
        cfp = configparser.RawConfigParser()
        cfp.read(config_file)
        self.milvus_uri = cfp.get('example', 'uri')
        self.milvus_token = cfp.get('example', 'token')

        # Initialize Milvus client
        self.milvus_client = MilvusClient(uri=self.milvus_uri, token=self.milvus_token)
        print(f"Connected to Milvus DB: {self.milvus_uri}")

        self.collection_name = "rag_text_collection"
        self.dim = 768

        # Prepare collection
        self._prepare_collection()

    def _prepare_collection(self):
        """Prepare Milvus collection with schema."""
        if self.milvus_client.has_collection(self.collection_name):
            self.milvus_client.drop_collection(self.collection_name)
            print(f"Dropped existing collection: {self.collection_name}")

        print("Preparing schema...")
        schema = self.milvus_client.create_schema()
        schema.add_field("text_id", DataType.INT64, is_primary=True, description="Unique text ID")
        schema.add_field("text_content", DataType.VARCHAR, max_length=5000, description="Original text content")
        schema.add_field("text_embedding", DataType.FLOAT_VECTOR, dim=self.dim, description="Text embeddings")

        index_params = self.milvus_client.prepare_index_params()
        index_params.add_index("text_embedding", metric_type="L2")

        print(f"Creating collection: {self.collection_name}")
        self.milvus_client.create_collection(
            self.collection_name, dimension=self.dim, schema=schema, index_params=index_params
        )
        print(f"Collection {self.collection_name} created successfully.")

    def create_documents(self, text_list):
        """Process text and store it in the Milvus collection."""
        if not isinstance(text_list, list) or not all(isinstance(text, str) for text in text_list):
            raise ValueError("Input must be a list of strings.")

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
        documents = text_splitter.split_text(text_list)

        rows = []
        for idx, doc in enumerate(documents):
            embedding = self.embeddings.embed_query(doc)
            rows.append({
                "text_id": idx,
                "text_content": doc,
                "text_embedding": embedding
            })

        print("Inserting documents into Milvus...")
        start_time = time.time()
        self.milvus_client.insert(self.collection_name, rows)
        self.milvus_client.flush(self.collection_name)
        print(f"Inserted {len(rows)} documents in {round(time.time() - start_time, 4)} seconds.")

    def search(self, query, k=5):
        """Search the Milvus collection with a query."""
        if not query:
            raise ValueError("Query cannot be empty.")

        embedding = self.embeddings.embed_query(query)
        search_params = {"metric_type": "L2", "params": {"level": 2}}

        print(f"Searching for query: {query}")
        results = self.milvus_client.search(
            self.collection_name, [embedding], anns_field="text_embedding", limit=k, search_params=search_params
        )

        return [
            {"text_content": result.entity.text_content, "score": result.distance}
            for result in results
        ]

# Example usage:
if __name__ == "__main__":
    HF_API_KEY = os.getenv("HF_API_KEY")
    CONFIG_FILE = "config.ini"

    rag = RAG(hf_api_key=HF_API_KEY, config_file=CONFIG_FILE)

    # Example texts
    text_list = [
        "The first text document content.",
        "The second text document content.",
        "Another piece of knowledge to store."
    ]
    rag.create_documents(text_list=text_list)

    query = "example search query"
    results = rag.search(query=query)

    for result in results:
        print(f"Content: {result['text_content']}, Score: {result['score']}")
