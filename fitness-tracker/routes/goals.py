"""
Goals routes: create, read, update, delete fitness goals
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Goal

# Create blueprint
goals_bp = Blueprint("goals", __name__)


# ===== HELPER FUNCTIONS =====


def serialize_goal(goal):
    """Convert Goal object to JSON-serializable dict"""
    return {
        "id": goal.id,
        "goal_type": goal.goal_type,
        "target_value": goal.target_value,
        "current_value": goal.current_value,
        "period": goal.period,
        "completed": goal.completed,
        "created_at": goal.created_at.isoformat(),
    }


# ===== ROUTES =====


@goals_bp.route("", methods=["POST"])
@jwt_required()
def create_goal():
    """
    Create a new fitness goal

    POST /api/goals
    Headers: Authorization: Bearer <token>
    {
        "goal_type": "weight",  # 'weight', 'calories', 'workout_count'
        "target_value":
        "period": "month"       # 'month' or 'year'
    }

    Returns:
    {
        "id":
        "goal_type":
        "target_value":
        "current_value":
        "period":
        "completed":
        "created_at":
    }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    # Validation
    required_fields = ["goal_type", "target_value", "period"]
    if not all(field in data for field in required_fields):
        return (
            jsonify(
                {"error": f"Missing required fields: {', '.join(required_fields)}"}
            ),
            400,
        )

    valid_goal_types = ["weight", "calories", "workout_count"]
    if data["goal_type"] not in valid_goal_types:
        return (
            jsonify(
                {"error": f"goal_type must be one of: {', '.join(valid_goal_types)}"}
            ),
            400,
        )

    valid_periods = ["month", "year"]
    if data["period"] not in valid_periods:
        return jsonify({"error": f"period must be 'month' or 'year'"}), 400
    try:
        target_value = float(data["target_value"])
        if target_value <= 0:
            return jsonify({"error": "target_value must be positive"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "target_value must be a number"}), 400

    goal = Goal(
        user_id=user_id,
        goal_type=data["goal_type"],
        target_value=target_value,
        period=data["period"],
    )
    db.session.add(goal)
    db.session.commit()

    return jsonify(serialize_goal(goal)), 201


@goals_bp.route("", methods=["GET"])
@jwt_required()
def get_goals():
    """
    Get all fitness goals for current user

    GET /api/goals
    Headers: Authorization: Bearer <token>

    Query Parameters:
    - completed: filter by completion status (true/false)

    Returns:
    [
        {
            "id":
            "goal_type":
            "target_value":
            "current_value":
            "period":
            "completed":
            "created_at":
        },
        ...
    ]
    """
    user_id = int(get_jwt_identity())
    query = Goal.query.filter_by(user_id=user_id)

    completed = request.args.get("completed", None)
    if completed is not None:
        completed = completed.lower() == "true"
        query = query.filter_by(completed=completed)

    goals = query.all()
    return jsonify([serialize_goal(g) for g in goals]), 200


@goals_bp.route("/<int:goal_id>", methods=["GET"])
@jwt_required()
def get_goal(goal_id):
    """
    Get specific goal by ID

    GET /api/goals/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "id":
        "goal_type":
        "target_value":
        "current_value":
        "period":
        "completed":
        "created_at":
    }
    """
    user_id = int(get_jwt_identity())
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()

    if not goal:
        return jsonify({"error": "Goal not found"}), 404

    return jsonify(serialize_goal(goal)), 200


@goals_bp.route("/<int:goal_id>", methods=["PUT"])
@jwt_required()
def update_goal(goal_id):
    """
    Update a goal (update progress or mark as complete)

    PUT /api/goals/1
    Headers: Authorization: Bearer <token>
    {
        "current_value":
        "completed":
    }

    Returns:
    {
        "id":
        "goal_type":
        "target_value":
        "current_value":
        "period":
        "completed":
        "created_at":
    }
    """
    user_id = int(get_jwt_identity())
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()

    if not goal:
        return jsonify({"error": "Goal not found"}), 404

    data = request.get_json()

    try:

        if "current_value" in data:
            goal.current_value = float(data["current_value"])

        if "completed" in data:
            goal.completed = bool(data["completed"])

        db.session.commit()
        return jsonify(serialize_goal(goal)), 200

    except (ValueError, TypeError):
        db.session.rollback()
        return jsonify({"error": "Invalid data format"}), 400


@goals_bp.route("/<int:goal_id>", methods=["DELETE"])
@jwt_required()
def delete_goal(goal_id):
    """
    Delete a goal

    DELETE /api/goals/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "message": "Goal deleted successfully"
    }
    """
    user_id = int(get_jwt_identity())
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()

    if not goal:
        return jsonify({"error": "Goal not found"}), 404

    db.session.delete(goal)
    db.session.commit()
    return jsonify({"message": "Goal deleted successfully"}), 204
