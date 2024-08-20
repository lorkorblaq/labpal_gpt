GPT AI App API
Overview

This repository contains a Flask-based API that leverages OpenAI's GPT-3.5-turbo model to provide responses to biomedical science-related queries. The API is designed to serve as a laboratory assistant, named Labpal, specializing in answering questions for biomedical scientists. It uses a combination of vector search through Chroma and GPT to generate accurate and contextually relevant responses.
Features

    Biomedical Science AI Assistant: Labpal is designed to assist with biomedical science queries.
    Contextual Query Handling: Utilizes Chroma vector store for similarity search with relevance scores to provide accurate responses.
    OpenAI Integration: Integrates with OpenAI's GPT-3.5-turbo for generating responses based on provided context or general knowledge.
    API Endpoints: Provides a RESTful API for querying the assistant.

Installation
Prerequisites

    Python 3.8+
    OpenAI API Key
    Docker (optional, for containerization)

Setup

    Clone the repository:

    bash

git clone https://github.com/yourusername/gpt-ai-app-api.git
cd gpt-ai-app-api

Create and activate a virtual environment:

bash

python3 -m venv venv
source venv/bin/activate

Install the required packages:

bash

pip install -r requirements.txt

Set up environment variables:

    Create a .env file in the root directory.

    Add your OpenAI API key:

    makefile

    OPENAI_API_KEY=your_openai_api_key_here

Run the application:

bash

    python app.py

The API will be available at http://127.0.0.1:5000/

Usage
API Endpoints
Query the Assistant

    Endpoint: /query

    Method: POST

    Parameters:
        query (string): The query text you want to ask Labpal.

    Example Request:

    bash

curl -X POST http://127.0.0.1:5000/query \
-H "Content-Type: application/json" \
-d '{"query": "What is the process of PCR in biomedical research?"}'

Example Response:

json

    {
      "response": "Polymerase Chain Reaction (PCR) is a method used in molecular biology to amplify a single or a few copies of a piece of DNA...",
      "sources": ["source1.pdf", "source2.pdf"]
    }

Command-Line Interface (CLI)

You can also use the assistant via a CLI interface.

bash

python cli.py "What is the process of PCR in biomedical research?"

Error Handling

The API includes error handlers to log exceptions and return error messages in JSON format.
Logging

Logging is configured to the INFO level. Logs will provide information about the loading of the database and the querying process.
Dockerization (Optional)

You can containerize the application using Docker.

    Build the Docker image:

    bash

docker build -t gpt-ai-app-api .

Run the container:

bash

    docker run -p 5000:5000 gpt-ai-app-api

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    OpenAI for providing the GPT-3.5-turbo model.
    LangChain for enabling advanced prompting and chaining capabilities.
    Chroma for the vector store functionality.
