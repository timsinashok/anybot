# import os
# from typing import List
# import requests
# from bs4 import BeautifulSoup
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# from transformers import pipeline
# import torch

# class CrustdataFreeRAG:
#     def __init__(self):
#         # Initialize sentence transformer for embeddings
#         self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
#         # Initialize local LLM using transformers
#         self.qa_model = pipeline(
#             "text-generation",
#             model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Small model that can run on CPU
#             torch_dtype=torch.float32,
#             device="cpu"
#         )
        
#         self.chunks = []
#         self.index = None
#         self.embeddings = None
        
#     def extract_text_from_notion(self, urls: List[str]) -> List[str]:
#         """Extract text content from Notion pages."""
#         documents = []
        
#         for url in urls:
#             response = requests.get(url)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Extract main content
#             content = soup.find('article')
#             if content:
#                 documents.append(content.get_text())
                
#         return documents
    
#     def chunk_documents(self, documents: List[str], chunk_size: int = 500) -> List[str]:
#         """Split documents into smaller chunks with simple overlap."""
#         chunks = []
        
#         for doc in documents:
#             words = doc.split()
#             for i in range(0, len(words), chunk_size // 2):
#                 chunk = ' '.join(words[i:i + chunk_size])
#                 if chunk:
#                     chunks.append(chunk)
                    
#         return chunks
    
#     def create_index(self, chunks: List[str]):
#         """Create FAISS index for vector similarity search."""
#         # Generate embeddings
#         embeddings = self.embedding_model.encode(chunks)
        
#         # Initialize FAISS index
#         dimension = embeddings.shape[1]
#         self.index = faiss.IndexFlatL2(dimension)
        
#         # Add vectors to index
#         self.index.add(np.array(embeddings).astype('float32'))
        
#         # Store chunks and embeddings
#         self.chunks = chunks
#         self.embeddings = embeddings
        
#     def process_documentation(self, urls: List[str]):
#         """Process documentation from URLs and set up the RAG system."""
#         # Extract text
#         documents = self.extract_text_from_notion(urls)
        
#         # Chunk documents
#         self.chunks = self.chunk_documents(documents)
        
#         # Create search index
#         self.create_index(self.chunks)
        
#     def get_response(self, query: str, k: int = 3) -> str:
#         """Get response for a query using the RAG system."""
#         if not self.index:
#             raise ValueError("Index not initialized. Call process_documentation first.")
        
#         # Get query embedding
#         query_embedding = self.embedding_model.encode([query])
        
#         # Search for similar chunks
#         distances, indices = self.index.search(
#             np.array(query_embedding).astype('float32'), k
#         )
        
#         # Get relevant chunks
#         relevant_chunks = [self.chunks[i] for i in indices[0]]
        
#         # Create prompt with context
#         prompt = f"""Based on the following API documentation, answer the question.
        
# Documentation:
# {' '.join(relevant_chunks)}

# Question: {query}

# Answer: """
        
#         # Generate response
#         response = self.qa_model(
#             prompt,
#             max_length=500,
#             num_return_sequences=1,
#             temperature=0.7
#         )[0]['generated_text']
        
#         # Extract the answer part
#         answer = response.split('Answer: ')[-1].strip()
        
#         return answer

# # Example usage
# if __name__ == "__main__":
#     # Initialize RAG system
#     rag = CrustdataFreeRAG()
    
#     # Process documentation
#     docs_urls = [
#         "https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c",
#         "https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48"
#     ]
    
#     rag.process_documentation(docs_urls)
    
#     # Example query
#     response = rag.get_response("How do I search for people by their title and company?")
#     print(response)

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List

class SimpleCrustdataRAG:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.chunks = []
        self.vectors = None

    def extract_text_from_notion(self, urls: List[str]) -> List[str]:
        """Extract text content from Notion pages."""
        documents = []

        for url in urls:
            try:
                response = requests.get(url)
                print(response.text)
                response.raise_for_status()  # Raise an error for bad status codes
                soup = BeautifulSoup(response.text, 'html.parser')

                # # Extract all text content from Notion-specific elements
                # text_elements = soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'a'])
                # print(text_elements)
                # text_content = ' '.join([element.get_text(separator=' ', strip=True) for element in text_elements])

                text_content = soup.body.get_text(separator=' ', strip=True)

                # Debug print
                print(f"Extracted text from {url}: {text_content[:20000]}...")  # Print first 200 characters

                documents.append(text_content)
            except Exception as e:
                print(f"Error fetching {url}: {str(e)}")

        return documents

    def chunk_documents(self, documents: List[str], chunk_size: int = 500) -> List[str]:
        """Split documents into smaller chunks."""
        chunks = []

        for doc in documents:
            words = doc.split()
            for i in range(0, len(words), chunk_size // 2):
                chunk = ' '.join(words[i:i + chunk_size])
                if chunk:
                    chunks.append(chunk)

        return chunks

    def create_index(self, chunks: List[str]):
        """Create TF-IDF vectors for similarity search."""
        if not chunks:
            raise ValueError("No chunks to create index from.")

        self.chunks = chunks
        self.vectors = self.vectorizer.fit_transform(chunks)

    def process_documentation(self, urls: List[str]):
        """Process documentation from URLs and set up the system."""
        # Extract text
        documents = self.extract_text_from_notion(urls)

        # Check for empty documents
        if not documents:
            raise ValueError("No text content extracted from the provided URLs.")

        # Chunk documents
        self.chunks = self.chunk_documents(documents)

        # Create search index
        self.create_index(self.chunks)

    def get_relevant_chunks(self, query: str, k: int = 3) -> List[str]:
        """Get most relevant chunks for a query."""
        if self.vectors is None or not self.vectors.nnz:
            raise ValueError("Index not initialized. Call process_documentation first.")

        # Get query vector
        query_vector = self.vectorizer.transform([query])

        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.vectors)

        # Ensure similarities is a 1D array
        similarities = similarities.flatten()

        # Get top k chunks
        top_indices = similarities.argsort()[-k:][::-1]
        return [self.chunks[i] for i in top_indices]

    def get_response(self, query: str) -> str:
        """Get response for a query using relevant documentation."""
        relevant_chunks = self.get_relevant_chunks(query)

        # Simple response template
        response = "Based on the documentation:\n\n"

        # Add relevant chunks
        for i, chunk in enumerate(relevant_chunks, 1):
            response += f"Reference {i}:\n{chunk.strip()}\n\n"

        return response

def main():
    # Initialize system
    rag = SimpleCrustdataRAG()

    # Process documentation
    docs_urls = [
        "https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c",
        "https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48"
    ]

    print("Processing documentation...")
    try:
        rag.process_documentation(docs_urls)
    except ValueError as ve:
        print(f"Error: {str(ve)}")
        return

    # Interactive query loop
    while True:
        query = input("\nEnter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        try:
            response = rag.get_response(query)
            print("\nResponse:", response)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()