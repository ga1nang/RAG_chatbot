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
        if self.chatbot_type not in st.session_state:
            self.embeddings = OpenAIEmbeddings()
            data_path = 'store/' + self.chatbot_type
            
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