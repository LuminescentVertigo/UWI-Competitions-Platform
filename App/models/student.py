from App.database import db
from App.models.user import User  # Import User model explicitly
from sqlalchemy.orm import relationship

class Student(User):
    __tablename__ = 'student'

    rating_score = db.Column(db.Float, nullable=False, default=0)
    comp_count = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    prev_rank = db.Column(db.Integer, nullable=False, default=0)

    teams = relationship('Team', secondary='student_team', overlaps='students', lazy=True)
    notifications = relationship('Notification', backref='student', lazy=True)

    observers = []

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rating_score = 0
        self.comp_count = 0
        self.curr_rank = 0
        self.prev_rank = 0
        self.teams = []
        self.notifications = []
        self.observers = []  

    #Register an observer
    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    #Notify all observers
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    #Update the rating score and trigger rank recalculation
    def update_rating(self, new_rating):
        old_rating = self.rating_score
        self.rating_score = new_rating
        self.comp_count += 1
        db.session.commit()
        return old_rating, new_rating

    #Recalculate rank based on the updated rating
    def recalculate_rank(self):
        students = Student.query.all()
        students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)
        curr_rank = 1
        prev_rating = -1
        for student in students:
            if student.rating_score != prev_rating:
                student.curr_rank = curr_rank
                prev_rating = student.rating_score
            curr_rank += 1
            db.session.commit()
    #Add a notification
    def add_notification(self, notification):
        if notification:
            try:
                self.notifications.append(notification)
                db.session.commit()
                return notification
            except Exception as e:
                db.session.rollback()
                return None
        return None

    #Convert the student to JSON
    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rating_score": self.rating_score,
            "comp_count": self.comp_count,
            "curr_rank": self.curr_rank
        }

    #Convert the student to a dictionary
    def to_dict(self):
        return {
            "ID": self.id,
            "Username": self.username,
            "Rating Score": self.rating_score,
            "Number of Competitions": self.comp_count,
            "Rank": self.curr_rank
        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'
