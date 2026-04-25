from langchain_core.prompts.chat import ChatPromptTemplate 
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from decouple import config
from operator import itemgetter
from langchain_openai import ChatOpenAI
from src.Qdrant import vectorstore

model=ChatOpenAI(
    model="gpt-5.4",
    temperature=0.7,
    openai_api_key=config("OPENAI_API_KEY"),
)

prompt_template= """
 Answer the question based on the context in a concise manner only from the website
and using bullet points where applicable
context :{context}
Question:{question}
Response:
"""
prompt=ChatPromptTemplate.from_template(prompt_template)
retriever = vectorstore.as_retriever()

def createchain():
    chain = (
        {
            "context":retriever.with_config(top_k=4),
            "question": RunnablePassthrough()

        }|RunnableParallel({
            "response": prompt|model,
            "context": itemgetter("context")
          }
               )
        
    )
    return chain

def return_answer(question:str):
    chain= createchain()
    response= chain.invoke(question)
    answer=response["response"].content
    context=response["context"]
    return  {
        "answer":answer,
        "context": context
    }
    
    
