import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough , RunnableLambda

from core.vector_store import   build_vector_store , load_vector_store , get_retriever


def get_llm() :
    return ChatMistralAI(model="mistral-small-latest" , mistral_api_key = os.getenv("MISTRAL_API_KEY"))

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def build_rag_chain(transcript:str):
    vector_store = build_vector_store(transcript)
    retriever=get_retriever(vector_store , k=4)
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([("system",""" you are an expert meeting assistant answer the users question based only ont he meeting transcript provided  below
                                                if the answer is not found in the context say i ncould not find the answer in the transcript
                                                
                                                always be concidse and precise if quoting someone mention it clearly
                                                context from meeting transcript:
                                                {context}"""),
                                                ("human","{question}")])
    
    rag_chain=({"context": retriever | RunnableLambda(format_docs),
                "question" : RunnablePassthrough()} | prompt | llm | StrOutputParser())
    
    return rag_chain

def load_rag_chain():
    vector_store = load_vector_store()
    retriever = get_retriever(vector_store)
    llm=get_llm()

    prompt = ChatPromptTemplate.from_messages([("system",""" you are an expert meeting assistant answer the users question based only ont he meeting transcript provided  below
                                                if the answer is not found in the context say i ncould not find the answer in the transcript
                                                
                                                always be concidse and precise if quoting someone mention it clearly
                                                context from meeting transcript:
                                                {context}"""),
                                                ("human"    ,"{question}")])
    
    rag_chain=({"context": retriever | RunnableLambda(format_docs),
                "question" : RunnablePassthrough()} | prompt | llm | StrOutputParser())
    
    return rag_chain 

def ask_question(rag_chain , question:str)->str :
    answer=rag_chain.invoke(question)
    return answer

