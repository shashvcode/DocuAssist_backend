import re
import docx
import fitz
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from huggingface_hub import InferenceClient
from transformers import pipeline

load_dotenv()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text("text") for page in doc)
    return text.strip()

def extract_text_from_word(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())

def split_text(text, chunk_size=225, chunk_overlap=60):
    if not text.strip():  
        return []

    text = re.sub(r'\s+', ' ', text).strip()  

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  
        chunk_overlap=chunk_overlap,
        separators=["\n\n", ". ", "? ", "! "],  
        keep_separator=True  
    )

    final_chunks = text_splitter.split_text(text)  

    return final_chunks

def generate_summary(extracted_text):
    return summarizer(
        extracted_text,
        min_length=100,
        max_length=350,
        do_sample=False,  
        truncation=True   
    )