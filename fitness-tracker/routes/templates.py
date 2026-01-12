"""
Workout template routes: create, read, delete templates
Templates allow users to save and reuse workout plans (e.g., Push Day, Pull Day, Leg Day)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, WorkoutTemplate, TemplateExercise

# Create blueprint
templates_bp = Blueprint("templates", __name__)


# ===== HELPER FUNCTIONS =====


def serialize_template(template):
    """Convert WorkoutTemplate object to JSON-serializable dict"""
    return {
        "id": template.id,
        "name": template.name,
        "created_at": template.created_at.isoformat(),
        "exercises": [
            {
                "id": e.id,
                "name": e.name,
                "sets": e.sets,
                "reps": e.reps,
                "alternatives": e.alternatives,
            }
            for e in template.exercises
        ],
    }


# ===== ROUTES =====


@templates_bp.route("", methods=["POST"])
@jwt_required()
def create_template():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    name = (data.get("name") or "").strip() or "Default Template"
    exercises = data.get("exercises") or []
    if not exercises:
        return jsonify({"error": "At least one exercise required"}), 400

    try:
        template = WorkoutTemplate(user_id=user_id, name=name)
        db.session.add(template)
        db.session.flush()

        for ex in exercises:
            if not ex.get("name") or ex.get("sets") is None:
                db.session.rollback()
                return jsonify({"error": "Each exercise needs: name and sets"}), 400

            exercise = TemplateExercise(
                template_id=template.id,
                name=ex["name"],
                sets=ex["sets"],
                reps=ex.get("reps"),
                alternatives=ex.get("alternatives", ""),
            )
            db.session.add(exercise)

        db.session.commit()
        # return the created template (serialize_template should include id)
        return jsonify(serialize_template(template)), 201

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to create template"}), 500


@templates_bp.route("", methods=["GET"])
@jwt_required()
def get_templates():
    """
    Get all workout templates for current user

    GET /api/templates
    Headers: Authorization: Bearer <token>

    Returns:
    [
        {
            "id": 1,
            "name": "Leg Day",
            "exercises": [...]
        },
        {
            "id": 2,
            "name": "Back Day",
            "exercises": [...]
        }
    ]
    """
    user_id = int(get_jwt_identity())
    templates = WorkoutTemplate.query.filter_by(user_id=user_id).all()
    return jsonify([serialize_template(t) for t in templates]), 200


@templates_bp.route("/<int:template_id>", methods=["GET"])
@jwt_required()
def get_template(template_id):
    """
    Get specific workout template by ID

    GET /api/templates/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "id": 1,
        "name": "Leg Day",
        "exercises": [...]
    }
    """
    user_id = int(get_jwt_identity())
    template = WorkoutTemplate.query.filter_by(id=template_id, user_id=user_id).first()

    if not template:
        return jsonify({"error": "Template not found"}), 404

    return jsonify(serialize_template(template)), 200


@templates_bp.route("/<int:template_id>", methods=["PUT"])
@jwt_required()
def update_template(template_id):
    """
    Update a workout template

    PUT /api/templates/1
    Headers: Authorization: Bearer <token>
    {
        "name": "Leg Day (Updated)",
        "exercises": [...]
    }

    Returns:
    {
        "id": 1,
        "name": "Leg Day (Updated)",
        "exercises": [...]
    }
    """
    user_id = int(get_jwt_identity())
    template = WorkoutTemplate.query.filter_by(id=template_id, user_id=user_id).first()

    if not template:
        return jsonify({"error": "Template not found"}), 404

    data = request.get_json()

    try:
        # Update name if provided
        if "name" in data:
            template.name = data["name"]

        # Update exercises if provided
        if "exercises" in data:
            # Delete old exercises
            TemplateExercise.query.filter_by(template_id=template_id).delete()

            # Add new exercises
            for ex in data.get("exercises", []):
                exercise = TemplateExercise(
                    template_id=template.id,
                    name=ex["name"],
                    sets=ex["sets"],
                    reps=ex["reps"],
                    alternatives=ex.get("alternatives", ""),
                )
                db.session.add(exercise)

        db.session.commit()
        return jsonify(serialize_template(template)), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update template"}), 500


@templates_bp.route("/<int:template_id>", methods=["DELETE"])
@jwt_required()
def delete_template(template_id):
    """
    Delete a workout template

    DELETE /api/templates/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "message": "Template deleted successfully"
    }
    """
    user_id = int(get_jwt_identity())
    template = WorkoutTemplate.query.filter_by(id=template_id, user_id=user_id).first()

    if not template:
        return jsonify({"error": "Template not found"}), 404

    db.session.delete(template)
    db.session.commit()
    return jsonify({"message": "Template deleted successfully"}), 204
