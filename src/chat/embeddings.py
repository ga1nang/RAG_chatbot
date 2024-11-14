import streamlit as st 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


class EmbeddingLoader:
    def __init__(self, chatbot_type):
        self.chatbot_type = chatbot_type
        self.vectors = None
        self.embeddings = None
        self.load_embeddings()
        
    
    def load_embeddings(self):
        data_path = f'{"credit" if self.chatbot_type == "Credit Papa(Credit scoring)" else "cooking"}'
        if data_path not in st.session_state:
            self.embeddings = OpenAIEmbeddings()
            data_path = 'store/' + data_path
            
            if data_path == 'credit':
                st.session_state.credit = None
            else:
                st.session_state.cooking = None
            
            #load faiss
            try:
                self.vectors = FAISS.load_local(
                    data_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                if data_path == 'credit':
                    st.session_state.credit = self.vectors
                else:
                    st.session_state.cooking = self.vectors
                    
            except Exception as e:
                st.error('Failed to load FAISS index: {e}')