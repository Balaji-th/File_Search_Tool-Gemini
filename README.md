# File Search Tool

 **File Search Tool**, a fully managed RAG system built directly into the Gemini API that abstracts away the retrieval pipeline so you can focus on building. File Search provides a simple, integrated and scalable way to ground Gemini with your data, delivering responses that are more accurate, relevant and verifiable.
![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/FileSearch-Keyword_RD2-V01.width-1300.png)

## How it works

The application allows you to upload a PDF file and ask questions about its content. The backend uses the Gemini API's file search capabilities to find the relevant information within the document and provide an answer.

## How to run this application

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/file-search-tool.git
    cd file-search-tool
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up your environment variables:**
    Create a `.env` file in the root of the project and add your Google API key:
    ```
    GOOGLE_API_KEY=your-api-key
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```
5.  Open your browser and navigate to `http://localhost:5000`.

<img width="1848" height="852" alt="image" src="https://github.com/user-attachments/assets/7c929d3f-0dbe-43db-b13a-76a160f822ff" />


## File Search Gemini API

This application is powered by the Google Gemini API. You can learn more about the file search capabilities in the official Google AI blog post.

[Learn more about the File Search Gemini API](https://blog.google/technology/developers/file-search-gemini-api/)


