# import sys
# sys.path.append('E:/subject/compulsory_elective_2/real_project')


import streamlit as st 
from src.chat.sessions import SessionManager
from src.chat.embeddings import EmbeddingLoader
from src.base.language_model import LanguageModel


class UIManager:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        
        
    def display_sidebar(self):
        st.sidebar.header('Chat Sessions')
        
        #New chat session
        if st.sidebar.button('New Chat Session'):
            self.session_manager.start_new_chat_message()
            st.sidebar.write('New chat session started!')
            
        session_option = list(st.session_state.chat_sessions.keys())
        if session_option:
            current_session_id = st.sidebar.selectbox(
                'Select a Chat Session', session_option, index=0
            )
            
            self.session_manager.set_current_session_id(current_session_id)
        else:
            st.sidebar.write('No active chat session')
            
        
        #Select type of chatbot
        chatbot = st.sidebar.selectbox(
            "Select a chatbot type",
            ['Credit Papa(Credit scoring)', 'Cooking Mama(Cooking master)']
        )
        chatbot_type = None
        if chatbot == 'Credit Papa(Credit scoring)':
            chatbot_type = 'credit'
        else:
            chatbot_type = 'cooking'
        
        EmbeddingLoader(chatbot_type)
        
        
        #Choose llm model
        engine = st.sidebar.selectbox(
            "Select OpenAI model", ["gpt-4o", "gpt-3.5-turbo"]
        )
        LanguageModel(engine, chatbot_type)
        
        
    def display_chat_messages(self):
        if self.session_manager.get_current_session_id():
            messages = self.session_manager.get_current_messages()
            for msg in messages:
                st.chat_message(msg['role']).write(msg['content'])
                
                
    def on_app_exit(self):
        self.session_manager.save_sessions()