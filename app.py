from flask import Flask, request, jsonify
from DocumentationChatAgent import DocumentationChatAgent
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"]) 

agent = DocumentationChatAgent()

docs_urls = [
    "https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c",
    "https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48"
]

def initialize_agent(docs_urls=docs_urls):
    print("🤖 Initializing Documentation Chat Agent...")
    try:
        documents = agent.extract_text_from_notion(docs_urls)
        agent.process_documentation(documents)
        print("📱 Documentation Chat Agent initialized successfully!")
    except Exception as e:
        print(f"Initialization Error: {str(e)}")

initialize_agent(docs_urls)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        response = agent.get_response(query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
