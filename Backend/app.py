from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os
import shutil
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)
CORS(app)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# Directory configurations
VECTORSTORE_DIR = "vectorstore"  # Path where FAISS files are stored
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

# Global variable to hold the latest vectorstore
latest_vectorstore_path = r'vectorstore'

# Load the FAISS vectorstore
def load_vectorstore():
    global latest_vectorstore_path
    if os.path.exists(VECTORSTORE_DIR):
        try:
            # Load the FAISS vectorstore
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            latest_vectorstore_path = VECTORSTORE_DIR
            return FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            logging.error(f"Failed to load vectorstore: {e}")
            return None
    else:
        logging.warning("No pre-existing vectorstore found.")
        return None


# Create a retrieval chain with the LLM
def create_retrieval_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 20})
    llm = ChatOpenAI(model="chatgpt-4o-latest", temperature=0.0, max_tokens=1000)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    return qa_chain


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        # Load the vectorstore
        vectorstore = load_vectorstore()
        if not vectorstore:
            return jsonify({'error': 'No vectorstore available. Please process the files first.'}), 400

        # Create retrieval chain
        qa_chain = create_retrieval_chain(vectorstore)

        # Run the chain with the user's question
        response = qa_chain.run(question)

        return jsonify({'answer': response}), 200
    except Exception as e:
        logging.error(f"Error during inference: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/process', methods=['POST'])
def process_files():
    global latest_vectorstore_path
    # Define your ingestion pipeline logic here
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Simulate loading documents
        documents = []  # Add your logic to load documents here
        # Example: Use your document loaders to process files and split them into chunks

        vectorstore = FAISS.from_documents(documents, embeddings)

        # Save the vectorstore
        vectorstore.save_local(VECTORSTORE_DIR)
        latest_vectorstore_path = VECTORSTORE_DIR

        return jsonify({'message': 'Files processed successfully.'}), 200
    except Exception as e:
        logging.error(f"Error processing files: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/delete_vectorstore', methods=['DELETE'])
def delete_vectorstore():
    try:
        # Delete the vectorstore directory
        if os.path.exists(VECTORSTORE_DIR):
            shutil.rmtree(VECTORSTORE_DIR)
            os.makedirs(VECTORSTORE_DIR, exist_ok=True)
            logging.info(f"Vectorstore deleted: {VECTORSTORE_DIR}")
            return jsonify({'message': 'Vectorstore deleted successfully.'}), 200
        else:
            return jsonify({'message': 'No vectorstore to delete.'}), 200
    except Exception as e:
        logging.error(f"Error deleting vectorstore: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


if __name__ == "__main__":
    # Flask app runs on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
