# 📚 DocuAssist.ai - AI-Powered Study Assistant

**DocuAssist.ai** is a **Retrieval-Augmented Generation (RAG)** system that allows users to **upload study materials and interact with them 
conversationally**. By leveraging **state-of-the-art NLP techniques**, the platform extracts, summarizes, and indexes document content for 
**efficient and accurate retrieval**.

---

## 🧠 How It Works

1. **📂 File Upload & Preprocessing**
   - Users upload study materials (`.pdf`, `.docx`, `.txt`).
   - The system extracts text using **PyMuPDF (Fitz) and python-docx**.

2. **🔍 Text Processing & Indexing**
   - Extracted content is **split into semantic chunks** using **LangChain's RecursiveCharacterTextSplitter**.
   - Each chunk is **embedded into a high-dimensional vector space** using `sentence-transformers/multi-qa-mpnet-base-dot-v1`.
   - The **FAISS (Facebook AI Similarity Search) index** efficiently stores and retrieves relevant chunks.

3. **📝 Summarization**
   - A **transformer-based summarization model** (`facebook/bart-large-cnn`) condenses the extracted content to provide quick document insights.

4. **💬 Conversational AI (RAG)**
   - When a user asks a question, the system:
     - Retrieves **the most relevant document chunks** using **FAISS and cosine similarity**.
     - Passes them as context to a **GPT-4-based chatbot** for **grounded and contextually aware responses**.
   - This **RAG pipeline minimizes hallucinations and out of context responses**, ensuring **accurate, document-driven answers**.

---

## ⚙️ Tech Stack

| **Component**            | **Technology Used**                              |
|-------------------------|------------------------------------------------|
| **Backend**             | Flask                                          |
| **Frontend**            | HTML, CSS, JavaScript                          |
| **Database**            | PostgreSQL (for user and file metadata)        |
| **Vector Store**        | FAISS (for efficient document chunk retrieval) |
| **ML Models**           | BART, Sentence-BERT, GPT-4                     |
| **LLM Inference**       | OpenAI API (GPT-4 for conversational responses)|
| **Auth**                | JWT Authentication                             |
                                                                              |
---

## 🚀 Features

✅ **Secure JWT Authentication** - Ensures user data privacy.  
✅ **Multi-Format File Support** - Works with PDFs, DOCX, and TXT files.  
✅ **Fast Semantic Search** - FAISS-powered similarity retrieval.  
✅ **AI-Powered Responses** - GPT-4-based chatbot with RAG pipeline.  
✅ **Summarization & Insights** - Extracts key points from documents.  
✅ **Easy to Use and Simplified UI** - Designed for straightforward user experience.

## **Live Demo**
