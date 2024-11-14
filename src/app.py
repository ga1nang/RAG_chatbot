import sys
sys.path.append('E:/subject/compulsory_elective_2/real_project')

import streamlit as st
import atexit
from src.chat.config import Config
from src.chat.sessions import SessionManager
from src.chat.ui import UIManager
from src.chat.utils import ChatHandler

def main():
    config = Config()
    st.title("Ga1nang")

    # Initialize session manager
    session_manager = SessionManager()

    # Initialize UI manager
    ui_manager = UIManager(session_manager)
    ui_manager.display_sidebar()

    # Display chat messages
    ui_manager.display_chat_messages()

    # Handle user input and generate responses
    chat_handler = ChatHandler(session_manager)
    chat_handler.handle_user_input()
    
    # Save session state when the app is closed
    def save_session_state():
        session_manager.save_sessions()
    atexit.register(save_session_state)

if __name__ == "__main__":
    main()