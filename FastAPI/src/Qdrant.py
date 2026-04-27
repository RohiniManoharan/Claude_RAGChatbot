from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
import os

quadrant_api_key = os.environ.get("QDRANT_API_KEY")
quadrant_url = os.environ.get("QDRANT_URL")
collection_name = "website_AI"

client = QdrantClient(
    url=quadrant_url,
    api_key=quadrant_api_key,
    timeout=30
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    api_key=os.environ.get("OPENAI_API_KEY")
)

def create_collection():
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE
        )
    )

def get_vectorstore():
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings
    )

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)

def upload_website_to_collection(url: str):
    loader = WebBaseLoader(url)
    docs = loader.load_and_split(text_splitter)
    for doc in docs:
        doc.metadata = {"source_url": url}
    get_vectorstore().add_documents(docs)
    return f"successfully uploaded {len(docs)} documents to collection {collection_name}"