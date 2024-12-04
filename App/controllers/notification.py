from flask import Blueprint, jsonify, request
from App.database import db
from App.models import Notification, Student
import logging

notifications = Blueprint('notifications', __name__)

# Utility session to commit session changes
def commit_session():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database commit failed: {str(e)}")
        raise e


# Add a notification for a student
def add_notification(student_id, message):
    try:
        new_notification = Notification(student_id=student_id, message=message) 
        db.session.add(new_notification)
        commit_session()
        logging.info(f"Notification added for student {student_id}")
        return new_notification
    except Exception as e:
        logging.error(f"Failed to add notification for student {student_id}: {str(e)}")
        raise e


# Route to add a notification manually (e.g. for testing purposes)
@notifications.route('/notifications/create', methods=['POST'])
def create_notification():
    data = request.json
    student_id = data.get('student_id')
    message = data.get('message')

    if not student_id or not message:
        return jsonify({"error": "Missing student_id or message"}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    try:
        notification = add_notification(student_id, message)
        return jsonify(notification.get_json()), 201
    except Exception as e:
        return jsonify({"error": "Failed to create notifications"}), 500


#retrieve all notifications for a specific student
def get_notifications(student_id):
    student = Student.query.get(student_id)
    if not student:
        return None

    notifications = Notification.query.filter_by(student_id=student_id).all()
    return notifications  # Return the list of Notification objects

# Logic for updating ranking notifications
def notify_ranking_change(student_id, old_rank, new_rank):
    if old_rank is None or new_rank is None:
        logging.error("Invalid rank values provided.")
        raise ValueError("Invalid rank values provided.")

    if old_rank < new_rank:
        message = f"Your rank has dropped from {old_rank} to {new_rank}."
    elif new_rank < old_rank:
        message = f"Your rank has improved from {old_rank} to {new_rank}!"
    else:
        logging.info(f"No rank change for student {student_id}. No notification needed.")
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

    try:
        old_rank = int(old_rank)
        new_rank = int(new_rank)
    except ValueError:
        return jsonify({"error": "Invalid rank values. They must be integers."}), 400

    try:
        notify_ranking_change(student_id, old_rank, new_rank)
        return jsonify({"message": "Notification sent."}), 200
    except Exception as e:
        logging.error(f"Failed to notify rank changes for student {student_id}: {str:(e)}")
        return jsonify({"error": "Failed to process rank update"}), 500