"""
Nutrition routes: log and track macros (protein, carbs, fats, calories)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models import db, NutritionLog

# Create blueprint
nutrition_bp = Blueprint("nutrition", __name__)


# ===== HELPER FUNCTIONS =====


def serialize_nutrition_log(log):
    """Convert NutritionLog object to JSON-serializable dict"""
    return {
        "id": log.id,
        "date": log.date.isoformat(),
        "protein": log.protein,
        "carbs": log.carbs,
        "fats": log.fats,
        "calories": log.calories,
    }


# ===== ROUTES =====


@nutrition_bp.route("", methods=["POST"])
@jwt_required()
def log_nutrition():
    """
    Log nutrition/macros for a day

    POST /api/nutrition
    Headers: Authorization: Bearer <token>
    {
        "protein": 150,
        "carbs": 200,
        "fats": 70,
        "calories": 2100
    }

    Returns:
    {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "protein": 150,
        "carbs": 200,
        "fats": 70,
        "calories": 2100
    }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    # Validation
    required_fields = ["protein", "carbs", "fats", "calories"]
    if not all(field in data for field in required_fields):
        return (
            jsonify(
                {"error": f"Missing required fields: {', '.join(required_fields)}"}
            ),
            400,
        )

    # Validate numeric values
    try:
        protein = float(data["protein"])
        carbs = float(data["carbs"])
        fats = float(data["fats"])
        calories = float(data["calories"])

        if any(v < 0 for v in [protein, carbs, fats, calories]):
            return jsonify({"error": "Values must be non-negative"}), 400

    except (ValueError, TypeError):
        return jsonify({"error": "All fields must be numeric"}), 400

    # Create nutrition log
    nutrition_log = NutritionLog(
        user_id=user_id,
        protein=protein,
        carbs=carbs,
        fats=fats,
        calories=calories,
        date=(
            datetime.fromisoformat(data["date"])
            if data.get("date")
            else datetime.utcnow()
        ),
    )
    db.session.add(nutrition_log)
    db.session.commit()

    return jsonify(serialize_nutrition_log(nutrition_log)), 201


@nutrition_bp.route("", methods=["GET"])
@jwt_required()
def get_nutrition():
    """
    Get nutrition logs for current user

    GET /api/nutrition?days=30
    Headers: Authorization: Bearer <token>

    Query Parameters:
    - days: number of days to look back (default: 30)

    Returns:
    [
        {
            "id": 1,
            "date": "2024-01-15T10:30:00",
            "protein": 150,
            "carbs": 200,
            "fats": 70,
            "calories": 2100
        },
        ...
    ]
    """
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 30, type=int)
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    logs = (
        NutritionLog.query.filter_by(user_id=user_id)
        .filter(NutritionLog.date >= cutoff_date)
        .order_by(NutritionLog.date.desc())
        .all()
    )

    return jsonify([serialize_nutrition_log(l) for l in logs]), 200


@nutrition_bp.route("/<int:log_id>", methods=["GET"])
@jwt_required()
def get_nutrition_log(log_id):
    """
    Get specific nutrition log by ID

    GET /api/nutrition/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "protein": 150,
        "carbs": 200,
        "fats": 70,
        "calories": 2100
    }
    """
    user_id = int(get_jwt_identity())
    log = NutritionLog.query.filter_by(id=log_id, user_id=user_id).first()

    if not log:
        return jsonify({"error": "Nutrition log not found"}), 404

    return jsonify(serialize_nutrition_log(log)), 200


@nutrition_bp.route("/<int:log_id>", methods=["PUT"])
@jwt_required()
def update_nutrition_log(log_id):
    """
    Update a nutrition log

    PUT /api/nutrition/1
    Headers: Authorization: Bearer <token>
    {
        "protein": 160,
        "carbs": 210,
        "fats": 75,
        "calories": 2150
    }

    Returns:
    {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "protein": 160,
        "carbs": 210,
        "fats": 75,
        "calories": 2150
    }
    """
    user_id = int(get_jwt_identity())
    log = NutritionLog.query.filter_by(id=log_id, user_id=user_id).first()

    if not log:
        return jsonify({"error": "Nutrition log not found"}), 404

    data = request.get_json()

    try:
        # Update fields if provided
        if "protein" in data:
            log.protein = float(data["protein"])
        if "carbs" in data:
            log.carbs = float(data["carbs"])
        if "fats" in data:
            log.fats = float(data["fats"])
        if "calories" in data:
            log.calories = float(data["calories"])

        db.session.commit()
        return jsonify(serialize_nutrition_log(log)), 200

    except (ValueError, TypeError):
        db.session.rollback()
        return jsonify({"error": "Invalid numeric values"}), 400


@nutrition_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
def delete_nutrition_log(log_id):
    """
    Delete a nutrition log

    DELETE /api/nutrition/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "message": "Nutrition log deleted successfully"
    }
    """
    user_id = int(get_jwt_identity())
    log = NutritionLog.query.filter_by(id=log_id, user_id=user_id).first()

    if not log:
        return jsonify({"error": "Nutrition log not found"}), 404

    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Nutrition log deleted successfully"}), 204
