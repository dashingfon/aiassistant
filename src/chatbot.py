import os
import pathlib
from dotenv import load_dotenv,find_dotenv
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import pinecone
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatCohere
from langchain_community.vectorstores import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever


load_dotenv(find_dotenv())
output_parser = StrOutputParser()
embeddings = OpenAIEmbeddings()

# pinecone.init(
#     api_key=os.getenv('PINECONE_API_KEY'),  
#     environment=os.getenv('PINECONE_ENV')  
# )

# llm = ChatOpenAI()
llm = ChatCohere()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert data summarizer"),
    ("user", "what is the size of the earth {input}")
])
chain = prompt | llm | output_parser

result = chain.invoke({"input": "Mr"})
print(result)


def save_document() -> None:
    ...


def chat_response(prompt: str) -> str:
    return ""


if __name__ == "__main__":
    ...