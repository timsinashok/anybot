Something Similar
https://www.runllm.com


# Cerebras Documentation Assistant

A RAG-powered documentation chatbot that uses Groq API for LLM responses and ChromaDB for vector search.

## Features

- Interactive chat interface to query Cerebras documentation
- Retrieval-augmented generation (RAG) for accurate, context-aware responses
- Source citations with expandable references
- Responsive design for desktop and mobile

## Tech Stack

- **Backend**: FastAPI, ChromaDB, Groq API, BAAI/bge-m3 embeddings
- **Frontend**: React, Axios

## Setup

### Backend

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn chromadb groq
   ```

2. Set environment variables:
   ```bash
   export GROQ_API_KEY="your-groq-api-key"
   ```

3. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### Frontend

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the React development server:
   ```bash
   npm start
   ```

3. If you encounter `ajv` errors, install compatible versions:
   ```bash
   npm install --save-dev ajv@^7 ajv-keywords@^4
   ```

## Usage

1. Open your browser to http://localhost:3000
2. Type your question about Cerebras documentation in the input field
3. View the AI response with source citations
4. Click "Show Sources" to see the retrieved document chunks

## API Endpoints

- `GET /health` - Check API status
- `GET /query?query={text}&top_n={number}` - Query the RAG system
- `POST /query` - Query with JSON payload