from flask import Blueprint, redirect, render_template, request, jsonify, session
from flask_login import login_required, login_user, current_user, logout_user
from App.models import db, ranking_observer
from App.controllers import *
import csv

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route("/api/profile", methods=["GET"])
@login_required
def api_profile():
    user_type = session.get("user_type")
    user_id = current_user.get_id()

    if user_type == "moderator":
        moderator = get_moderator(user_id)
        if moderator:
            return jsonify({"id": moderator.id, "username": moderator.username, "type": "moderator"}), 200
        return jsonify({"error": "Moderator not found"}), 404

    elif user_type == "student":
        student = get_student(user_id)
        if student:
            profile_info = display_student_info(student.id)
            return jsonify(profile_info), 200
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"error": "User type not recognized"}), 403

#Initialize the database and load data from CSV files
@index_views.route("/api/init", methods=["POST"])
def api_init():
    db.drop_all()
    db.create_all()

    with open("students.csv") as student_file:
        reader = csv.DictReader(student_file)
        for student in reader:
            stud = create_student(student['username'], student['password'])
            ranking_system = RankingSystem() 
            stud.register_observer(ranking_observer)  
            ranking_system.register_observer(stud)  
        student_file.close()


    with open("moderators.csv") as moderator_file:
        reader = csv.DictReader(moderator_file)
        for moderator in reader:
            mod = create_moderator(moderator['username'], moderator['password'])
        moderator_file.close()

    with open("competitions.csv") as competition_file:
        reader = csv.DictReader(competition_file)
        for competition in reader:
            comp = create_competition(competition['mod_name'], competition['comp_name'], competition['date'], competition['location'], competition['level'], competition['max_score'])
        competition_file.close()

    with open("results.csv") as results_file:
        reader = csv.DictReader(results_file)
        for result in reader:
            students = [result['student1'], result['student2'], result['student3']]
            team = add_team(result['mod_name'], result['comp_name'], result['team_name'], students)
            add_results(result['mod_name'], result['comp_name'], result['team_name'], int(result['score']))
        results_file.close()

    with open("competitions.csv") as competitions_file:
        reader = csv.DictReader(competitions_file)
        for competition in reader:
            if competition['comp_name'] != 'TopCoder':
                update_ratings(competition['mod_name'], competition['comp_name'])
                update_rankings() 
    competitions_file.close()

    display_rankings()
    print('Database initialized and rankings updated.')

    return jsonify({"message": "Database initialized and rankings updated"}), 200

#retrieve the leaderboard
@index_views.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = display_rankings()
    return jsonify(leaderboard), 200

#recalculate rankings for all users (Special Feature API Call for rank updates)
@index_views.route('/api/rankings/update', methods=['POST'])
def update_all_rankings():
    update_rankings()
    return jsonify({"message": "Rankings updated successfully!"}), 200

#retrieve a student's profile
@index_views.route('/api/student/<int:id>/profile', methods=['GET'])
def get_student_profile(id):
    student = get_student(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    profile_info = display_student_info(student.id)
    return jsonify(profile_info), 200

#retrieve a moderator's profile
@index_views.route('/api/moderator/<int:id>/profile', methods=['GET'])
def get_moderator_profile(id):
    moderator = get_moderator(id)
    if not moderator:
        return jsonify({"error": "Moderator not found"}), 404

    return jsonify({"id": moderator.id, "username": moderator.username}), 200

#retrieve notifications for a specific student
@index_views.route('/api/notifications/<int:student_id>', methods=['GET'])
def get_student_notifications(student_id):
    notifications = display_notifications(student_id)
    if not notifications:
        return jsonify({"message": f"No notifications found for student ID {student_id}"}), 404
    return jsonify(notifications), 200

#retrieve a student's current ranking
@index_views.route('/api/rankings/student/<int:student_id>', methods=['GET'])
def get_student_ranking(student_id):
    student = get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"id": student.id, "username": student.username, "rank": student.curr_rank, "rating": student.rating_score}), 200

