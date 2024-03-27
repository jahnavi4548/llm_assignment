## Question and Answer System using Flask
This project implements a Question and Answer (Q&A) system using Flask, allowing users to upload a document and ask questions related to its content. The system utilizes Natural Language Processing (NLP) techniques to summarize the document and provide accurate answers to user queries.

## Installation
To run the web application on your local machine, make sure you have Python installed. Additionally, install the required Python packages listed in the requirements.txt file. You can install them using pip: pip install -r requirements.txt


## Getting Started
After installing the required packages, navigate to the project directory and run the Flask application by executing the following command in your terminal: python main.py
This will start the Flask server, and you can access the application in your web browser by visiting http://localhost:5000.

## Features
Document Upload: Users can upload a PDF file containing text data.
Text Summarization: The system automatically summarizes the uploaded document to provide an overview of its main points.
Question Asking: Users can ask questions related to the content of the uploaded document.
Question Answering: Utilizing NLP techniques, the system provides accurate answers to user queries based on the content of the document.
Error Handling: The application handles errors gracefully and provides informative error messages to users.
Usage
Upload Document: Navigate to the "Upload PDF File" page and upload a PDF document containing text data.

Ask Questions: After uploading the document, visit the "Ask Question" page to input your questions related to the document's content.

View Answers: The system will process your question and provide accurate answers based on the content of the uploaded document.
