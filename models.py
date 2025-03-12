from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
class UploadedFile(db.Model):
    __tablename__ = "uploaded_files"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)  
    upload_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    text_summary = db.Column(db.Text, nullable=True)  

    user = db.relationship('User', backref=db.backref('files', lazy=True, cascade="all, delete-orphan"))

class DocumentChunk(db.Model):
    __tablename__ = "document_chunks"

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('uploaded_files.id', ondelete="CASCADE"), nullable=False)
    chunk_index = db.Column(db.Integer, nullable=False)
    chunk_text = db.Column(db.Text, nullable=False) 
    embedding = db.Column(db.ARRAY(db.Float), nullable=True) 
    
    file = db.relationship('UploadedFile', backref=db.backref('chunks', lazy=True, cascade="all, delete-orphan"))

