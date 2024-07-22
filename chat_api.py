from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
import os
from openai import OpenAI
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv(find_dotenv())
openai_key = os.getenv('OPENAI_API_KEY')

if not openai_key:
    logging.error("OPENAI_API_KEY is not set. Please check your .env file.")
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

client = OpenAI(api_key=openai_key)

CHROMA_PATH = "chroma"

# Assistant persona
ASSISTANT_NAME = "Labpal"
ASSISTANT_ROLE = "biomedical scientist"

INTRO_PROMPT_TEMPLATE = """
Hy, I'm {name}, an AI laboratory assistant, designed to help with biomedical science questions. 
How can I assist you today?
"""

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above given snippets from an IFU, give the answer like you were asked by a biomedical scientist: {question}
"""

GENERAL_PROMPT_TEMPLATE = """
You are an AI assistant named {name}, designed to help with biomedical science questions. 
You can call me {name}. 

Question: {question}

Answer the question as best as you can based on your knowledge and training.
"""

# Initialize assistant persona and store the initial message
intro_prompt = ChatPromptTemplate.from_template(INTRO_PROMPT_TEMPLATE).format(name=ASSISTANT_NAME)
intro_response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": intro_prompt},
    ],
    max_tokens=250,
    n=1,
    stop=None,
    temperature=0.7)
assistant_intro = intro_response.choices[0].message.content.strip()

app = Flask(__name__)
api = Api(app)

class QueryChat(Resource):
    def post(self):
        # Create CLI parser
        chat_api_parser = reqparse.RequestParser()
        chat_api_parser.add_argument("query", type=str, help="The query text.", required=True)
        args = chat_api_parser.parse_args()
        query_text = args["query"]

        # Prepare the DB
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        logging.info("DB loaded successfully.")
        logging.info("Querying... %s", query_text)

        # Search the DB
        results = db.similarity_search_with_relevance_scores(query_text, k=3)

        if len(results) == 0 or results[0][1] < 0.7:
            # If no relevant results, use a general response template
            general_prompt_template = ChatPromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)
            general_prompt = general_prompt_template.format(name=ASSISTANT_NAME, question=query_text)
            response = client.chat.completions.create(model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": assistant_intro},
                    {"role": "user", "content": general_prompt}
                ],
                max_tokens=250,
                n=1,
                stop=None,
                temperature=0.7)
            response_text = response.choices[0].message.content.strip()
            formatted_response = {"response": response_text}
            logging.info("Query completed")
            return jsonify(formatted_response)
        else:
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, question=query_text)

            response = client.chat.completions.create(model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": assistant_intro},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                n=1,
                stop=None,
                temperature=0.7)
            response_text = response.choices[0].message.content.strip()
            sources = [doc.metadata.get("source", None) for doc, _score in results]
            formatted_response = {
                "response": response_text,
                "sources": sources
            }
            logging.info("Query completed")
            return jsonify(formatted_response)

# Add Flask error handlers for better logging
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error("An error occurred", exc_info=True)
    return jsonify({"error": str(e)}), 500

