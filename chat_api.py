from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
import os
import openai

# Load environment variables
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

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
        print("DB loaded successfully.")
        print("Querying...", query_text)
        # Search the DB
        results = db.similarity_search_with_relevance_scores(query_text, k=3)
        # print("Results:", results)
        if len(results) == 0 or results[0][1] < 0.7:
            return jsonify({"response": "I'm unable to find an appropriate answer..."})

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = ChatOpenAI()
        response_text = model.predict(prompt)

        sources = [doc.metadata.get("source", None) for doc, _score in results]
        formatted_response = {
            "response": response_text,
            "sources": sources
        }
        return jsonify(formatted_response)

