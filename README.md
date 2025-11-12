# File Search Tool

This repository contains a simple web application that demonstrates the power of the Google Gemini API for file searching.

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

## File Search Gemini API

This application is powered by the Google Gemini API. You can learn more about the file search capabilities in the official Google AI blog post.

[Learn more about the File Search Gemini API](https://blog.google/technology/developers/file-search-gemini-api/)

![File Search Gemini API](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image_1_hP4a44q.width-1200.format-webp.webp)
