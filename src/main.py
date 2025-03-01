from fastapi import FastAPI, HTTPException, Query, Body, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import uvicorn
import os
import time
import logging
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Import database
from database import ChromaDatabase

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# resolving issue with tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize FastAPI app
app = FastAPI(
    title="API Interaction Agents Platform",
    description="Platform for interacting with API documentation, testing endpoints, and providing information about API usage",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define request/response models
class QueryRequest(BaseModel):
    query: str = Field(..., description="The natural language query to process")
    top_n: Optional[int] = Field(5, description="Number of documents to retrieve")
    similarity_threshold: Optional[float] = Field(None, description="Optional similarity threshold (0-1)")

class SourceInfo(BaseModel):
    file_name: str
    source_path: str
    chunk_index: int

class DocumentResult(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None
    similarity: Optional[float] = None
    source: Optional[SourceInfo] = None

class QueryResponse(BaseModel):
    query: str
    results: List[DocumentResult]
    llm_response: str
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    database: Dict[str, Any]
    llm_provider: Dict[str, Any]
    uptime: float

# LLM Provider abstraction layer
class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, query: str, context_docs: List[str]) -> str:
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        pass

# Implementation for Groq
class GroqLLMProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str = "llama-3.1-8b-instant"):
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
            self.model_name = model_name
            self.status = "connected"
        except Exception as e:
            logger.error(f"Error initializing Groq client: {e}")
            self.client = None
            self.model_name = model_name
            self.status = f"error: {str(e)}"
    
    def generate_response(self, query: str, context_docs: List[str]) -> str:
        """Generate a response using Groq API based on retrieved documents"""
        if not self.client:
            return "LLM provider not initialized. Please check the configuration."
        
        # Combine the retrieved documents into context
        context = "\n\n".join(context_docs)
        
        # Create system prompt with RAG context
        system_prompt = f"""
        Instructions:
        - Be helpful and answer questions concisely based on the provided context.
        - If the context doesn't contain relevant information, say 'I don't have enough information to answer this question.'
        - Provide specific information from the context when available.
        - When referencing information, mention which document it came from if possible.
        
        Context:
        {context}
        """

        print(system_prompt)
        
        try:
            start_time = time.time()
            chat_completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
            )
            response = chat_completion.choices[0].message.content
            
            logger.info(f"LLM response generated in {time.time() - start_time:.2f} seconds")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "provider": "Groq",
            "model": self.model_name,
            "status": self.status
        }

# Rate limiter middleware
class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.request_history = {}
        
    async def __call__(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old entries
        self.request_history = {ip: times for ip, times in self.request_history.items() 
                             if times and times[-1] > current_time - 60}
        
        # Initialize if new client
        if client_ip not in self.request_history:
            self.request_history[client_ip] = []
        
        # Check rate limit
        if len(self.request_history[client_ip]) >= self.requests_per_minute:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
        
        # Record request
        self.request_history[client_ip].append(current_time)
        return True

# Global instances
db = None
llm_provider = None
start_time = time.time()

@app.on_event("startup")
async def startup_event():
    """Initialize the database and LLM provider when the application starts"""
    global db, llm_provider
    print("Initializing database and LLM provider...")
    
    # Initialize LLM provider
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if groq_api_key:
        llm_provider = GroqLLMProvider(api_key=groq_api_key)
        logger.info("LLM provider initialized.")
    else:
        logger.warning("GROQ_API_KEY not found in environment variables.")
    
    # Initialize database
    try:
        db_host = os.environ.get("CHROMADB_HOST", "localhost")
        db_port = int(os.environ.get("CHROMADB_PORT", "8000"))
        
        db = ChromaDatabase(
            "api_documentation", 
            host=db_host, 
            port=db_port, 
            model_name="BAAI/bge-m3"
        )
 
        # Check if documents are already stored
        stats = db.get_collection_stats()
        print(stats)
        if stats["document_count"] > 0:
            print(f"Collection already contains {stats['document_count']} document chunks.")
            logger.info(f"Collection already contains {stats['document_count']} document chunks.")
        else:
            print("Storing documents in the database...")
            # Store documents if needed
            # data_dir = os.environ.get("API_DOCS_DIR")
            if os.path.exists("./scraped_data"):
                logger.info(f"Storing API documentation from scraped_data...")
                result = db.store_documents('./scraped_data')
                logger.info(f"Stored {result['document_count']} documents with {result['chunk_count']} chunks.")
            else:
                logger.warning(f"API documentation directory {data_dir} not found.")
        
        logger.info("Database setup complete.")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)

@app.get("/", summary="Root endpoint", tags=["Information"])
async def root():
    """Root endpoint that returns API information"""
    return {
        "name": "API Interaction Agents Platform",
        "version": "0.1.0",
        "endpoints": {
            "/query": "POST endpoint to query the RAG system",
            "/health": "GET endpoint to check API health",
            "/docs": "API documentation (Swagger UI)"
        }
    }

@app.get("/health", response_model=HealthResponse, summary="Health check", tags=["Information"])
async def health_check():
    """Health check endpoint providing status of all services"""
    global db, llm_provider, start_time
    
    database_status = {"status": "not connected"}
    if db is not None:
        try:
            stats = db.get_collection_stats()
            database_status = {
                "status": "connected", 
                **stats
            }
        except Exception as e:
            database_status = {"status": "error", "message": str(e)}
    
    llm_status = {"status": "not connected"}
    if llm_provider is not None:
        llm_status = llm_provider.get_status()
    
    uptime = time.time() - start_time
    
    return {
        "status": "healthy" if db is not None and llm_provider is not None else "warning",
        "database": database_status,
        "llm_provider": llm_status,
        "uptime": uptime
    }

@app.post(
    "/query", 
    response_model=QueryResponse, 
    dependencies=[Depends(RateLimiter())],
    summary="Query the RAG system",
    tags=["RAG"],
    description="Query the RAG system with a natural language question to retrieve relevant API documentation and generate a response"
)
async def query(request: QueryRequest):
    """
    Query the RAG system with a natural language question
    
    - **query**: The question to answer
    - **top_n**: Number of relevant passages to retrieve (default: 5)
    - **similarity_threshold**: Optional threshold to filter results (0-1)
    
    Returns document chunks, generated answer, and metadata about the search
    """
    global db, llm_provider
    
    if db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    if llm_provider is None:
        raise HTTPException(status_code=503, detail="LLM provider not initialized")
    
    try:
        # Get query results
        results = db.query_rag(
            request.query, 
            top_n=request.top_n,
            similarity_threshold=request.similarity_threshold
        )
        print("Query results:", results)
        # Format the documents
        documents = results.get('documents', [[]])[0] if results else []
        metadatas = results.get('metadatas', [[]])[0] if results else []
        distances = results.get('distances', [[]])[0] if results else []
        
        # Prepare document results
        doc_results = []
        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
            source_info = SourceInfo(
                file_name=meta.get('file_name', 'unknown'),
                source_path=meta.get('source', 'unknown'),
                chunk_index=meta.get('chunk_index', 0)
            ) if meta else None
            
            doc_results.append(DocumentResult(
                content=doc,
                metadata=meta,
                similarity=1.0 - dist,  # Convert distance to similarity
                source=source_info
            ))
        
        print("Documents retrieved:", documents)
        # Generate LLM response
        llm_response = llm_provider.generate_response(request.query, documents)
        
        # Add metadata about the query
        metadata = {
            "total_results": len(documents),
            "top_n": request.top_n,
            "query_time": results.get('query_time', 0),
            "similarity_threshold": request.similarity_threshold
        }
        
        return QueryResponse(
            query=request.query,
            results=doc_results,
            llm_response=llm_response,
            metadata=metadata
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)













# from database import ChromaDatabase
# from fastapi import FastAPI, HTTPException, Query, Body
# from pydantic import BaseModel
# from typing import List, Optional
# import uvicorn
# import os
# from fastapi.middleware.cors import CORSMiddleware
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()
# app = FastAPI(title="Cerebras RAG API", description="API for querying Cerebras documents using RAG")

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )


# # Global database instance
# db = None
# groq_client = None

# class QueryRequest(BaseModel):
#     query: str
#     top_n: Optional[int] = 5

# class QueryResponse(BaseModel):
#     results: List[str]
#     llm_response: str
#     metadata: Optional[dict] = None

# @app.on_event("startup")
# async def startup_event():
#     """Initialize the database and Groq client when the application starts"""
#     global db, groq_client
    
#     # Initialize Groq client
#     try:
#         # Check if GROQ_API_KEY is set
#         groq_api_key = os.environ.get("GROQ_API_KEY")
#         if not groq_api_key:
#             print("Warning: GROQ_API_KEY environment variable not set")
#         else:
#             groq_client = Groq(api_key=groq_api_key)
#             print("Groq client initialized successfully")
#     except Exception as e:
#         print(f"Error initializing Groq client: {e}")
    
#     # Initialize database if first time running, otherwise check if documents are already stored
#     try:
#         db = ChromaDatabase("cerebras", model_name="BAAI/bge-m3")
#         print(f"Collection: {db.collection.name}")

#         # Check if documents are already stored
#         doc_count = db.collection.count()
#         if doc_count > 0:
#             print(f"Documents already stored in the database: {doc_count} chunks.")
#         else:
#             # Store documents in the database
#             print("Storing documents in the database...")
#             db.store_documents("../scraped_data")
#             print(f"Now containing {db.collection.count()} document chunks.")
#         print("\nDatabase setup complete.")
#     except Exception as e:
#         print(f"Error during startup: {e}")

# @app.get("/")
# async def root():
#     """Root endpoint that returns API information"""
#     return {
#         "message": "Cerebras RAG API is running",
#         "endpoints": {
#             "/query": "POST endpoint to query the RAG system",
#             "/health": "GET endpoint to check API health"
#         }
#     }

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     global db, groq_client
#     status = {"database": "not connected", "groq": "not connected"}
    
#     if db is None:
#         status["database"] = "not initialized"
#     else:
#         try:
#             count = db.collection.count()
#             status["database"] = {
#                 "status": "connected", 
#                 "document_count": count,
#                 "embedding_model": db.embed_model.model_name
#             }
#         except Exception as e:
#             status["database"] = {"status": "error", "message": str(e)}
    
#     if groq_client is None:
#         status["groq"] = "not initialized"
#     else:
#         status["groq"] = "connected"
    
#     return {"status": "healthy" if db is not None and groq_client is not None else "warning", **status}

# def generate_groq_response(query, context_docs):
#     """Generate a response using Groq API based on retrieved documents"""
#     global groq_client
    
#     if not groq_client:
#         return "Groq client not initialized. Please check your API key."
    
#     # Combine the retrieved documents into context
#     context = "\n\n".join(context_docs)
    
#     # Create system prompt with RAG context
#     system_prompt = f"""
#     Instructions:
#     - Be helpful and answer questions concisely based on the provided context.
#     - If the context doesn't contain relevant information, say 'I don't have enough information to answer this question.'
#     - Provide specific information from the context when available.
    
#     Context:
#     {context}
#     """
    
#     try:
#         chat_completion = groq_client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": query}
#             ]
#         )
#         response = chat_completion.choices[0].message.content
        
#         return response
#     except Exception as e:
#         return f"Error generating response: {str(e)}"

# @app.post("/query", response_model=QueryResponse)
# async def query(request: QueryRequest):
#     """
#     Query the RAG system with a question
#     """
#     global db
#     if db is None:
#         raise HTTPException(status_code=503, detail="Database not initialized")
    
#     try:
#         # Get query results
#         results = db.query_rag(request.query, top_n=request.top_n)
        
#         # Format the response
#         documents = results['documents'][0] if results and 'documents' in results and results['documents'] else []
        
#         # Generate LLM response using Groq
#         llm_response = generate_groq_response(request.query, documents)
        
#         # Add metadata about the query
#         metadata = {
#             "total_results": len(documents),
#             "top_n": request.top_n,
#             "distances": results.get('distances', [[]])[0] if results and 'distances' in results else []
#         }
        
#         return QueryResponse(results=documents, llm_response=llm_response, metadata=metadata)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# if __name__ == "__main__":
#     # Run the FastAPI app using Uvicorn
#     port = int(os.environ.get("PORT", 8001))
#     uvicorn.run(app, host="0.0.0.0", port=port)
