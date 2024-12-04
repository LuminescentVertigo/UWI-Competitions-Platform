from flask import Blueprint, render_template, jsonify, request, session
from flask_login import login_required, login_user, current_user, logout_user
from App.models import db
from App.controllers import (
    get_student_by_username,
    get_moderator_by_username,
    create_student,
    display_rankings,
    update_rankings,
)

auth_views = Blueprint("auth_views", __name__, template_folder="../templates")

@auth_views.route("/api/login", methods=["POST"])
def login_api():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    student = get_student_by_username(username)
    moderator = get_moderator_by_username(username)

    if student and student.check_password(password):
        login_user(student)
        session["user_type"] = "student"
        return jsonify({"message": "Login successful!", "user_type": "student", "id": student.id}), 200

    if moderator and moderator.check_password(password):
        login_user(moderator)
        session["user_type"] = "moderator"
        return jsonify({"message": "Login successful!", "user_type": "moderator", "id": moderator.id}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@auth_views.route("/api/logout", methods=["POST"])
@login_required
def logout_api():
    logout_user()
    session["user_type"] = None
    return jsonify({"message": "Logout successful!"}), 200

@auth_views.route("/api/signup", methods=["POST"])
def signup_api():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    student = create_student(username, password)

    if student:
        login_user(student)
        session["user_type"] = "student"
        return jsonify({"message": "Signup successful!", "user_id": student.id}), 201

    return jsonify({"error": "Username already taken"}), 409

# Demonstration of Observer Pattern
@auth_views.route("/api/rankings/update", methods=["POST"])
@login_required
def trigger_rank_update_api():
    if session.get("user_type") != "moderator":
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        leaderboard = update_rankings()
        return jsonify({"message": "Rankings updated successfully!", "leaderboard": leaderboard}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# View the leaderboard
@auth_views.route("/api/leaderboard", methods=["GET"])
@login_required
def leaderboard_api():
    leaderboard = display_rankings()
    return jsonify(leaderboard), 200
