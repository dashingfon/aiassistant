import os
from dotenv import load_dotenv,find_dotenv
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain_openai import ChatOpenAI
# from langchain_community import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


load_dotenv(find_dotenv())

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
messages = [
    SystemMessage(content="You are an expert data summarizer"),
    HumanMessage(content="hi"),
]
result = llm.invoke(messages)
print(result)

# response=llm(messages)

# print(response.content, end='\n')


def chat_response():
    ...


if __name__ == "__main__":
    ...