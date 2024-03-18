import os
import pathlib
from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.chat_models import ChatCohere
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever


PATH = r"media\Indie Bites 9 PDF.pdf"
load_dotenv(find_dotenv())
output_parser = StrOutputParser()
embeddings = CohereEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(separators=[".", ","])
loader = PyPDFLoader(PATH)
doc = loader.load()
docs = text_splitter.split_documents(doc)
index = FAISS.from_documents(docs, embeddings)


llm = ChatCohere()
prompt = ChatPromptTemplate.from_template(
    """
    You are an ai assistant, answer the following question based on the context.
    The context is an interview, answer the question based on the reply the interviewee gave.
    use the context where relevant

    <context>
    {context}
    </context>

    Question: {input}
    """
)

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = index.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)


def chat_response(prompt: str) -> str:
    result = retrieval_chain.invoke({"input": prompt})
    print(result["answer"])
    return result["answer"]


if __name__ == "__main__":
    chat_response("whats in store for your readers next?")
    # save_pdf_document(r"media\Indie Bites 9 PDF.pdf")