from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from App.controllers.notification import add_notification, get_notifications, notify_ranking_change
from App.models import Student

notifications_views = Blueprint('notifications_views', __name__)

#Manually add a notification
@notifications_views.route('/api/notifications', methods=['POST'])
def create_notification_api():
    data = request.json
    student_id = data.get('student_id')
    message = data.get('message')

    if not student_id or not message:
        return jsonify({"error": "Missing student_id or message"}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    notification = add_notification(student_id, message)
    if notification:
        return jsonify({"message": "Notification added successfully!", "notification": notification.get_json()}), 201

    return jsonify({"error": "Error adding notification"}), 500

#Handle ranking change notifications
@notifications_views.route('/api/notifications/rank-update', methods=['POST'])
def rank_update_api():
    data = request.json
    student_id = data.get('student_id')
    old_rank = data.get('old_rank')
    new_rank = data.get('new_rank')

    # Validate inputs
    if not student_id or old_rank is None or new_rank is None:
        return jsonify({"error": "Missing required fields: student_id, old_rank, new_rank"}), 400

    try:
        old_rank = int(old_rank)
        new_rank = int(new_rank)
    except ValueError:
        return jsonify({"error": "Old rank and new rank must be integers"}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    notify_ranking_change(student_id, old_rank, new_rank)
    return jsonify({"message": f"Ranking change notification processed for student ID {student_id}"}), 200
