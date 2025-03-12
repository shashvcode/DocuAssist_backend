import os
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app_utils.file_utils import extract_text_from_pdf, extract_text_from_word, split_text, generate_summary
from app_utils.embedding_utils import generate_embedding 
from app_utils.faiss_utils import store_in_faiss
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, UploadedFile, DocumentChunk

uploads = Blueprint("uploads", __name__)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"pdf", "docx", "txt"}

@uploads.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():

    user_id = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    filename = secure_filename(file.filename)
    file_extension = filename.rsplit(".", 1)[1].lower()
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads") 
    os.makedirs(upload_folder, exist_ok=True) 
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    extracted_text = ""
    if file_extension == "pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_extension == "docx":
        extracted_text = extract_text_from_word(file_path)
    elif file_extension == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            extracted_text = f.read()

    if not extracted_text.strip():
        return jsonify({"error": "No text found in document"}), 400
    
    summary = generate_summary(extracted_text)

    new_file = UploadedFile(
        user_id=user_id,
        filename=filename,
        file_type=file_extension,
        extracted_text=extracted_text,
        text_summary = json.dumps(summary)  
    )
    db.session.add(new_file)
    db.session.commit()

    chunks = split_text(extracted_text)
    chunk_objects = []
    chunk_texts = []

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)
        if embedding is not None:
            chunk_objects.append(DocumentChunk(file_id=new_file.id, chunk_index=index, chunk_text=chunk, embedding=embedding.tolist()))
            chunk_texts.append(chunk)  

    db.session.bulk_save_objects(chunk_objects)
    db.session.commit()

    store_in_faiss(user_id, chunk_texts)

    return jsonify({
        "filename": filename, 
        "file_id": new_file.id, 
        "message": "File uploaded, chunked, embedded, and stored successfully!"
    }), 201


@uploads.route("/document/<int:doc_id>", methods=["GET"])
@jwt_required()
def get_document(doc_id):
    user_id = get_jwt_identity()

    document = UploadedFile.query.filter_by(id=doc_id, user_id=user_id).first()

    if not document:
        return jsonify({"error": "Document not found or access denied"}), 404

    chunks = DocumentChunk.query.filter_by(file_id=doc_id).order_by(DocumentChunk.chunk_index).all()

    chunk_texts = [chunk.chunk_text for chunk in chunks]

    return jsonify({
        "doc_id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "upload_date": document.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
        "total_chunks": len(chunk_texts),
        "chunks": chunk_texts  
    }), 200