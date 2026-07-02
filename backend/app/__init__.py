from flask import Flask
from config import Config
from dotenv import load_dotenv
from .extensions import db, jwt, migrate, bcrypt
from .auth.routes import auth_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from .customers.routes import customers_bp
from .payments.routes import payments_bp

# Load environment variables from .env
load_dotenv()

def create_app():
    Config.require_core_vars()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(payments_bp)

    from . import models

    @app.route("/")
    def home():
        return {"message": "TechOps Insight API is running 🚀"}

    @app.route("/protected")
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        return {
            "message": "Access granted",
            "user_id": current_user_id
        }

    return app