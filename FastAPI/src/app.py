from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rag import return_answer
from Qdrant import upload_website_to_collection
from pydantic import BaseModel
 
from fastapi.middleware.cors import CORSMiddleware



chatapp= FastAPI (
    title="Chatbot using RAG",
    description="First ChatBot API",
    version= "1.0",
 )


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://claude-rag-chatbot.vercel.app/",
]

class Qmessage(BaseModel):
    message: str

class Umessage(BaseModel):
    mes: str

chatapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@chatapp.post("/chat",description="Enter your query")
def chat(message: Qmessage):
    response=return_answer(message.message)
   
    response_content= {
        "question": message.message,
        "answer": response["answer"],
        "document": [doc.dict() for doc in response["context"]]   
    }
    
    return JSONResponse(content=response_content,status_code=200)
    #print("Answer",response_content)

@chatapp.post("/load_doc",description="Enter your website link")
async def load_doc( url: Umessage):
    try:
        #return url
        response= upload_website_to_collection(url.mes)
        return JSONResponse(content={"response":response},status_code=200)
        #print("url res",response)
    except Exception as e:
       return JSONResponse(content={"Error":str(e)},status_code=200)

