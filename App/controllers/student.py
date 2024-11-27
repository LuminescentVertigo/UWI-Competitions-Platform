from App.database import db
from App.models import Student, Notification, RankingObserver, RankingSystem
from App.models.competition import Competition
from App.models.competition_team import CompetitionTeam

#Create a new student and register them
def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    new_student = Student(username=username, password=password)
    ranking_observer = RankingObserver()

    if ranking_observer not in new_student.observers:  
        new_student.register_observer(ranking_observer)

    try:
        db.session.add(new_student)
        db.session.commit()
        print(f'New Student: {username} created!')
        return new_student
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}: {e}')
        return None

#Retrieve a student by username
def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

#Retrieve a student by ID
def get_student(id):
    return Student.query.get(id)

#Retrieve all students
def get_all_students():
    return Student.query.all()

#Get all students as JSON
def get_all_students_json():
    students = get_all_students()
    student_list = []
    for student in students:
        student_data = student.get_json()
        student_list.append(student_data)
    
    return student_list

#Update a student's username
def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        try:
            db.session.add(student)
            db.session.commit()
            print("Username was updated!")
            return student
        except Exception as e:
            db.session.rollback()
            print(f"Username was not updated: {e}")
            return None
    print(f"ID: {id} does not exist!")
    return None

#Display a student's profile
def display_student_info(student_id):
    student = get_student(student_id)

    if not student:
        print(f'No student found with ID {student_id}!')
        return None

    competitions = []
    for team in student.teams:
        team_comps = CompetitionTeam.query.filter_by(team_id=team.id).all()
        for comp_team in team_comps:
            comp = Competition.query.filter_by(id=comp_team.comp_id).first()
            competitions.append(comp.name)

    profile_info = {
        "profile": student.to_dict(),
        "competitions": competitions
    }
    return profile_info

#Display all notifications for a student.
def display_notifications(student_id):
    student = get_student(student_id)
    if not student:
        print(f"Student with ID {student_id} does not exist!")
        return []

    notifications = student.notifications
    notification_list = []
    for notification in notifications:
        notification_list.append({
            "message": notification.message,
            "timestamp": notification.timestamp
        })
    
    return notification_list

#Update a student's rating and trigger rank recalculation
def update_student_rating(student_id, new_rating):
    student = get_student(student_id)
    if student:
        old_rating, updated_rating = student.update_rating(new_rating)
        print(f"Updated {student.username}'s rating from {old_rating} to {updated_rating}.")
        return {"old_rating": old_rating, "updated_rating": updated_rating}
    print(f"Student with ID {student_id} not found.")
    return None

#Recalculate rankings for all students and notify observers
def update_rankings():
    students = get_all_students()
    if not students:
        print("No students found to update rankings.")
        return []

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)
    leaderboard = []
    count = 1
    curr_high = students[0].rating_score if students else 0
    curr_rank = 1

    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        if student.comp_count != 0:
            leaderboard.append({
                "placement": curr_rank,
                "student": student.username,
                "rating_score": student.rating_score
            })
            count += 1

            if student.curr_rank != curr_rank:
                student.curr_rank = curr_rank
                if student.prev_rank == 0:
                    message = f'RANK: {student.curr_rank}. Congratulations on your first rank!'
                elif student.curr_rank < student.prev_rank:
                    message = f'RANK: {student.curr_rank}. Congratulations! Your rank has improved!'
                elif student.curr_rank > student.prev_rank:
                    message = f'RANK: {student.curr_rank}. Oh no! Your rank has dropped!'
                else:
                    message = f'RANK: {student.curr_rank}. You retained your rank!'

                student.prev_rank = student.curr_rank
                notification = Notification(student_id=student.id, message=message)
                db.session.add(notification)

                print(f"Notification created: {message} for student {student.username}")

                try:
                    db.session.commit()  # Commit changes before notifying observers
                    student.notify_observers()  # Notify observers after rank updates
                except Exception as e:
                    db.session.rollback()
                    print(f"Error updating student {student.username}'s rank: {e}")

    return leaderboard


#Display overall rankings including scores
def display_rankings():
    students = get_all_students()
    if not students:
        print("No students found to display rankings.")
        return []

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)
    leaderboard = []
    count = 1
    curr_high = students[0].rating_score if students else 0
    curr_rank = 1

    for student in students:
        # If the score is different from the previous student, update rank
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        # Ensure only students with a competition count > 0 are included
        if student.comp_count != 0:
            leaderboard.append({
                "placement": curr_rank,
                "student": student.username,
                "rating_score": student.rating_score
            })
            count += 1

    # Print the leaderboard in a readable format
    print(f"{'Rank':<5}{'Student':<20}{'Rating Score'}") 
    for position in leaderboard:
        print(f"{position['placement']:<5}{position['student']:<20}{position['rating_score']}")
    
    return leaderboard


    

