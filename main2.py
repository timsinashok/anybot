import os
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import replicate


class DocumentationChatAgent:
    def __init__(self):
        # Initialize Sentence Transformer model for embeddings
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Initialize Replicate Llama-2-7B-chat model
        self.llm_model = replicate.models.get("replicate/llama-2-7b-chat")

        # Variables for document chunks and embeddings
        self.chunks = []
        self.chunk_embeddings = None
        self.conversation_history = []
        self.chunk_metadata = {}

    def chunk_documents(self, documents: List[Dict], max_chunk_size: int = 500) -> List[str]:
        """Split documents into chunks for embedding."""
        chunks = []
        for idx, doc in enumerate(documents):
            metadata = {"source": f"Document {idx + 1}"}
            self.chunk_metadata[len(chunks)] = metadata
            
            text = doc.strip()
            while len(text) > max_chunk_size:
                split_idx = text.rfind(" ", 0, max_chunk_size)
                chunks.append(text[:split_idx])
                text = text[split_idx:].strip()
            chunks.append(text)
        return chunks

    def process_documents(self, documents: List[str]):
        """Generate embeddings for document chunks."""
        self.chunks = self.chunk_documents(documents)
        self.chunk_embeddings = self.embedding_model.encode(self.chunks, convert_to_tensor=False)

    def retrieve_relevant_chunks(self, query: str, top_n: int = 3) -> List[str]:
        """Retrieve the most relevant document chunks for a query."""
        if not self.chunks:
            raise ValueError("Documentation not processed. Please load documents first.")
        
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)
        similarities = cosine_similarity([query_embedding], self.chunk_embeddings)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        return [self.chunks[i] for i in top_indices if similarities[i] > 0.1]

    def get_llm_response(self, query: str, context: List[str]) -> str:
        """Generate a response using Llama-2."""
        context_text = "\n".join(context)
        prompt = f"Context: {context_text}\n\nQuestion: {query}\n\nAnswer:"
        response = self.llm_model.predict(prompt=prompt)
        return response.get("text", "Unable to generate a response.")

    def get_response(self, query: str) -> str:
        """Get a response for a query."""
        relevant_chunks = self.retrieve_relevant_chunks(query)
        if not relevant_chunks:
            return "Sorry, I couldn't find anything relevant in the documentation."
        
        response = self.get_llm_response(query, relevant_chunks)
        self.save_conversation(query, response)
        return response

    def save_conversation(self, query: str, response: str):
        """Save query and response to conversation history."""
        self.conversation_history.append({"query": query, "response": response})

    def extract_text_from_notion(self, urls: List[str]) -> List[str]:
        """Extract text content from Notion pages using Selenium."""
        documents = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

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
                    time.sleep(2)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # Extract text content
                text_content = driver.find_element(By.CSS_SELECTOR, ".notion-page-content").text
                documents.append(text_content)
            except Exception as e:
                print(f"Error fetching {url}: {str(e)}")

        driver.quit()
        return documents


def main():
    agent = DocumentationChatAgent()
    
    docs_urls = [
        "https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c",
        "https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48"
    ]
    
    print("🤖 Initializing Documentation Chat Agent...")
    
    try:
        documents = agent.extract_text_from_notion(docs_urls)
        agent.process_documents(documents)
        
        print("\n📱 Welcome to the Documentation Chat Assistant!")
        print("\nType 'quit' to exit or ask your question!")
        
        while True:
            query = input("\n👤 Your question: ")
            if query.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            try:
                response = agent.get_response(query)
                print("\n🤖 Response:\n", response)
            except Exception as e:
                print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Initialization Error: {str(e)}")

if __name__ == "__main__":
    main()








# # import requests
# # from bs4 import BeautifulSoup
# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity
# # import numpy as np
# # from typing import List, Dict, Tuple
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # import time
# # import json
# # from datetime import datetime
# # import re

# # class DocumentationChatAgent:
# #     def __init__(self):
# #         self.vectorizer = TfidfVectorizer(
# #             stop_words='english',
# #             max_df=0.95,
# #             min_df=2,
# #             ngram_range=(1, 2)
# #         )
# #         self.chunks = []
# #         self.vectors = None
# #         self.conversation_history = []
# #         self.chunk_metadata = {}  # Store section/topic info for each chunk
        
# #     def extract_text_from_notion(self, urls: List[str]) -> List[str]:
# #         """Extract text content from Notion pages using Selenium with improved structure parsing."""
# #         documents = []
        
# #         chrome_options = Options()
# #         chrome_options.add_argument("--headless")
# #         chrome_options.add_argument("--disable-gpu")
# #         chrome_options.add_argument("--no-sandbox")
# #         chrome_options.add_argument("--disable-dev-shm-usage")
# #         chrome_options.add_experimental_option("detach", True)
        
# #         driver = webdriver.Chrome(options=chrome_options)
        
# #         for url in urls:
# #             try:
# #                 driver.get(url)
# #                 WebDriverWait(driver, 20).until(
# #                     EC.presence_of_element_located((By.CSS_SELECTOR, ".notion-page-content"))
# #                 )
                
# #                 # Extract structured content
# #                 sections = driver.find_elements(By.CSS_SELECTOR, ".notion-header-block")
# #                 for section in sections:
# #                     try:
# #                         section_title = section.text
# #                         # Find the content following this header until the next header
# #                         content = self._extract_section_content(section, driver)
# #                         if content:
# #                             # Store metadata along with content
# #                             doc_info = {
# #                                 'title': section_title,
# #                                 'content': content,
# #                                 'url': url,
# #                                 'section': section_title
# #                             }
# #                             documents.append(doc_info)
# #                     except Exception as e:
# #                         print(f"Error processing section: {str(e)}")
                
# #             except Exception as e:
# #                 print(f"Error fetching {url}: {str(e)}")
                
# #         driver.quit()
# #         return documents

# #     def _extract_section_content(self, section_element, driver) -> str:
# #         """Extract content for a specific section including code blocks."""
# #         try:
# #             next_section = section_element.find_element(By.XPATH, "following::div[contains(@class, 'notion-header-block')]")
# #             content = ""
# #             current = section_element
# #             while current != next_section:
# #                 # Handle code blocks specially
# #                 if 'notion-code-block' in current.get_attribute('class'):
# #                     content += f"\nCode Example:\n```\n{current.text}\n```\n"
# #                 else:
# #                     content += current.text + "\n"
# #                 current = current.find_element(By.XPATH, "following-sibling::*[1]")
# #             return content
# #         except:
# #             # If no next section is found, get all remaining content
# #             return section_element.find_element(By.XPATH, "following::*").text

# #     def chunk_documents(self, documents: List[Dict], chunk_size: int = 500) -> List[str]:
# #         """Split documents into smaller chunks while preserving metadata."""
# #         chunks = []
        
# #         for doc in documents:
# #             text = doc['content']
# #             words = text.split()
            
# #             for i in range(0, len(words), chunk_size // 2):
# #                 chunk = ' '.join(words[i:i + chunk_size])
# #                 if chunk:
# #                     chunk_id = len(chunks)
# #                     self.chunk_metadata[chunk_id] = {
# #                         'title': doc['title'],
# #                         'url': doc['url'],
# #                         'section': doc['section']
# #                     }
# #                     chunks.append(chunk)
                    
# #         return chunks

# #     def format_response(self, relevant_chunks: List[str], query: str) -> str:
# #         """Format response with improved readability and context."""
# #         response = "📚 Based on your question about Crustdata's API documentation:\n\n"
        
# #         # Group chunks by section
# #         sections = {}
# #         for i, chunk in enumerate(relevant_chunks):
# #             metadata = self.chunk_metadata.get(self.chunks.index(chunk), {})
# #             section = metadata.get('section', 'General')
# #             if section not in sections:
# #                 sections[section] = []
# #             sections[section].append((chunk, metadata))
        
# #         # Format response by section
# #         for section, chunks_with_metadata in sections.items():
# #             response += f"### {section}\n\n"
            
# #             for chunk, metadata in chunks_with_metadata:
# #                 # Clean up code blocks
# #                 chunk = self._format_code_blocks(chunk)
                
# #                 # Add chunk content
# #                 response += chunk.strip() + "\n\n"
                
# #                 # Add source link
# #                 if metadata.get('url'):
# #                     response += f"🔗 [View full documentation]({metadata['url']})\n\n"
        
# #         # Add follow-up suggestions based on the query and chunks
# #         follow_ups = self._generate_follow_up_questions(query, relevant_chunks)
# #         if follow_ups:
# #             response += "\n💡 You might also want to know:\n"
# #             for question in follow_ups:
# #                 response += f"- {question}\n"
        
# #         return response

# #     def _format_code_blocks(self, text: str) -> str:
# #         """Format code blocks with proper markdown."""
# #         # Detect curl commands or JSON blocks
# #         code_block_pattern = r'(curl[^`]+|{[^}]+})'
        
# #         def replace_with_code_block(match):
# #             code = match.group(1)
# #             return f"\n```\n{code}\n```\n"
            
# #         return re.sub(code_block_pattern, replace_with_code_block, text)

# #     def _generate_follow_up_questions(self, query: str, relevant_chunks: List[str]) -> List[str]:
# #         """Generate relevant follow-up questions based on the context."""
# #         common_follow_ups = {
# #             "authentication": ["How do I authenticate my API requests?", "Where can I find my API token?"],
# #             "error": ["What are the common error codes?", "How do I handle API errors?"],
# #             "limit": ["What are the API rate limits?", "How can I optimize my API usage?"],
# #             "filter": ["What other filters are available?", "How do I combine multiple filters?"],
# #             "region": ["How do I find valid region values?", "Can I search across multiple regions?"]
# #         }
        
# #         relevant_questions = set()
        
# #         # Add relevant follow-ups based on query keywords
# #         for keyword, questions in common_follow_ups.items():
# #             if keyword.lower() in query.lower():
# #                 relevant_questions.update(questions)
        
# #         # Add relevant follow-ups based on chunk content
# #         for chunk in relevant_chunks:
# #             for keyword, questions in common_follow_ups.items():
# #                 if keyword.lower() in chunk.lower():
# #                     relevant_questions.update(questions)
        
# #         return list(relevant_questions)[:3]  # Return top 3 most relevant questions

# #     def save_conversation(self, query: str, response: str):
# #         """Save conversation history."""
# #         self.conversation_history.append({
# #             'timestamp': datetime.now().isoformat(),
# #             'query': query,
# #             'response': response
# #         })

# #     def get_similar_past_queries(self, query: str, limit: int = 2) -> List[Dict]:
# #         """Find similar questions from conversation history."""
# #         if not self.conversation_history:
# #             return []
            
# #         past_queries = [h['query'] for h in self.conversation_history]
# #         query_vector = self.vectorizer.transform([query])
# #         past_vectors = self.vectorizer.transform(past_queries)
        
# #         similarities = cosine_similarity(query_vector, past_vectors)
# #         top_indices = similarities[0].argsort()[-limit:][::-1]
        
# #         return [self.conversation_history[i] for i in top_indices if similarities[0][i] > 0.3]

# #     def get_response(self, query: str) -> str:
# #         """Get enhanced response for a query."""
# #         # Check for similar past queries
# #         similar_queries = self.get_similar_past_queries(query)
# #         if similar_queries:
# #             response = "I found some similar questions you might find helpful:\n\n"
# #             for sq in similar_queries:
# #                 response += f"Q: {sq['query']}\n"
# #                 response += f"A: {sq['response']}\n\n"
# #             response += "Now, let me answer your current question:\n\n"
# #         else:
# #             response = ""
        
# #         # Get relevant chunks and format response
# #         relevant_chunks = self.get_relevant_chunks(query)
# #         formatted_response = self.format_response(relevant_chunks, query)
# #         response += formatted_response
        
# #         # Save to conversation history
# #         self.save_conversation(query, formatted_response)
        
# #         return response

# # def main():
# #     # Initialize agent
# #     agent = DocumentationChatAgent()
    
# #     # Process documentation
# #     docs_urls = [
# #         "https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c",
# #         "https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48"
# #     ]
    
# #     print("🤖 Initializing Documentation Chat Agent...")
# #     print("📚 Processing documentation...")
    
# #     try:
# #         agent.extract_text_from_notion(docs_urls)
# #         print("✅ Documentation processed successfully!")
        
# #         print("\n📱 Welcome to the Crustdata API Assistant!")
# #         print("❓ You can ask questions about:")
# #         print("   - API endpoints and their usage")
# #         print("   - Authentication and tokens")
# #         print("   - Filters and parameters")
# #         print("   - Common errors and troubleshooting")
# #         print("\nType 'quit' to exit, 'help' for tips, or ask your question!")
        
# #         while True:
# #             query = input("\n👤 Your question: ")
            
# #             if query.lower() == 'quit':
# #                 print("\n👋 Thanks for using the Crustdata API Assistant!")
# #                 break
                
# #             if query.lower() == 'help':
# #                 print("\n💡 Tips for getting better answers:")
# #                 print("- Be specific about which API endpoint you're asking about")
# #                 print("- Include error messages if you're troubleshooting")
# #                 print("- Ask about one topic at a time")
# #                 print("- Use keywords like 'example', 'error', or 'how to'")
# #                 continue
                
# #             try:
# #                 print("\n🤖 Finding the best answer for you...")
# #                 response = agent.get_response(query)
# #                 print("\nResponse:", response)
# #             except Exception as e:
# #                 print(f"❌ Error: {str(e)}")
# #                 print("Please try rephrasing your question or type 'help' for tips.")
                
# #     except Exception as e:
# #         print(f"❌ Error during initialization: {str(e)}")

# # if __name__ == "__main__":
# #     main()


# import requests
# from bs4 import BeautifulSoup
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
# from typing import List, Dict, Tuple
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import json
# from datetime import datetime
# import re

# class DocumentationChatAgent:
#     def __init__(self):
#         self.vectorizer = TfidfVectorizer(
#             stop_words='english',
#             max_df=0.95,
#             min_df=2,
#             ngram_range=(1, 2)
#         )
#         self.chunks = []
#         self.vectors = None
#         self.conversation_history = []
#         self.chunk_metadata = {}
        
#     def extract_text_from_notion(self, urls: List[str]) -> List[Dict]:
#         """Extract text content from Notion pages using Selenium."""
#         documents = []
        
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
        
#         driver = webdriver.Chrome(options=chrome_options)
        
#         for url in urls:
#             try:
#                 driver.get(url)
#                 WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, ".notion-page-content"))
#                 )
                
#                 page_content = driver.find_element(By.CSS_SELECTOR, ".notion-page-content").text
#                 sections = driver.find_elements(By.CSS_SELECTOR, ".notion-header-block")
                
#                 for section in sections:
#                     try:
#                         section_title = section.text
#                         content = self._extract_section_content(section, driver)
#                         if content:
#                             doc_info = {
#                                 'title': section_title,
#                                 'content': content,
#                                 'url': url,
#                                 'section': section_title
#                             }
#                             documents.append(doc_info)
#                     except Exception as e:
#                         print(f"Error processing section: {str(e)}")
#             except Exception as e:
#                 print(f"Error fetching {url}: {str(e)}")
        
#         driver.quit()
#         return documents

#     def _extract_section_content(self, section_element, driver) -> str:
#         """Extract content for a section."""
#         try:
#             content = []
#             sibling = section_element.find_element(By.XPATH, "following-sibling::*[1]")
            
#             while sibling and 'notion-header-block' not in sibling.get_attribute('class'):
#                 if 'notion-code-block' in sibling.get_attribute('class'):
#                     content.append(f"\nCode Example:\n```\n{sibling.text}\n```\n")
#                 else:
#                     content.append(sibling.text)
#                 sibling = sibling.find_element(By.XPATH, "following-sibling::*[1]")
#         except Exception:
#             pass
        
#         return "\n".join(content)

#     def chunk_documents(self, documents: List[Dict], chunk_size: int = 500) -> List[str]:
#         """Split documents into smaller chunks while preserving metadata."""
#         chunks = []
        
#         for doc in documents:
#             text = doc['content']
#             words = text.split()
            
#             for i in range(0, len(words), chunk_size // 2):
#                 chunk = ' '.join(words[i:i + chunk_size])
#                 if chunk:
#                     chunk_id = len(chunks)
#                     self.chunk_metadata[chunk_id] = {
#                         'title': doc['title'],
#                         'url': doc['url'],
#                         'section': doc['section']
#                     }
#                     chunks.append(chunk)
                    
#         return chunks

#     def format_response(self, relevant_chunks: List[str], query: str) -> str:
#         """Format response for the query."""
#         response = "📚 Based on your question about the documentation:\n\n"
        
#         sections = {}
#         for i, chunk in enumerate(relevant_chunks):
#             metadata = self.chunk_metadata.get(self.chunks.index(chunk), {})
#             section = metadata.get('section', 'General')
#             if section not in sections:
#                 sections[section] = []
#             sections[section].append((chunk, metadata))
        
#         for section, chunks_with_metadata in sections.items():
#             response += f"### {section}\n\n"
            
#             for chunk, metadata in chunks_with_metadata:
#                 chunk = self._format_code_blocks(chunk)
#                 response += chunk.strip() + "\n\n"
#                 if metadata.get('url'):
#                     response += f"🔗 [View full documentation]({metadata['url']})\n\n"
        
#         return response

#     def _format_code_blocks(self, text: str) -> str:
#         """Format code blocks."""
#         code_block_pattern = r'(curl[^`]+|{[^}]+})'
        
#         def replace_with_code_block(match):
#             code = match.group(1)
#             return f"\n```\n{code}\n```\n"
            
#         return re.sub(code_block_pattern, replace_with_code_block, text)

#     def save_conversation(self, query: str, response: str):
#         """Save conversation."""
#         self.conversation_history.append({
#             'timestamp': datetime.now().isoformat(),
#             'query': query,
#             'response': response
#         })

#     def get_response(self, query: str) -> str:
#         """Get response for a query."""
#         if not self.chunks:
#             raise ValueError("Documentation not processed. Please load documents first.")
        
#         query_vector = self.vectorizer.transform([query])
#         similarities = cosine_similarity(query_vector, self.vectors)
#         top_indices = similarities[0].argsort()[-3:][::-1]
        
#         relevant_chunks = [self.chunks[i] for i in top_indices if similarities[0][i] > 0.1]
#         if not relevant_chunks:
#             return "Sorry, I couldn't find anything relevant in the documentation."
        
#         formatted_response = self.format_response(relevant_chunks, query)
#         self.save_conversation(query, formatted_response)
        
#         return formatted_response

#     def process_documents(self, documents: List[Dict]):
#         """Vectorize document chunks."""
#         self.chunks = self.chunk_documents(documents)
#         self.vectors = self.vectorizer.fit_transform(self.chunks)

# def main():
#     agent = DocumentationChatAgent()
    
#     docs_urls = [
#         "https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c",
#         "https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48"
#     ]
    
#     print("🤖 Initializing Documentation Chat Agent...")
    
#     try:
#         documents = agent.extract_text_from_notion(docs_urls)
#         agent.process_documents(documents)
        
#         print("\n📱 Welcome to the Documentation Chat Assistant!")
#         print("\nType 'quit' to exit or ask your question!")
        
#         while True:
#             query = input("\n👤 Your question: ")
#             if query.lower() == 'quit':
#                 print("👋 Goodbye!")
#                 break
            
#             try:
#                 response = agent.get_response(query)
#                 print("\n🤖 Response:\n", response)
#             except Exception as e:
#                 print(f"Error: {str(e)}")
#     except Exception as e:
#         print(f"Initialization Error: {str(e)}")

# if __name__ == "__main__":
#     main()
