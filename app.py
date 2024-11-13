import streamlit as st
import os
import uuid
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_community.vectorstores import FAISS

load_dotenv()

# Load the API keys
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


# Start a new chat session with a welcome message
def start_new_chat_session():
    session_id = str(uuid.uuid4())
    st.session_state.chat_sessions[session_id] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can help you. How can I help you?"}
    ]
    st.session_state.current_session_id = session_id


# Embedding vector based on chatbot type
def load_vector_embeddings(chatbot_type):
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OpenAIEmbeddings()
        data_path = 'store/' + ('credit' if chatbot_type == 'Credit Papa(Credit scoring)' else 'cooking')
        
        # Load FAISS vectors
        try:
            st.session_state.vectors = FAISS.load_local(
                data_path,
                st.session_state.embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            st.error(f"Failed to load FAISS index: {e}")

# Set up the language model and retrieval chain
def setup_language_model(engine):
    llm = ChatOpenAI(model=engine)
    
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    if "vectors" in st.session_state:
        #create retriever
        retriever = st.session_state.vectors.as_retriever()
        
        #create Q&A chain
        document_chain = create_stuff_documents_chain(llm, qa_prompt)

        #create history aware chain
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )
        
        
        
        st.session_state.retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)
    else:
        st.write("Vectors not initialized. Please check the FAISS index.")




# Initialize sessions in session state if not already done
def initialize_sessions():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
        
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None
        
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
        
# Set up the sidebar with chatbot options
def display_sidebar():
    st.sidebar.header("Chat Sessions")

    if st.sidebar.button("New Chat Session"):
        start_new_chat_session()
        st.sidebar.write("New chat session started!")

    session_options = list(st.session_state.chat_sessions.keys())
    current_session_id = st.sidebar.selectbox("Select a Chat Session", session_options, index=0 if session_options else -1)
    if current_session_id:
        st.session_state.current_session_id = current_session_id

    chatbot_type = st.sidebar.selectbox("Select a chatbot type", ['Credit Papa(Credit scoring)', 'Cooking Mama(Cooking master)'])
    load_vector_embeddings(chatbot_type)

    engine = st.sidebar.selectbox("Select Open AI model", ["gpt-4o", "gpt-3.5-turbo-1106"])
    setup_language_model(engine)


# Display messages for the selected session
def display_chat_messages():
    if st.session_state.current_session_id:
        st.session_state.messages = st.session_state.chat_sessions[st.session_state.current_session_id]
        for msg in st.session_state.messages:
            st.chat_message(msg['role']).write(msg['content'])


# Handle new user input and generate a response
def handle_user_input():
    if user_input := st.chat_input(placeholder="What is risk management?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        historical_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

        if "retrieval_chain" in st.session_state:
            with st.chat_message("assistant"):
                try:
                    response = st.session_state.retrieval_chain.invoke({'context': historical_context, 'input': user_input})
                    assistant_response = response['answer'] if isinstance(response, dict) and 'answer' in response else str(response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    st.write(assistant_response)
                    st.session_state.chat_sessions[st.session_state.current_session_id] = st.session_state.messages
                except Exception as e:
                    st.error(f"Error generating response: {e}")
        else:
            st.error("Retrieval chain not initialized.")


# Main application logic
def main():
    st.title("Ga1nang")

    # Initialize sessions and display sidebar
    initialize_sessions()
    display_sidebar()

    # Display chat messages and handle new user input
    display_chat_messages()
    handle_user_input()

if __name__ == "__main__":
    main()
