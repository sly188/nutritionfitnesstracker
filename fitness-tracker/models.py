"""
Database models for Fitness Tracker application.
All SQLAlchemy ORM models defined here.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """User account model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    workouts = db.relationship(
        "Workout", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    nutrition_logs = db.relationship(
        "NutritionLog", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    templates = db.relationship(
        "WorkoutTemplate", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    goals = db.relationship(
        "Goal", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    weights = db.relationship(
        "WeightLog", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class WorkoutTemplate(db.Model):
    """Reusable workout template (e.g., Leg Day, Back Day)"""

    __tablename__ = "workout_templates"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    exercises = db.relationship(
        "TemplateExercise", backref="template", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<WorkoutTemplate {self.name}>"


class TemplateExercise(db.Model):
    """Exercise within a workout template"""

    __tablename__ = "template_exercises"

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(
        db.Integer, db.ForeignKey("workout_templates.id"), nullable=False
    )
    name = db.Column(db.String(120), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.String(50), nullable=True)
    alternatives = db.Column(db.String(500))

    def __repr__(self):
        return f"<TemplateExercise {self.name}>"


class Workout(db.Model):
    """Logged workout session"""

    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey("workout_templates.id"))
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    exercises = db.relationship(
        "WorkoutExercise", backref="workout", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Workout {self.date}>"


class WorkoutExercise(db.Model):
    """Exercise within a logged workout"""

    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    sets = db.relationship(
        "WorkoutSet", backref="exercise", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<WorkoutExercise {self.name}>"


class WorkoutSet(db.Model):
    """Individual set within an exercise"""

    __tablename__ = "workout_sets"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("workout_exercises.id"), nullable=False
    )
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    set_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<WorkoutSet Set#{self.set_number}>"


class NutritionLog(db.Model):
    """Daily nutrition tracking"""

    __tablename__ = "nutrition_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<NutritionLog {self.date}>"


class WeightLog(db.Model):
    """Weight tracking"""

    __tablename__ = "weight_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<WeightLog {self.weight}lbs>"


class Goal(db.Model):
    """User fitness goals"""

    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    goal_type = db.Column(
        db.String(50), nullable=False
    )  # 'weight', 'calories', 'workout_count'
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, default=0)
    period = db.Column(db.String(20), nullable=False)  # 'month', 'year'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Goal {self.goal_type}>"
