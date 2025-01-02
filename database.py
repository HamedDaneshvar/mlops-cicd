from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Store hashed password
    password = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc),
                           nullable=False)

    # Relationship to CancerDiagnosis (one-to-many)
    diagnoses = db.relationship('CancerDiagnosis', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.fullname}')"


class CancerDiagnosis(db.Model):
    __tablename__ = "cancer_diagnoses"
    id = db.Column(db.Integer, primary_key=True)

    # Link to User model (foreign key)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Form fields for cancer diagnosis
    mean_radius = db.Column(db.Float, nullable=False)
    mean_texture = db.Column(db.Float, nullable=False)
    mean_perimeter = db.Column(db.Float, nullable=False)
    mean_area = db.Column(db.Float, nullable=False)
    mean_smoothness = db.Column(db.Float, nullable=False)
    mean_compactness = db.Column(db.Float, nullable=False)
    mean_concavity = db.Column(db.Float, nullable=False)
    mean_concave_points = db.Column(db.Float, nullable=False)
    mean_symmetry = db.Column(db.Float, nullable=False)
    mean_fractal_dimension = db.Column(db.Float, nullable=False)
    radius_error = db.Column(db.Float, nullable=False)
    texture_error = db.Column(db.Float, nullable=False)
    perimeter_error = db.Column(db.Float, nullable=False)
    area_error = db.Column(db.Float, nullable=False)
    smoothness_error = db.Column(db.Float, nullable=False)
    compactness_error = db.Column(db.Float, nullable=False)
    concavity_error = db.Column(db.Float, nullable=False)
    concave_points_error = db.Column(db.Float, nullable=False)
    symmetry_error = db.Column(db.Float, nullable=False)
    fractal_dimension_error = db.Column(db.Float, nullable=False)
    worst_radius = db.Column(db.Float, nullable=False)
    worst_texture = db.Column(db.Float, nullable=False)
    worst_perimeter = db.Column(db.Float, nullable=False)
    worst_area = db.Column(db.Float, nullable=False)
    worst_smoothness = db.Column(db.Float, nullable=False)
    worst_compactness = db.Column(db.Float, nullable=False)
    worst_concavity = db.Column(db.Float, nullable=False)
    worst_concave_points = db.Column(db.Float, nullable=False)
    worst_symmetry = db.Column(db.Float, nullable=False)
    worst_fractal_dimension = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc),
                           nullable=False)

    # Diagnosis result (Cancerous or Non-Cancerous)
    diagnosis_result = db.Column(db.String(20), nullable=False)
