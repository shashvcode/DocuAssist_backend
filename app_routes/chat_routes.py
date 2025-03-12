from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app_utils.chat_utils import classify_prompt, general_document_query, specific_document_query, generate_specific_questions, general_document_questions, general_query

chat = Blueprint("chat", __name__)

@chat.route("/ask/<int:doc_id>", methods = ["POST"])
@jwt_required()
def ask_chat(doc_id):
    user_id = get_jwt_identity()

    data = request.get_json()
    user_query = data["query"]

    if not user_query:
        return jsonify({"error": "Query must be provided"}), 400
    
    response_type = int(classify_prompt(user_query))
    response = ""

    if response_type == 1:
        response = general_document_query(user_id, doc_id, user_query)
    elif response_type == 2:
        response = specific_document_query(user_id, user_query)
    elif response_type == 3:
        response = generate_specific_questions(user_id, user_query)
    elif response_type == 4:
        response = general_document_questions(user_id, doc_id, user_query)
    elif response_type == 5:
        response = general_query(user_query)
    elif response_type == 6:
        response = "Hey there! I am an academic chatbot designed to help you learn! Please refrain from inappropriate or unrelated questions."
    
    return jsonify({"reply": response}), 201





