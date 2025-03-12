from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager 
from flask_migrate import Migrate
from datetime import timedelta
from app_routes.auth_routes import auth
from app_routes.upload_routes import uploads
from app_routes.chat_routes import chat
from dotenv import load_dotenv
from models import db
import os

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days = 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
jwt = JWTManager(app)
CORS(app)  
migrate = Migrate(app, db) 

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(uploads, url_prefix="/uploads")
app.register_blueprint(chat, url_prefix="/chat")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)