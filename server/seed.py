"""Seed database with demo user and workout logs."""
from datetime import date
from config import app, db
from models import User, Workout

with app.app_context():
    print("Clearing old data...")
    Workout.query.delete()
    User.query.delete()

    print("Creating demo user...")
    user = User(username="yakin", password_hash="password123")
    db.session.add(user)
    db.session.commit()

    print("Creating sample workouts...")
    w1 = Workout(
        exercise="Bench Press",
        duration_minutes=45,
        notes="Pushed for heavy triples.",
        date=date.today(),
        user_id=user.id
    )
    w2 = Workout(
        exercise="5k Run",
        duration_minutes=25,
        notes="Paced 5:00 min/km.",
        date=date.today(),
        user_id=user.id
    )
    db.session.add_all([w1, w2])
    db.session.commit()

    print("Database re-seeded for Workouts! Log in with username: yakin, password: password123")
