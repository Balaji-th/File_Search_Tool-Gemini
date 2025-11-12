# app.py

import os
import time
import tempfile
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

load_dotenv(override=True)

# --- Configuration ---
app = Flask(__name__)

# Initialize the GenAI client with an API key from an environment variable
# IMPORTANT: Set this environment variable before running the app!
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set. Please set it and restart the app.")

# --- Global State ---
# Create a single file search store to be reused for the app's lifetime.
# In a production multi-user app, you might create one store per user session.
print("Creating a new File Search Store...")
try:
    store = client.file_search_stores.create(display_name="Document Q&A Store")
    print(f"Successfully created store: {store.name}")
except Exception as e:
    print(f"Could not create a new store. Error: {e}")
    print("Attempting to list existing stores to find a reusable one...")
    stores = client.file_search_stores.list()
    if stores:
        store = stores[0] # Use the first available store
        print(f"Reusing existing store: {store.name}")
    else:
        raise RuntimeError("Failed to create or find a file search store.")


# --- Routes ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handles file upload and question, returns AI response."""
    if 'file' not in request.files or 'question' not in request.form:
        return jsonify({"error": "Missing file or question"}), 400

    file = request.files['file']
    question = request.form['question']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    # Use a temporary file to store the upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        file.save(tmp_file.name)
        temp_file_path = tmp_file.name

    try:
        print(f"Uploading {file.filename} to store {store.name}...")
        upload_op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=store.name,
            file=temp_file_path
        )

        # Wait for the upload to complete. This is a blocking call.
        # For a production app, consider using a background task queue.
        while not upload_op.done:
            time.sleep(2)
            print("Upload in progress...")
            upload_op = client.operations.get(upload_op)
        
        print("Upload complete.")

        # Generate content using the uploaded file
        print(f"Asking question: '{question}'")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=question,
            config=types.GenerateContentConfig(
                tools=[types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[store.name]
                    )
                )]
            )
        )

        answer = response.text
        
        # Extract grounding sources
        grounding = response.candidates[0].grounding_metadata
        sources = []
        if grounding:
            sources = list({c.retrieved_context.title for c in grounding.grounding_chunks})

        return jsonify({"answer": answer, "sources": sources})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred while processing your request."}), 500

    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)
        print(f"Cleaned up temporary file: {temp_file_path}")

# --- Main Execution ---
if __name__ == '__main__':
    # host='0.0.0.0' makes the server accessible from outside the Docker container
    app.run(host='0.0.0.0', port=5000, debug=True)