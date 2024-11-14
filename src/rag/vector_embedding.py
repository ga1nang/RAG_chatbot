import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from tempfile import TemporaryDirectory
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

st.title('Update the vector store')
st.write('Upload your pdf')

# Set up the temp directory
temp_dir = "RAG_Q&A_Conversation"
os.makedirs(temp_dir, exist_ok=True)

# Track chatbot_type with session state
if 'previous_chatbot_type' not in st.session_state:
    st.session_state.previous_chatbot_type = None

# Select chatbot type and track any change
chatbot_type = st.sidebar.selectbox('Select a chatbot type to load data', ['credit', 'cooking'])
if chatbot_type != st.session_state.previous_chatbot_type:
    st.session_state.previous_chatbot_type = chatbot_type
    st.session_state.vector_store_loaded = False  # Flag to reload the vector store

# Process uploaded PDF
uploaded_files = st.file_uploader("Choose a PDF file", type='pdf', accept_multiple_files=True)
start = st.button('Generate Embedding')

if start:
    with st.spinner('Generating Embedding....'):
        # Load data
        documents = []
        with TemporaryDirectory() as temp_dir:
            for uploaded_file in uploaded_files:
                temp_pdf = os.path.join(temp_dir, f"temp_{uploaded_file.name}")
                with open(temp_pdf, 'wb') as file:
                    file.write(uploaded_file.getvalue())
                
                # Load the PDF file and save to documents
                loader = PyPDFLoader(temp_pdf)
                docs = loader.load()
                documents.extend(docs)

        # Split and create embeddings for the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)

        # Load or create the vector store
        vector_store_path = 'store/' + chatbot_type
        try:
            if not st.session_state.vector_store_loaded:
                vector_store = FAISS.load_local(vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)
                st.session_state.vector_store_loaded = True  # Flag as loaded
            vector_store.add_documents(splits, embeddings=embeddings)

        except (FileNotFoundError, RuntimeError) as e:
            if "could not open" in str(e) or "No such file or directory" in str(e):
                st.warning("No existing vector store found. A new vector store will be created.")
                vector_store = FAISS.from_documents(documents=splits, embedding=embeddings)
            else:
                raise e

        # Save the updated vector store
        vector_store.save_local(vector_store_path)
        st.success("Vector store updated and saved successfully.")

st.success("Vector store updated and saved successfully.")


