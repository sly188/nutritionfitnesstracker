"""
Authentication routes: register, login, logout
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user account

    POST /api/auth/register
    {
        "username":
        "email":
        "password":
    }

    Returns:
    {
        "access_token":
        "user_id":
    }
    """
    data = request.get_json()

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return (
            jsonify({"error": "Missing required fields: username, email, password"}),
            400,
        )

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
    )
    db.session.add(user)
    db.session.commit()

    # MAKE STRING
    access_token = create_access_token(identity=str(user.id))
    return (
        jsonify(
            {
                "message": "User registered successfully",
                "access_token": access_token,
                "user_id": user.id,
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login with username and password

    POST /api/auth/login
    {
        "username": ,
        "password":
    }
    Returns:
    {
        "access_token":
        "user_id":
    }
    """
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return (
        jsonify(
            {
                "message": "Login successful",
                "access_token": access_token,
                "user_id": user.id,
            }
        ),
        200,
    )


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout user (invalidate token on frontend)

    POST /api/auth/logout
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "message": "Logged out successfully"
    }
    """
    return jsonify({"message": "Logged out successfully"}), 200
