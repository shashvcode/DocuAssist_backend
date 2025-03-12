import openai
import os
from models import UploadedFile
from dotenv import load_dotenv
from app_utils.faiss_utils import retrieve_relevant_chunks

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_prompt(user_message):
    system_prompt = f"""
        You are a powerful classification bot whose job is to classify the user's message into one of these three categories:

        1. The user is requesting a comprehensive summary or questions covering the entire document.,
        2. The user is asking about a specific section, topic, or detail within the document.,
        3. The user is asking for some questions from a specific section, topic, or part of the document.,
        4. The user is asking for some question from the entire document.,
        5  The user's query is simply conversational and not related to anything academic.
        6. The user's query is inapropriate or nonsensical.

        Return only the number associated with the category(eg. 1, 2, or 3)
                """

    response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=150
                )

    ai_output = response.choices[0].message.content.strip()
    return ai_output

def general_query(user_message):
    system_prompt = f"""
        You are an academic chatbot who has been extensively trained on responding to academic queries. 
        
        - The user's is just trying to talk regularly outside of an academic context: {user_message}
        - Your job is to briefly reply to them while gently reminding them that you are an academic chatbot whose purpose it to help learn, not have conversation.
                """

    response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=500
                )

    ai_output = response.choices[0].message.content.strip()
    return ai_output

def general_document_query(user_id, doc_id, user_message):

    document = UploadedFile.query.filter_by(id=doc_id, user_id=user_id).first()
    summary = document.text_summary

    system_prompt = f"""
        You are an academic chatbot who has been extensively trained on responding to academic queries. 
        
        Based on the user's message and this document summary {summary}, respond to their query in an informative yet VERY friendly manner.

        Your answer should articulate complete and intelligent thought that is very easy to understand in no more than 200 tokens
                """

    response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=500
                )

    ai_output = response.choices[0].message.content.strip()
    return ai_output

def general_document_questions(user_id, doc_id, user_message):

    document = UploadedFile.query.filter_by(id=doc_id, user_id=user_id).first()
    summary = document.text_summary

    system_prompt = f"""
        You are an expert academic question generator, capable of creating thought-provoking, well-structured questions based on a document summary.
        
        Below is the summary of the document:
        {summary}

        Using only the information within this summary, generate a list of **high-quality, engaging questions** that match the **tone, style, and subject matter** of the document. 

        The questions should be:
        - **Contextually accurate** (based only on the provided summary)
        - **Cater to the user's query** (e.g., If the user asks for MCQs, short-response, or long-form questions, adjust accordingly. If none specified, return a mix of these three.)
        - **Clear & well-structured** (easy to understand)
        - **Appropriate in tone** (matching the style of the document)

        Return the user's requested number of questions in a numbered list. If no number is specified, return 3-4 varying questions.
        """ 

    response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=500
                )

    ai_output = response.choices[0].message.content.strip()
    return ai_output

def specific_document_query(user_id, user_message):
    
    nearest_neighbors = retrieve_relevant_chunks(user_id, user_message, top_k=3)

    system_prompt = f"""
        You are an academic assistant specializing in answering specific, detail-oriented questions based on document content. 
        
        The user has asked a question related to the following retrieved document excerpts:
        {nearest_neighbors}

        Using only the relevant information from these excerpts, provide a precise, well-structured response that directly addresses the user's question. 
        Your answer should be concise, clear, and written in an approachable, VERY friendly tone while ensuring accuracy in no more than 200 tokens
                """

    response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=500
                )

    ai_output = response.choices[0].message.content.strip()
    return ai_output

def generate_specific_questions(user_id, user_message):
    
    nearest_neighbors = retrieve_relevant_chunks(user_id, user_message, top_k = 5)

    system_prompt = f"""
        You are an expert academic question generator, capable of creating thought-provoking, well-structured questions based on specific document excerpts.
        
        Below are the most relevant excerpts retrieved from the document:
        {nearest_neighbors}

        Using only the information within these excerpts, generate a list of **high-quality, engaging questions** that match the **tone, style, and subject matter** of the document. 

        The questions should be:
        - **Contextually accurate** (based only on the provided excerpts)
        - **Cater to the user's query** (eg. If user asks for MCQ, or short response, or long form. If none specified, return a mix of these three)
        - **Clear & well-structured** (easy to understand)
        - **Appropriate in tone** (matching the style of the document)

        Return the user's requested number of questions in a numbered list. If no number is specified, return 3-4 varying questions.
        """

    response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=500
                )

    ai_output = response.choices[0].message.content.strip()
    return ai_output
