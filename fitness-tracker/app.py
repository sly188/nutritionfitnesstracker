"""
app.py
Main flask app (backend)
Purpose: Initializes app, database, health check,
error handling, and registering blueprints.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from models import db
from routes.auth import auth_bp
from routes.workouts import workouts_bp
from routes.nutrition import nutrition_bp
from routes.weight import weight_bp
from routes.goals import goals_bp
from routes.templates import templates_bp

load_dotenv()


def create_app():
    """Application factory - creates and configures Flask app"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///fitness.db"
    )
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:3000"}},
        supports_credentials=True,
    )

    @app.before_request
    def log_request_info():
        if request.endpoint not in ["health", "static"]:
            print(f"\n=== {request.method} {request.path} ===")
            auth_header = request.headers.get("Authorization")

            if auth_header and request.method != "OPTIONS":
                print(f"Authorization header present")
                try:
                    token = auth_header.replace("Bearer ", "")
                    from flask_jwt_extended import decode_token

                    decoded = decode_token(token, allow_expired=True)
                    print(f"Decoded token claims: {decoded}")
                    print(
                        f"Identity (sub): {decoded.get('sub')}, Type: {type(decoded.get('sub'))}"
                    )
                except Exception as e:
                    print(f"Error decoding token (non-fatal): {e}")

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(workouts_bp, url_prefix="/api/workouts")
    app.register_blueprint(templates_bp, url_prefix="/api/templates")
    app.register_blueprint(nutrition_bp, url_prefix="/api/nutrition")
    app.register_blueprint(weight_bp, url_prefix="/api/weight")
    app.register_blueprint(goals_bp, url_prefix="/api/goals")

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint"""
        return {"status": "Good", "service": "fitness-tracker-api"}, 200

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad request"}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {"error": "Unauthorized"}, 401

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"error": "Internal server error"}, 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
