from flask import Blueprint, jsonify, request, send_from_directory, flash
from flask_jwt_extended import create_access_token
from App.controllers import create_student, get_all_students_json, display_rankings, display_notifications
from App.controllers.moderator import create_moderator
from App.models import Student

user_views = Blueprint('user_views', __name__, template_folder='../templates')

#create a new student
@user_views.route("/api/students", methods=["POST"])
def create_student_api():
    data = request.json
    student = create_student(data["username"], data["password"])
    if student:
        return jsonify({"message": f"User {student.username} created successfully"}), 201
    return jsonify({"message": "Username already exists"}), 409

#create a new moderator
@user_views.route("/api/moderators", methods=["POST"])
def create_moderator_api():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    moderator = create_moderator(username, password)

    if moderator:
        return jsonify({
            "message": f"Moderator {username} created successfully!",
            "id": moderator.id
        }), 201

    return jsonify({"error": "Failed to create moderator. Username may already exist."}), 409

#get all students as a JSON list
@user_views.route('/api/students', methods=['GET'])
def get_all_students():
    students = get_all_students_json()
    return jsonify(students), 200

#get the overall rankings of all students
@user_views.route("/api/rankings", methods=["GET"])
def get_rankings_api():
    rankings = display_rankings()
    return jsonify(rankings), 200

#fetch all notifications for a specific student
@user_views.route("/api/students/<int:student_id>/notifications", methods=["GET"])
def get_student_notifications_api(student_id):
    notifications = display_notifications(student_id)
    if notifications:
        return jsonify(notifications), 200
    return jsonify({"message": f"No notifications found for student ID {student_id}"}), 404


