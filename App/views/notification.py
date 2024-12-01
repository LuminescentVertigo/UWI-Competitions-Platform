from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from App.controllers.notifications_controller import (add_notification, get_notifications, notify_ranking_change,)
from App.models import Student

notifications_views = Blueprint('notifications_views', __name__, template_folder='../templates')


# Route to display all notifications for a student
@notifications_views.route('/notifications/<int:student_id>', methods=['GET'])
@login_required
def view_notifications(student_id):
    if current_user.id != student_id:
        flash("You are not authorized to view these notifications.", "danger")
        return redirect(url_for('notifications_views.notifications_home'))

    notifications = get_notifications(student_id)
    if not notifications:
        flash(f"No notifications found for student ID {student_id}.", "info")

    return render_template('notifications.html', student_id=student_id, notifications=notifications)


# Route to manually add a notification
@notifications_views.route('/add-notification', methods=['GET', 'POST'])
@login_required
def add_notification_view():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        message = request.form.get('message')

        # Check if student ID and message are provided
        if not student_id or not message:
            flash("Please provide both student ID and a message.", "danger")
            return redirect(url_for('notifications_views.add_notification_view'))

        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            flash(f"No student found with ID {student_id}.", "danger")
            return redirect(url_for('notifications_views.add_notification_view'))

        try:
            # Attempt to add the notification
            notification = add_notification(student_id, message)
            if notification:
                flash(f"Notification added successfully for student ID {student_id}.", "success")
            else:
                flash("There was an error adding the notification.", "danger")
        except Exception as e:
            # If any error occurs, catch it and display a message
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('notifications_views.add_notification_view'))

        return redirect(url_for('notifications_views.notifications_home'))

    return render_template('add-notification.html')


# Route to handle ranking change notifications
@notifications_views.route('/notifications/rank-update', methods=['POST'])
@login_required
def rank_update_notification():
    student_id = request.form.get('student_id')
    old_rank = request.form.get('old_rank')
    new_rank = request.form.get('new_rank')

    # Check if all required fields are provided
    if not student_id or old_rank is None or new_rank is None:
        flash("All fields (student ID, old rank, new rank) are required.", "danger")
        return redirect(url_for('notifications_views.notifications_home'))

    # Validate rank fields to ensure they are integers
    try:
        old_rank = int(old_rank)
        new_rank = int(new_rank)
    except ValueError:
        flash("Old rank and new rank must be valid numbers.", "danger")
        return redirect(url_for('notifications_views.notifications_home'))

    # Check if the student exists
    student = Student.query.get(student_id)
    if not student:
        flash(f"No student found with ID {student_id}.", "danger")
        return redirect(url_for('notifications_views.notifications_home'))

    # Send notification for ranking change
    try:
        notify_ranking_change(student_id, old_rank, new_rank)
        flash(f"Ranking change notification processed successfully for student {student_id}.", "success")
    except Exception as e:
        flash(f"An error occurred while processing the ranking change notification: {str(e)}", "danger")

    return redirect(url_for('notifications_views.notifications_home'))


# Route to display the notifications home page
@notifications_views.route('/notifications-home', methods=['GET'])
@login_required
def notifications_home():
    return render_template('notifications-home.html')