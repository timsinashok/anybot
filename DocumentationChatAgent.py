import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DocumentationChatAgent:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.chunks = []
        self.vectors = None

    def extract_text_from_notion(self, urls: List[str]) -> List[str]:
        """Extract text content from Notion pages using Selenium."""
        documents = []

        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=chrome_options)

        for url in urls:
            try:
                driver.get(url)
                
                # Wait for the main content to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".notion-page-content"))
                )

                # Scroll to load all content
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # Wait for content to load
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # Extract text content
                text_content = driver.find_element(By.CSS_SELECTOR, ".notion-page-content").text

                # Debug print
                print(f"Extracted text from {url}: {text_content[:20000]}...")  # Print first 200 characters

                documents.append(text_content)
            except Exception as e:
                print(f"Error fetching {url}: {str(e)}")

        driver.quit()
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
    rag = DocumentationChatAgent()

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
