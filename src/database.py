import chromadb
from chromadb.config import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core.text_splitter import TokenTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
import time
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChromaDatabase:
    def __init__(
        self, 
        database_name: str, 
        host: str = 'localhost', 
        port: int = 8000,
        model_name: str = "BAAI/bge-m3", 
        cache_dir: str = "./.cache"
    ):
        """
        Initialize the ChromaDatabase instance.
        
        Args:
            database_name (str): The name of the collection.
            host (str): The host where ChromaDB is running.
            port (int): The port for ChromaDB.
            model_name (str): The name of the embedding model to use.
            cache_dir (str): Directory to cache embeddings to avoid recomputation
        """
        try:
            # Create cache directory if it doesn't exist
            os.makedirs(cache_dir, exist_ok=True)
            
            # Connect to ChromaDB
            self.client = chromadb.HttpClient(host=host, port=port)
            self.collection = self.client.get_or_create_collection(name=database_name)
            
            # Initialize embedding model with caching
            self.embed_model = HuggingFaceEmbedding(
                model_name=model_name,
                cache_folder=cache_dir
            )
            
            logger.info(f"Database setup complete using {model_name} embedding model.")
        except Exception as e:
            logger.error(f"Error setting up database: {e}")
            raise

    def store_documents(
        self, 
        directory_path: str, 
        chunk_size: int = 1024, 
        chunk_overlap: int = 100, 
        batch_size: int = 100
    ):
        """
        Store documents from a directory into ChromaDB with batch processing and metadata.
        
        Args:
            directory_path (str): The path to the directory containing documents.
            chunk_size (int): The size of each text chunk.
            chunk_overlap (int): The overlap between consecutive text chunks.
            batch_size (int): Number of documents to process in each batch.
        """
        try:
            logger.info(f"Loading documents from {directory_path}...")
            reader = SimpleDirectoryReader(input_dir=directory_path)
            documents = reader.load_data()
            logger.info(f"Loaded {len(documents)} documents.")
            
            # Initialize text splitter
            splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            
            # Process documents and track metadata
            chunks = []
            metadatas = []
            doc_count = 0
            
            start_time = time.time()
            for doc_idx, doc in enumerate(documents):
                text_chunks = splitter.split_text(doc.text)
                source_name = doc.metadata.get("file_path", f"document_{doc_idx}")
                file_name = os.path.basename(source_name)
                
                for chunk_idx, chunk in enumerate(text_chunks):
                    chunks.append(chunk)
                    metadatas.append({
                        "source": source_name,
                        "file_name": file_name,
                        "chunk_index": chunk_idx,
                        "doc_index": doc_idx,
                        "total_chunks": len(text_chunks)
                    })
                doc_count += 1
                
                # Log progress for large document sets
                if doc_count % 10 == 0:
                    logger.info(f"Processed {doc_count}/{len(documents)} documents")
            
            # Batch processing with metadata
            total_batches = (len(chunks) + batch_size - 1) // batch_size
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i+batch_size]
                batch_metadatas = metadatas[i:i+batch_size]
                
                # Generate embeddings
                batch_embeddings = [self.embed_model.get_text_embedding(chunk) for chunk in batch_chunks]
                
                # Create unique IDs
                batch_ids = [f"doc_{meta['doc_index']}_chunk_{meta['chunk_index']}" for meta in batch_metadatas]
                
                # Add to collection
                self.collection.add(
                    documents=batch_chunks,
                    embeddings=batch_embeddings,
                    metadatas=batch_metadatas,
                    ids=batch_ids
                )
                
                logger.info(f"Processed batch {i//batch_size + 1}/{total_batches}")
            
            processing_time = time.time() - start_time
            logger.info(f"Documents stored successfully. Processed {len(chunks)} chunks in {processing_time:.2f} seconds.")
            
            return {
                "document_count": len(documents),
                "chunk_count": len(chunks),
                "processing_time": processing_time
            }
            
        except Exception as e:
            logger.error(f"Error storing documents: {e}", exc_info=True)
            raise

    def query_rag(
        self, 
        query: str, 
        top_n: int = 5, 
        similarity_threshold: Optional[float] = None,
        include_metadata: bool = True
    ):
        """
        Query the ChromaDB collection and retrieve top results.
        
        Args:
            query (str): The query string.
            top_n (int): The number of top results to retrieve.
            similarity_threshold (float, optional): If set, filter results below this similarity threshold.
            include_metadata (bool): Whether to include metadata in results.
            
        Returns:
            dict: Query results including documents, metadata, and distances.
        """
        try:
            start_time = time.time()
            print("Query = ", query)
            
            # Generate embedding for query
            query_embedding = self.embed_model.get_text_embedding(query)
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding], 
                n_results=top_n,
                include=["documents", "metadatas", "distances", "embeddings"] if include_metadata else ["documents", "distances"]
            )
            print("Top Results:", results)
            #print(results)
            print(len(results['documents']))
            query_time = time.time() - start_time
            logger.info(f"Query completed in {query_time:.4f} seconds")
            
            # Filter by similarity threshold if specified
            if similarity_threshold is not None and results['distances'] and results['distances'][0]:
                distances = results['distances'][0]
                mask = [distance >= similarity_threshold for distance in distances]
                
                filtered_results = {
                    'ids': [[id for id, m in zip(results['ids'][0], mask) if m]] if 'ids' in results else [],
                    'documents': [[doc for doc, m in zip(results['documents'][0], mask) if m]],
                    'metadatas': [[meta for meta, m in zip(results['metadatas'][0], mask) if m]] if 'metadatas' in results else [],
                    'distances': [[dist for dist, m in zip(distances, mask) if m]],
                    'query_time': query_time
                }
                
                logger.info(f"Filtered from {len(distances)} to {len(filtered_results['distances'][0])} results using threshold {similarity_threshold}")
                return filtered_results
            
            # Add query time to results
            results['query_time'] = query_time
            return results
            
        except Exception as e:
            logger.error(f"Error querying database: {e}", exc_info=True)
            raise

    def delete_collection(self):
        """Delete the current collection"""
        try:
            self.client.delete_collection(self.collection.name)
            logger.info(f"Collection {self.collection.name} deleted successfully")
            return {"status": "success", "message": f"Collection {self.collection.name} deleted"}
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise

    def get_collection_stats(self):
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection.name,
                "document_count": count,
                "embedding_model": self.embed_model.model_name
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            raise
















# import chromadb
# from chromadb.config import Settings
# from llama_index.core import SimpleDirectoryReader
# from llama_index.core.text_splitter import TokenTextSplitter
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# class ChromaDatabase:
#     def __init__(self, database_name: str, host: str = 'localhost', port: int = 8000, 
#                  model_name: str = "BAAI/bge-m3"):
#         """
#         Initialize the ChromaDatabase instance.

#         Args:
#             database_name (str): The name of the collection.
#             host (str): The host where ChromaDB is running.
#             port (int): The port for ChromaDB.
#             model_name (str): The name of the embedding model to use.
#         """
#         try:
#             self.client = chromadb.HttpClient(host=host, port=port)
#             self.collection = self.client.get_or_create_collection(name=database_name)
#             self.embed_model = HuggingFaceEmbedding(model_name=model_name)
#             print(f"Database setup complete using {model_name} embedding model.")
#         except Exception as e:
#             print(f"Error setting up database: {e}")
#             raise

#     def store_documents(self, directory_path: str, chunk_size: int = 1024, chunk_overlap: int = 100):
#         """
#         Store documents from a directory into ChromaDB.

#         Args:
#             directory_path (str): The path to the directory containing documents.
#             chunk_size (int): The size of each text chunk.
#             chunk_overlap (int): The overlap between consecutive text chunks.
#         """
#         try:
#             reader = SimpleDirectoryReader(input_dir=directory_path)
#             documents = reader.load_data()
#             splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#             chunks = []
#             for doc in documents:
#                 text_chunks = splitter.split_text(doc.text)
#                 chunks.extend(text_chunks)

#             for i, chunk in enumerate(chunks):
#                 embedding = self.embed_model.get_text_embedding(chunk)
#                 self.collection.add(documents=[chunk], embeddings=[embedding], ids=[str(i)])
#             print(f"Documents stored successfully. Processed {len(chunks)} chunks.")
#         except Exception as e:
#             print(f"Error storing documents: {e}")
#             raise

#     def query_rag(self, query: str, top_n: int = 5):
#         """
#         Query the ChromaDB collection and retrieve top results.

#         Args:
#             query (str): The query string.
#             top_n (int): The number of top results to retrieve.
#         """
#         try:
#             query_embedding = self.embed_model.get_text_embedding(query)
#             results = self.collection.query(query_embeddings=[query_embedding], n_results=top_n)
#             print("Top Results:")
#             print(results)
#             for i, doc in enumerate(results['documents'][0]):
#                 print(f"\nResult {i+1}:")
#             return results
#         except Exception as e:
#             print(f"Error querying database: {e}")
#             raise