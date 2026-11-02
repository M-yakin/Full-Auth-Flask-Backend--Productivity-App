"""Database models: User and Workout."""
from datetime import date
from sqlalchemy.orm import validates
from config import bcrypt, db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    workouts = db.relationship(
        "Workout", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates("username")
    def validate_username(self, key, value):
        if not value or not value.strip():
            raise ValueError("Username is required.")
        return value.strip()

    def to_dict(self):
        return {"id": self.id, "username": self.username}


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="workouts")

    @validates("exercise")
    def validate_exercise(self, key, value):
        if not value or not str(value).strip():
            raise ValueError("Exercise is required.")
        return str(value).strip()

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("Duration must be a positive whole number of minutes.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "exercise": self.exercise,
            "duration_minutes": self.duration_minutes,
            "notes": self.notes,
            "date": self.date.isoformat(),
            "user_id": self.user_id,
        }
