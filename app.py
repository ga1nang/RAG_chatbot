import streamlit as st
import os

from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()


#set up streamlit
st.title('Conversational RAG which can help you understanding more about credit score')

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()


#input the Groq API key
api_key = st.text_input('Enter your Groq API key:', type='password')


#Check if groq api key is provided
if api_key:
    llm = ChatGroq(model_name="Gemma2-9b-It", groq_api_key=api_key)