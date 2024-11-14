import streamlit as st 
import uuid
import json
import os 

class SessionManager:
    def __init__(self):
        self.SESSION_FILE = 'store/chat_sessions.json'
        self.initialize_sessions()
    
    
    def initialize_sessions(self):
        if 'chat_sessions' not in st.session_state:
            st.session_state.chat_sessions = {}
        if 'current_session_id' not in st.session_state:
            st.session_state.current_session_id = None
        
        self.load_sessions()
            
    
    def start_new_chat_message(self):
        session_id = str(uuid.uuid4())
        st.session_state.chat_sessions[session_id] = [
            {'role': 'assistant', 'content': 'Hi, I am a chatbot who can help you. How can I help you?'}
        ]    
        st.session_state.current_session_id = session_id
        self.save_sessions()
        
    
    def get_current_session_id(self):
        return st.session_state.current_session_id
    
    
    def get_current_messages(self):
        if self.get_current_session_id():
            return st.session_state.chat_sessions[self.get_current_session_id()]
        return []
    
    
    def set_current_messages(self, messages):
        if self.get_current_session_id():
            st.session_state.chat_sessions[self.get_current_session_id()] = messages
            self.save_sessions()
            
            
    def set_current_session_id(self, session_id):
        if session_id in st.session_state.chat_sessions:
            st.session_state.current_session_id = session_id
            self.save_sessions()
        else:
            st.write('Selected session does not exist')
            
    
    def load_sessions(self):
        if os.path.exists(self.SESSION_FILE):
            try:
                with open(self.SESSION_FILE, 'r') as f:
                    data = json.load(f)
                st.session_state.chat_sessions = data.get('chat_sessions', {})
                st.session_state.current_session_id = data.get('current_session_id', None)
                st.write('Loaded existing chat sessions.')
            except Exception as e:
                st.error(f"Failed to load chat sessions: {e}")
        else:
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            st.write('No existing chat sessions found. Starting fresh.')


    def save_sessions(self):
        data = {
            'chat_sessions': st.session_state.chat_sessions,
            'current_session_id': st.session_state.current_session_id
        }
        try:
            with open(self.SESSION_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            # Optional: Uncomment the next line for confirmation messages
            # st.write('Chat sessions saved successfully.')
        except Exception as e:
            st.error(f"Failed to save chat sessions: {e}")
