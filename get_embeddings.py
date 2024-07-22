from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")


class OpenAIEmbeddings:
    def __init__(self, api_key=api_key, model="text-embedding-ada-002"):
        self.api_key = api_key 
        self.model = model

    def embed(self, texts):
        client = OpenAI(api_key=self.api_key)
        # Use the updated OpenAI API for embeddings
        response = client.embeddings.create(model='text-embedding-ada-002', input=texts)
        embeddings = [item["embedding"] for item in response.data]
        return embeddings

    def embed_documents(self, texts):
        return self.embed(texts)





def get_embedding_function():
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    return embeddings




from openai import OpenAI

client = OpenAI(api_key=self.api_key,
api_key=self.api_key)
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")


class OpenAIEmbeddings:
    def __init__(self, api_key=api_key, model="text-embedding-ada-002"):
        self.api_key = api_key 
        self.model = model

    def embed(self, texts):
        # Use the updated OpenAI API for embeddings
        response = client.embeddings.create(model=self.model, input=texts)
        embeddings = [item["embedding"] for item in response.data]
        return embeddings

    def embed_documents(self, texts):
        return self.embed(texts)

def get_embedding_function():
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    return embeddings.embed_documents





from openai import OpenAI

client = OpenAI(api_key=self.api_key,
api_key=self.api_key)
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")


class OpenAIEmbeddings:
    def __init__(self, api_key=api_key, model="text-embedding-ada-002"):
        self.api_key = api_key 
        self.model = model

    def embed(self, texts):
        # Use the updated OpenAI API for embeddings
        response = client.embeddings.create(model=self.model, input=texts)
        embeddings = [item["embedding"] for item in response.data]
        return embeddings

    def embed_documents(self, texts):
        return self.embed(texts)

def get_embedding_function():
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    return embeddings.embed_documents
