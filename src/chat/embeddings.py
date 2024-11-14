import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

class EmbeddingLoader:
    def __init__(self, chatbot_type):
        self.chatbot_type = chatbot_type
        self.vectors = None
        self.embeddings = None
        self.load_embeddings()
        
    def load_embeddings(self):
        if self.chatbot_type not in st.session_state:
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings()
            
            # Define the path based on chatbot type
            data_path = os.path.join('store', self.chatbot_type)
            
            # Initialize session state for the specific chatbot type
            if self.chatbot_type == 'credit':
                st.session_state.credit = None
            elif self.chatbot_type == 'cooking':
                st.session_state.cooking = None
            else:
                st.error(f"Unknown chatbot type: {self.chatbot_type}")
                return
            
            # Attempt to load FAISS index
            try:
                self.vectors = FAISS.load_local(
                    data_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                
                # Update session state with loaded vectors
                if self.chatbot_type == 'credit':
                    st.session_state.credit = self.vectors
                elif self.chatbot_type == 'cooking':
                    st.session_state.cooking = self.vectors
                    
                st.success(f"FAISS index for {self.chatbot_type} loaded successfully.")
                    
            except Exception as e:
                st.error(f"Failed to load FAISS index: {e}")
