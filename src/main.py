from database import ChromaDatabase
from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Cerebras RAG API", description="API for querying Cerebras documents using RAG")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Global database instance
db = None
groq_client = None

class QueryRequest(BaseModel):
    query: str
    top_n: Optional[int] = 5

class QueryResponse(BaseModel):
    results: List[str]
    llm_response: str
    metadata: Optional[dict] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the database and Groq client when the application starts"""
    global db, groq_client
    
    # Initialize Groq client
    try:
        # Check if GROQ_API_KEY is set
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            print("Warning: GROQ_API_KEY environment variable not set")
        else:
            groq_client = Groq(api_key=groq_api_key)
            print("Groq client initialized successfully")
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
    
    # Initialize database if first time running, otherwise check if documents are already stored
    try:
        db = ChromaDatabase("cerebras", model_name="BAAI/bge-m3")
        print(f"Collection: {db.collection.name}")

        # Check if documents are already stored
        doc_count = db.collection.count()
        if doc_count > 0:
            print(f"Documents already stored in the database: {doc_count} chunks.")
        else:
            # Store documents in the database
            print("Storing documents in the database...")
            db.store_documents("../scraped_data")
            print(f"Now containing {db.collection.count()} document chunks.")
        print("\nDatabase setup complete.")
    except Exception as e:
        print(f"Error during startup: {e}")

@app.get("/")
async def root():
    """Root endpoint that returns API information"""
    return {
        "message": "Cerebras RAG API is running",
        "endpoints": {
            "/query": "POST endpoint to query the RAG system",
            "/health": "GET endpoint to check API health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global db, groq_client
    status = {"database": "not connected", "groq": "not connected"}
    
    if db is None:
        status["database"] = "not initialized"
    else:
        try:
            count = db.collection.count()
            status["database"] = {
                "status": "connected", 
                "document_count": count,
                "embedding_model": db.embed_model.model_name
            }
        except Exception as e:
            status["database"] = {"status": "error", "message": str(e)}
    
    if groq_client is None:
        status["groq"] = "not initialized"
    else:
        status["groq"] = "connected"
    
    return {"status": "healthy" if db is not None and groq_client is not None else "warning", **status}

def generate_groq_response(query, context_docs):
    """Generate a response using Groq API based on retrieved documents"""
    global groq_client
    
    if not groq_client:
        return "Groq client not initialized. Please check your API key."
    
    # Combine the retrieved documents into context
    context = "\n\n".join(context_docs)
    
    # Create system prompt with RAG context
    system_prompt = f"""
    Instructions:
    - Be helpful and answer questions concisely based on the provided context.
    - If the context doesn't contain relevant information, say 'I don't have enough information to answer this question.'
    - Provide specific information from the context when available.
    
    Context:
    {context}
    """
    
    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        response = chat_completion.choices[0].message.content
        
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the RAG system with a question
    """
    global db
    if db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    try:
        # Get query results
        results = db.query_rag(request.query, top_n=request.top_n)
        
        # Format the response
        documents = results['documents'][0] if results and 'documents' in results and results['documents'] else []
        
        # Generate LLM response using Groq
        llm_response = generate_groq_response(request.query, documents)
        
        # Add metadata about the query
        metadata = {
            "total_results": len(documents),
            "top_n": request.top_n,
            "distances": results.get('distances', [[]])[0] if results and 'distances' in results else []
        }
        
        return QueryResponse(results=documents, llm_response=llm_response, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
