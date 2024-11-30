from flask import Blueprint, jsonify, request
from App.database import db
from App.models import Notification, Student

notifications = Blueprint('notifications', __name__)

# Add a notification for a student
def add_notification(student_id, message):
    new_notification = Notification(student_id=student_id, message=message) 
    db.session.add(new_notification)
    db.session.commit()
    return new_notification

# Route to add a notification manually (e.g. for testing purposes)
@notifications.route('/notifications', methods=['POST'])
def create_notification():
    data = request.json
    student_id = data.get('student_id')
    message = data.get('message')

    if not student_id or not message:
        return jsonify({"error": "Missing student_id or message"}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    notification = add_notification(student_id, message)
    return jsonify(notification.get_json()), 201

# Route to retrieve all notifications for a specific student
@notifications.route('/notifications/<int:student_id>', methods=['GET'])
def get_notifications(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    notifications = Notification.query.filter_by(student_id=student_id).all()
    if not notifications:
        return f"No notifications found for student ID: {student_id}."

    return "\n".join([str(notification.to_dict()) for notification in notifications])
    # return jsonify([notification.get_json() for notification in notifications]), 200

# Logic for updating ranking notifications
def notify_ranking_change(student_id, old_rank, new_rank):
    if old_rank < new_rank:
        message = f"Your rank has improved from {old_rank} to {new_rank}!"
    elif old_rank > new_rank:
        message = f"Your rank has dropped from {old_rank} to {new_rank}."
    else:
        return  # No change in ranking, no notification needed
    
    add_notification(student_id, message)

# Example endpoint for simulating rank updates (for testing purposes)
@notifications.route('/notifications/rank-update', methods=['POST'])
def rank_update():
    data = request.json
    student_id = data.get('student_id')
    old_rank = data.get('old_rank')
    new_rank = data.get('new_rank')

    if not student_id or old_rank is None or new_rank is None:
        return jsonify({"error": "Missing student_id, old_rank, or new_rank"}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    notify_ranking_change(student_id, old_rank, new_rank)
    return jsonify({"message": "Notification sent."}), 200