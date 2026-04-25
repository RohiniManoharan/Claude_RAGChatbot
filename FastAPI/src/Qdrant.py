from langchain_qdrant  import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from decouple import config

quadrant_Api_key = config("QDRANT_API_KEY")
quadrant_url = config("QDRANT_URL")
collection_name = "website_AI"

client= QdrantClient(
    url= quadrant_url,
    api_key=quadrant_Api_key,
    timeout=30
)

def create_collection(collection_name):
 
    client.create_collection(collection_name=collection_name,
                             vectors_config=VectorParams(
                                 size=1536,
                                 distance=Distance.COSINE))
 

    
   # print (f"connections {collection_name} created succesfully")


    #create_collection(collection_name)
 

vectorstore = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=config("OPENAI_API_KEY")
    )
)
text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
    )
def upload_website_to_collection(url:str):
    loader=WebBaseLoader(url)
    docs= loader.load_and_split(text_splitter)
    for doc in docs:
        doc.metadata={"source_url":url}

    vectorstore.add_documents(docs)
    return f"succesfully uploaded {len(docs)} documents to collection {collection_name}"

