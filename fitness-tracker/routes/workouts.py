"""
Workout routes: create, read, update, delete workouts
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models import db, Workout, WorkoutExercise, WorkoutSet

workouts_bp = Blueprint("workouts", __name__)


def serialize_workout(workout):
    """Convert Workout object to JSON-serializable dict"""
    return {
        "id": workout.id,
        "date": workout.date.isoformat(),
        "template_id": workout.template_id,
        "exercises": [
            {
                "id": e.id,
                "name": e.name,
                "sets": [
                    {
                        "id": s.id,
                        "set_number": s.set_number,
                        "reps": s.reps,
                        "weight": s.weight,
                    }
                    for s in e.sets
                ],
            }
            for e in workout.exercises
        ],
    }


@workouts_bp.route("", methods=["POST"])
@jwt_required()
def log_workout():
    """
    Log a new workout

    POST /api/workouts
    Headers: Authorization: Bearer <token>
    {
        "template_id": 1,  # optional
        "exercises": [
            {
                "name": "",
                "sets": [
                    {"set_number":  "reps": "weight": },
                ]
            },
        ]
    }

    Returns:
    {
        "id": 1,
        "message": "Workout logged successfully"
    }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get("exercises"):
        return jsonify({"error": "Exercises required"}), 400

    try:
        workout = Workout(
            user_id=user_id,
            template_id=data.get("template_id"),
            date=(
                datetime.fromisoformat(data["date"])
                if data.get("date")
                else datetime.utcnow()
            ),
        )
        db.session.add(workout)
        db.session.flush()

        for ex in data.get("exercises", []):
            if not ex.get("name") or not ex.get("sets"):
                db.session.rollback()
                return jsonify({"error": "Each exercise needs name and sets"}), 400

            exercise = WorkoutExercise(workout_id=workout.id, name=ex["name"])
            db.session.add(exercise)
            db.session.flush()

            for set_data in ex.get("sets", []):
                if not all(k in set_data for k in ["set_number", "reps", "weight"]):
                    db.session.rollback()
                    return (
                        jsonify({"error": "Each set needs set_number, reps, weight"}),
                        400,
                    )

                workout_set = WorkoutSet(
                    exercise_id=exercise.id,
                    reps=set_data["reps"],
                    weight=set_data["weight"],
                    set_number=set_data["set_number"],
                )
                db.session.add(workout_set)

        db.session.commit()
        return (
            jsonify({"id": workout.id, "message": "Workout logged successfully"}),
            201,
        )

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"Invalid data: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to log workout"}), 500


@workouts_bp.route("", methods=["GET"])
@jwt_required()
def get_workouts():
    """
    Get all workouts for current user

    GET /api/workouts?days=30
    Headers: Authorization: Bearer <token>

    Query Parameters:
    - days:

    Returns:
    [
        {
            "id":
            "date":
            "exercises":
        },
        ...
    ]
    """
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 30, type=int)
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    workouts = (
        Workout.query.filter_by(user_id=user_id)
        .filter(Workout.date >= cutoff_date)
        .order_by(Workout.date.desc())
        .all()
    )

    return jsonify([serialize_workout(w) for w in workouts]), 200


@workouts_bp.route("/<int:workout_id>", methods=["GET"])
@jwt_required()
def get_workout(workout_id):
    """
    Get specific workout by ID

    GET /api/workouts/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "id":
        "date":
        "exercises":
    }
    """
    user_id = int(get_jwt_identity())
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(serialize_workout(workout)), 200


@workouts_bp.route("/<int:workout_id>", methods=["PUT"])
@jwt_required()
def update_workout(workout_id):
    """
    Update a workout

    PUT /api/workouts/1
    Headers: Authorization: Bearer <token>
    {
        "exercises":
    }

    Returns:
    {
        "message": "Workout updated successfully",
        "workout":
    }
    """
    user_id = int(get_jwt_identity())
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()

    try:
        if "exercises" in data:
            WorkoutExercise.query.filter_by(workout_id=workout_id).delete()

            for ex in data.get("exercises", []):
                exercise = WorkoutExercise(workout_id=workout.id, name=ex["name"])
                db.session.add(exercise)
                db.session.flush()

                for set_data in ex.get("sets", []):
                    workout_set = WorkoutSet(
                        exercise_id=exercise.id,
                        reps=set_data["reps"],
                        weight=set_data["weight"],
                        set_number=set_data["set_number"],
                    )
                    db.session.add(workout_set)

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Workout updated successfully",
                    "workout": serialize_workout(workout),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update workout"}), 500


@workouts_bp.route("/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete_workout(workout_id):
    """
    Delete a workout

    DELETE /api/workouts/1
    Headers: Authorization: Bearer <token>

    Returns:
    {
        "message": "Workout deleted successfully"
    }
    """
    user_id = int(get_jwt_identity())
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 204
