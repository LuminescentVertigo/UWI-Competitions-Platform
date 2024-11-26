class RankingSystem:
    def __init__(self):
        self.students = []
        self.observers = []

    #Calculate rankings for all students
    def calculate_ranking(self, students):
        students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)
        for index, student in enumerate(students, start=1):
            student.curr_rank = index
            self.notify_observers(student)


    #Notify all registered observers
    def notify_observers(self, student):
        for observer in self.observers:
            observer.update(student)

    #Register an observer to the system
    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
