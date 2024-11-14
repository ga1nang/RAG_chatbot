import streamlit as st 
import uuid

class SessionManager:
    def __init__(self):
        self.initialize_sessions()
    
    
    def initialize_sessions(self):
        if 'chat_sessions' not in st.session_state:
            st.session_state.chat_sessions = {}
        if 'current_session_id' not in st.session_state:
            st.session_state.current_session_id = None
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
    
    def start_new_chat_message(self):
        session_id = str(uuid.uuid4())
        st.session_state.chat_history[session_id] = [
            {'role': 'assistant', 'content': 'Hi, I am a chatbot who can help you. How can I help you?'}
        ]    
        st.session_state.current_session_id = session_id
        
    
    def get_current_session_id(self):
        return st.session_state.current_session_id
    
    
    def get_current_messages(self):
        if self.get_current_session_id():
            return st.session_state.chat_history[self.get_current_session_id()]
        return []
    
    
    def set_current_messages(self, messages):
        if self.get_current_session_id():
            st.session_state.chat_history[self.get_current_session_id()] = messages
            