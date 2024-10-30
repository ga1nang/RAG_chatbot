from typing import Union, List, Literal
import glob
from tqdm import tqdm
import multiprocessing
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def remove_non_utf8_characters(text):
    return ''.join(char for char in text if ord(char) < 128)


def load_pdf(pdf_file):
    docs = PyPDFLoader(pdf_file, extract_images=True).load()
    for doc in docs:
        doc.page_content = remove_non_utf8_characters(doc.page_content)
    return docs


def load_html(html_file):
    docs = BSHTMLLoader(html_file).load()
    for doc in docs:
        doc.page_content = remove_non_utf8_characters(doc.page_content)
    return docs


def get_num_cpu():
    return multiprocessing.cpu_count()







