from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough , RunnableLambda
import os

def get_llm() :
    return ChatMistralAI(model="mistral-small-latest" , mistral_api_key = os.getenv("MISTRAL_API_KEY"))

def build_chain(system_prompt : str):
    llm=get_llm()
    return (RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | ChatPromptTemplate.from_messages([
        (
            "system" , system_prompt 

        ),
        ("human" , "{text}")
    ]) | llm | StrOutputParser())

def extract_action_items(transcript:str)->str:
    chain=build_chain("You are an expert meeting analyst , from the meeting transcript extract all action items"
                      "for each provide:" \
                      "task description" \
                      "who is responsible" \
                      "fromat as a numbered list , if none found ssay no action items were found"
                      )
    
    return chain.invoke(transcript)

def extract_key_decision(transcript:str)->str:
    chain=build_chain("from the meeting transcript extract key decisions made" \
    "format as a numbered list   if none found say no decisions found" \
                      
                      )
    
    return chain.invoke(transcript)

def extract_questions(transcript:str)->str:
    chain=build_chain("from the meeting transcript extract all unresolved questions" \
    "or topics needing folllow up format as a numbered list" \
    "if none found say no questions found" \
                      
                      )
    
    return chain.invoke(transcript)

 