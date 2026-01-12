"""
Weight tracking routes: log and track weight progress
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models import db, WeightLog

# Create blueprint
weight_bp = Blueprint("weight", __name__)


# ===== HELPER FUNCTIONS =====


def serialize_weight_log(log):
    """Convert WeightLog object to JSON-serializable dict"""
    return {
        "id": log.id,
        "date": log.date.isoformat(),
        "weight": log.weight,
    }


# ===== ROUTES =====


@weight_bp.route("", methods=["POST"])
@jwt_required()
def log_weight():
    """
    Log weight for a day

    POST /api/weight
    Headers: Authorization: Bearer <token>
    {
        "weight": 185.5
    }

    Returns:
    {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "weight": 185.5
    }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    # Validation
    if "weight" not in data:
        return jsonify({"error": "Weight required"}), 400

    try:
        weight = float(data["weight"])
        if weight <= 0:
            return jsonify({"error": "Weight must be positive"}), 400

    except (ValueError, TypeError):
        return jsonify({"error": "Weight must be a number"}), 400

    # Create weight log
    weight_log = WeightLog(
        user_id=user_id,
        weight=weight,
        date=(
            datetime.fromisoformat(data["date"])
            if data.get("date")
            else datetime.utcnow()
        ),
    )
    db.session.add(weight_log)
    db.session.commit()

    return jsonify(serialize_weight_log(weight_log)), 201


@weight_bp.route("", methods=["GET"])
@jwt_required()
def get_weight():
    """
    Get weight logs for current user

    GET /api/weight?days=90
    Headers: Authorization: Bearer <token>

    Query Parameters:
    - days: number of days to look back (default: 90)

    Returns:
    [
        {
            "id": 1,
            "date": "2024-01-15T10:30:00",
            "weight": 185.5
        },
        ...
    ]
    """
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 90, type=int)
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    logs = (
        WeightLog.query.filter_by(user_id=user_id)
        .filter(WeightLog.date >= cutoff_date)
        .order_by(WeightLog.date.desc())
        .all()
    )

    return jsonify([serialize_weight_log(l) for l in logs]), 200


@weight_bp.route("/<int:log_id>", methods=["GET"])
@jwt_required()
def get_weight_log(log_id):
    """
    Get specific weight log by ID

    GET /api/weight/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "weight": 185.5
    }
    """
    user_id = int(get_jwt_identity())
    log = WeightLog.query.filter_by(id=log_id, user_id=user_id).first()

    if not log:
        return jsonify({"error": "Weight log not found"}), 404

    return jsonify(serialize_weight_log(log)), 200


@weight_bp.route("/<int:log_id>", methods=["PUT"])
@jwt_required()
def update_weight_log(log_id):
    """
    Update a weight log

    PUT /api/weight/1
    Headers: Authorization: Bearer <token>
    {
        "weight": 184.5
    }

    Returns:
    {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "weight": 184.5
    }
    """
    user_id = int(get_jwt_identity())
    log = WeightLog.query.filter_by(id=log_id, user_id=user_id).first()

    if not log:
        return jsonify({"error": "Weight log not found"}), 404

    data = request.get_json()

    try:
        if "weight" in data:
            weight = float(data["weight"])
            if weight <= 0:
                return jsonify({"error": "Weight must be positive"}), 400
            log.weight = weight

        db.session.commit()
        return jsonify(serialize_weight_log(log)), 200

    except (ValueError, TypeError):
        db.session.rollback()
        return jsonify({"error": "Weight must be a valid number"}), 400


@weight_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
def delete_weight_log(log_id):
    """
    Delete a weight log

    DELETE /api/weight/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "message": "Weight log deleted successfully"
    }
    """
    user_id = int(get_jwt_identity())
    log = WeightLog.query.filter_by(id=log_id, user_id=user_id).first()

    if not log:
        return jsonify({"error": "Weight log not found"}), 404

    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Weight log deleted successfully"}), 204
