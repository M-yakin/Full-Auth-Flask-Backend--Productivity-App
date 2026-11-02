"""Flask RESTful API: Workouts and User Sessions."""
from datetime import date
from functools import wraps
from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import api, app, db
from models import User, Workout


def current_user():
    user_id = session.get("user_id")
    return db.session.get(User, user_id) if user_id else None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user() is None:
            session.pop("user_id", None)
            return {"error": "Unauthorized. Please log in."}, 401
        return fn(*args, **kwargs)
    return wrapper


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError("Date must be in YYYY-MM-DD format.")


class Signup(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password are required."}, 422

        try:
            user = User(username=username, password_hash=password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Username already taken."}, 422
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422

        session["user_id"] = user.id
        return user.to_dict(), 201


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter_by(username=data.get("username")).first()

        if user and user.authenticate(data.get("password") or ""):
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid username or password."}, 401


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204

    post = delete


class CheckSession(Resource):
    def get(self):
        user = current_user()
        if user:
            return user.to_dict(), 200
        return {"error": "Unauthorized. Please log in."}, 401


class WorkoutList(Resource):
    method_decorators = [login_required]

    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = Workout.query.filter_by(user_id=session["user_id"])\
            .order_by(Workout.date.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return [w.to_dict() for w in pagination.items], 200

    def post(self):
        data = request.get_json() or {}
        try:
            workout = Workout(
                exercise=data.get("exercise"),
                duration_minutes=int(data.get("duration_minutes", 0)),
                notes=data.get("notes"),
                date=parse_date(data["date"]) if data.get("date") else date.today(),
                user_id=session["user_id"],
            )
            db.session.add(workout)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422
        return workout.to_dict(), 201


class WorkoutDetail(Resource):
    method_decorators = [login_required]

    def delete(self, workout_id):
        workout = Workout.query.filter_by(id=workout_id, user_id=session["user_id"]).first()
        if not workout:
            return {"error": "Workout not found."}, 404

        data = request.get_json() or {}
        try:
            if "exercise" in data:
                workout.exercise = data["exercise"]
            if "duration_minutes" in data:
                workout.duration_minutes = int(data["duration_minutes"])
            if "notes" in data:
                workout.notes = data["notes"]
            if "date" in data:
                workout.date = parse_date(data["date"])

            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422

        return workout.to_dict(), 200

    def delete(self, workout_id):
        workout = Workout.query.filter_by(id=workout_id, user_id=session["user_id"]).first()
        if not workout:
            return {"error": "Workout not found."}, 404
        db.session.delete(workout)
        db.session.commit()
        return {}, 204


api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/me", "/check_session")
api.add_resource(WorkoutList, "/workouts")
api.add_resource(WorkoutDetail, "/workouts/<int:workout_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
