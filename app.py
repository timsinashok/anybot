from flask import Flask, request, jsonify
# from DocumentationChatAgent import DocumentationChatAgent
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3001"], methods=["POST", "OPTIONS"], allow_headers=["Content-Type"])

# # Instantiate the DocumentationChatAgent
# agent = DocumentationChatAgent()

docs_urls = [
    "https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c",
    "https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48"
]

# # Initialize the Documentation Chat Agent
# print("🤖 Initializing Documentation Chat Agent...")
# try:
#     agent.process_documentation(docs_urls)
#     print("📘 Documentation processed successfully!")
# except Exception as e:
#     print(f"Initialization Error: {str(e)}")


@app.route('/api/create-bot', methods=['POST', 'OPTIONS'])
def create_bot():
    return jsonify({"message": "Bot created successfully"}), 200

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

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


