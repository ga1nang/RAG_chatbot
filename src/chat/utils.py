import streamlit as st

class ChatHandler:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        
    
    def handle_user_input(self):
        user_input = st.chat_input(placeholder='What information can you provide?')
        
        if user_input:
            self.session_manager.get_current_messages().append({'role': 'user', 'content': user_input})
            st.chat_message('user').write(user_input)
            
            chat_history = self.session_manager.get_current_messages()
        
            if 'retrieval_chain' in st.session_state:
                with st.chat_message('assistant'):
                    try:
                        response = st.session_state.retrieval_chain.invoke({
                            'input': user_input,
                            'chat_history': chat_history
                        })
                        assitant_response = response['answer'] if isinstance(response, dict) and 'answer' in response else str(response)
                        self.session_manager.get_current_messages().append({'role': 'assistant', 'content': assitant_response})
                        st.write(assitant_response)
                        self.session_manager.set_current_messages(self.session_manager.get_current_messages())
                    except Exception as e:
                        st.error(f'Error generating response: {e}')
                        
            else:
                st.error('Retrieval chain not initialized.')