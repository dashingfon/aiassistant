from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.chat_models import ChatCohere
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


load_dotenv(find_dotenv())


class ChatBot:

    def __init__(self, reference_path: str) -> None:
        self.path = reference_path
        self.output_parser = StrOutputParser()
        self.embeddings = CohereEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(separators=[".", ","])
        self.loader = PyPDFLoader(self.path)
        doc = self.loader.load()
        docs = self.text_splitter.split_documents(doc)
        self.vector = FAISS.from_documents(docs, self.embeddings)
        self.llm = ChatCohere()
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an eloquent english speaker and writer, answer the question as accurately as possible,
            using the context only when the question is not well understood. When using the context,
            include only information from the context.

            <context>
            {context}
            </context>

            Question: {input}
            """
        )
        document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        retriever = self.vector.as_retriever()
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)

    def respond(self, message: str) -> str:
        result = self.retrieval_chain.invoke({"input": message})
        return result["answer"]



if __name__ == "__main__":
    chat_bot = ChatBot(r"media\Indie Bites 9 PDF.pdf")
    print(chat_bot.respond("how are you?"))
