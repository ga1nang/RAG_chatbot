import os
import streamlit as st 
from dotenv import load_dotenv


class Config:
    def __init__(self, env_path='.env'):
        self.env_path = env_path
        self.load_config()
        
    
    def load_config(self):
        load_dotenv(self.env_path)
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        
        
def main():
    config = Config()
    
    
if __name__ == '__main__':
    main()
    print('success')