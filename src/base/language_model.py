import streamlit as st 
from langchain_openai import OpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain


class LanguageModel:
    def __init__(self, engine, chatbot_type):
        self.engine = engine
        self.llm = None
        self.retrieval_chain = None
        self.chatbot_type = chatbot_type
        self.setup_language_model()
        
    
    def setup_language_model(self):
        self.llm = OpenAI(model=self.engine)
        
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
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
        
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        
        if self.chatbot_type in st.session_state:
            if self.chatbot_type == 'credit':
                retriever = st.session_state.credit.as_retriever()
            else:
                retriever = st.session_state.cooking.as_retriver()
                
            #create Q&A chain
            document_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
            
            #create history aware chain
            history_aware_retriever = create_history_aware_retriever(
                self.llm, retriever, self.contextualize_q_prompt
            )
            
            #create retrieval chain
            self.retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)
            st.session_state.retrieval_chain = self.retrieval_chain
            
        else:
            st.write('Vectors not initialized. Please check the FAISS index')