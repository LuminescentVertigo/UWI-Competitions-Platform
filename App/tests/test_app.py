import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class UnitTests(unittest.TestCase):
    '''
    #User Unit Tests
    def test_new_user(self):
        user = User("ryan", "ryanpass")
        assert user.username == "ryan"

    def test_hashed_password(self):
        password = "ryanpass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("ryan", password)
        assert user.password != password

    def test_check_password(self):
        password = "ryanpass"
        user = User("ryan", password)
        assert user.check_password(password)

    #Student Unit Tests
    def test_new_student(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      assert student.username == "james"

    def test_student_get_json(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      self.assertDictEqual(student.get_json(), {"id": None, "username": "james", "rating_score": 0, "comp_count": 0, "curr_rank": 0})

    #Moderator Unit Tests
    def test_new_moderator(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      assert mod.username == "robert"

    def test_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      self.assertDictEqual(mod.get_json(), {"id":None, "username": "robert", "competitions": []})
    
    #Team Unit Tests
    def test_new_team(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      assert team.name == "Scrum Lords"
    
    def test_team_get_json(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      self.assertDictEqual(team.get_json(), {"id":None, "name":"Scrum Lords", "students": []})
    
    #Competition Unit Tests
    def test_new_competition(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      assert competition.name == "RunTime" and competition.date.strftime("%d-%m-%Y") == "09-02-2024" and competition.location == "St. Augustine" and competition.level == 1 and competition.max_score == 25

    def test_competition_get_json(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      self.assertDictEqual(competition.get_json(), {"id": None, "name": "RunTime", "date": "09-02-2024", "location": "St. Augustine", "level": 1, "max_score": 25, "moderators": [], "teams": []})
    
    #Notification Unit Tests
    def test_new_notification(self):
      db.drop_all()
      db.create_all()
      notification = Notification(1, "Ranking changed!")
      assert notification.student_id == 1 and notification.message == "Ranking changed!"

    def test_notification_get_json(self):
      db.drop_all()
      db.create_all()
      notification = Notification(1, "Ranking changed!")
      self.assertDictEqual(notification.get_json(), {"id": None, "student_id": 1, "notification": "Ranking changed!"})
    '''
    # #Ranking Unit Tests
    # def test_new_ranking(self):
    #   db.drop_all()
    #   db.create_all()
    #   ranking = Ranking(1)
    #   assert ranking.student_id == 1
  
    # def test_set_points(self):
    #   db.drop_all()
    #   db.create_all()
    #   ranking = Ranking(1)
    #   ranking.set_points(15)
    #   assert ranking.total_points == 15

    # def test_set_ranking(self):
    #   db.drop_all()
    #   db.create_all()
    #   ranking = Ranking(1)
    #   ranking.set_ranking(1)
    #   assert ranking.curr_ranking == 1

    # def test_previous_ranking(self):
    #   db.drop_all()
    #   db.create_all()
    #   ranking = Ranking(1)
    #   ranking.set_previous_ranking(1)
    #   assert ranking.prev_ranking == 1

    # def test_ranking_get_json(self):
    #   db.drop_all()
    #   db.create_all()
    #   ranking = Ranking(1)
    #   ranking.set_points(15)
    #   ranking.set_ranking(1)
    #   self.assertDictEqual(ranking.get_json(), {"rank":1, "total points": 15})
    #New Ranking Unit Tests 

    def test_newRankingObserver(self):
      # Create the observer
      observer = RankingObserver()

      # Check if the created object is an instance of RankingObserver
      self.assertIsInstance(observer, RankingObserver)

    def test_initialize_ranking_system(self):
      # Create an instance of RankingSystem
      ranking_system = RankingSystem()

      # Verify the system starts with empty lists
      self.assertEqual(len(ranking_system.students), 0)
      self.assertEqual(len(ranking_system.observers), 0)   

    def test_register_observer(self):
      # Create an instance of RankingSystem
      ranking_system = RankingSystem()

      # Observer to register
      observer = 'observer1'

      # Register observer
      ranking_system.register_observer(observer)

      # Verify that the observer is added to the observers list
      self.assertIn(observer, ranking_system.observers)

    def test_register_observer_multiple_observers(self):
        # Create an instance of RankingSystem
        ranking_system = RankingSystem()

        # Register multiple observers
        observer1 = 'observer1'
        observer2 = 'observer2'
        ranking_system.register_observer(observer1)
        ranking_system.register_observer(observer2)

        # Verify both observers are added
        self.assertIn(observer1, ranking_system.observers)
        self.assertIn(observer2, ranking_system.observers)
    '''
    #CompetitionTeam Unit Tests
    def test_new_competition_team(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      assert competition_team.comp_id == 1 and competition_team.team_id == 1

    def test_competition_team_update_points(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      assert competition_team.points_earned == 15

    def test_competition_team_update_rating(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_rating(12)
      assert competition_team.rating_score == 12

    def test_competition_team_get_json(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      competition_team.update_rating(12)
      self.assertDictEqual(competition_team.get_json(), {"id": None, "team_id": 1, "competition_id": 1, "points_earned": 15, "rating_score": 12})

    #CompetitionModerator Unit Tests
    def test_new_competition_moderator(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      assert competition_moderator.comp_id == 1 and competition_moderator.mod_id == 1

    def test_competition_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      self.assertDictEqual(competition_moderator.get_json(), {"id": None, "competition_id": 1, "moderator_id": 1})

    #StudentTeam Unit Tests
    def test_new_student_team(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      assert student_team.student_id == 1 and student_team.team_id == 1
    
    def test_student_team_get_json(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      self.assertDictEqual(student_team.get_json(), {"id": None, "student_id": 1, "team_id": 1})

'''
   # Integration Tests

class IntegrationTests(unittest.TestCase):
    
    #Feature 1 Integration Tests
    def test1_create_competition(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      assert comp.name == "RunTime" and comp.date.strftime("%d-%m-%Y") == "29-03-2024" and comp.location == "St. Augustine" and comp.level == 2 and comp.max_score == 25

    def test2_create_competition(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      self.assertDictEqual(comp.get_json(), {"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": []})
      
    #Feature 2 Integration Tests
    def test1_add_results(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      assert comp_team.points_earned == 15
    
    def test2_add_results(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      students = [student1.username, student2.username, student3.username]
      add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students = [student1.username, student4.username, student5.username]
      team = add_team(mod.username, comp.name, "Scrum Lords", students)
      assert team == None
    
    def test3_add_results(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod2.username, comp.name, "Runtime Terrors", students)
      assert team == None

    #Feature 3 Integration Tests
    def test_display_student_info(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      update_ratings(mod.username, comp.name)
      update_rankings()
      self.assertDictEqual(display_student_info(1), {"profile": {'id': 1, 'username': 'james', 'rating_score': 24.0, 'comp_count': 1, 'curr_rank': 1}, "competitions": ['RunTime']})

    #Feature 4 Integration Tests
    def test_display_competition(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      student7 = create_student("isabella", "isabellapass")
      student8 = create_student("richard", "richardpass")
      student9 = create_student("jessica", "jessicapass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 12)
      students3 = [student7.username, student8.username, student9.username]
      team3 = add_team(mod.username, comp.name, "Beyond Infinity", students3)
      comp_team = add_results(mod.username, comp.name, "Beyond Infinity", 10)
      update_ratings(mod.username, comp.name)
      update_rankings()
      self.assertDictEqual(comp.get_json(), {'id': 1, 'name': 'RunTime', 'date': '29-03-2024', 'location': 'St. Augustine', 'level': 2, 'max_score': 25, 'moderators': ['debra'], 'teams': ['Runtime Terrors', 'Scrum Lords', 'Beyond Infinity']})

    #Feature 5 Integration Tests
    # def test_display_rankings(self):
    #   db.drop_all()
    #   db.create_all()
    #   mod = create_moderator("debra", "debrapass")
    #   comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
    #   student1 = create_student("james", "jamespass")
    #   student2 = create_student("steven", "stevenpass")
    #   student3 = create_student("emily", "emilypass")
    #   student4 = create_student("mark", "markpass")
    #   student5 = create_student("eric", "ericpass")
    #   student6 = create_student("ryan", "ryanpass")
    #   students1 = [student1.username, student2.username, student3.username]
    #   team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
    #   comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
    #   students2 = [student4.username, student5.username, student6.username]
    #   team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
    #   comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 10)
    #   update_ratings(mod.username, comp.name)
    #   update_rankings()
    #   self.assertListEqual(display_rankings(), [{"placement": 1, "student": "james", "rating score": 24.0}, {"placement": 1, "student": "steven", "rating score": 24.0}, {"placement": 1, "student": "emily", "rating score": 24.0}, {"placement": 4, "student": "mark", "rating score": 16.0}, {"placement": 4, "student": "eric", "rating score": 16.0}, {"placement": 4, "student": "ryan", "rating score": 16.0}])





    def test_display_notifications(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      students1 = [student1.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      update_ratings(mod.username, comp.name)
      update_rankings()

      # Assuming a notification is generated with ID=1 for this setup
      notification = display_notifications(1)

      # Check if the first notification in the list matches the expected output
      expected = {'id': 1, 'student_id': 1, 'message': 'RANK: 1. Congratulations on your first rank!'}
      self.assertDictEqual(notification[0], expected)
  
    # def test2_display_notification(self):
    #   db.drop_all()
    #   db.create_all()
    #   mod = create_moderator("debra", "debrapass")
      
    #   # Create competitions and students
    #   comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
    #   comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 30)
      
    #   student1 = create_student("james", "jamespass")
    #   student2 = create_student("steven", "stevenpass")
    #   student3 = create_student("emily", "emilypass")
    #   student4 = create_student("mark", "markpass")
    #   student5 = create_student("eric", "ericpass")
    #   student6 = create_student("ryan", "ryanpass")
      
    #   # Add teams and results for competition 1
    #   students1 = [student1.username, student2.username, student3.username]
    #   team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
    #   comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      
    #   students2 = [student4.username, student5.username, student6.username]
    #   team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
    #   comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      
    #   # Update ratings and rankings for competition 1
    #   update_ratings(mod.username, comp1.name)
    #   update_rankings()
      
    #   # Add teams and results for competition 2
    #   students3 = [student1.username, student4.username, student5.username]
    #   team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
    #   comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 15)
      
    #   students4 = [student2.username, student3.username, student6.username]
    #   team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
    #   comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      
    #   # Update ratings and rankings for competition 2
    #   update_ratings(mod.username, comp2.name)
    #   update_rankings()
      
    #   # Assuming notifications are generated with IDs 1 and 7 for this setup
    #   notifications = display_notifications(1)
      
    #   # Expected structure for the notifications
    #   expected = [
    #       {"id": 1, "student_id": 1, "message": "RANK: 1. Congratulations on your first rank!"},
    #       {"id": 7, "student_id": 1, "message": "RANK: 1. Well done! You retained your rank."}
    #   ]
      
    









    #   # Check if the notifications match the expected output
    #   self.assertListEqual(notifications, expected)
    # def test3_display_notification(self):
    #   db.drop_all()
    #   db.create_all()
    #   mod = create_moderator("debra", "debrapass")
    #   comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
    #   comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
    #   student1 = create_student("james", "jamespass")
    #   student2 = create_student("steven", "stevenpass")
    #   student3 = create_student("emily", "emilypass")
    #   student4 = create_student("mark", "markpass")
    #   student5 = create_student("eric", "ericpass")
    #   student6 = create_student("ryan", "ryanpass")
    #   students1 = [student1.username, student2.username, student3.username]
    #   team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
    #   comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
    #   students2 = [student4.username, student5.username, student6.username]
    #   team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
    #   comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
    #   update_ratings(mod.username, comp1.name)
    #   update_rankings()
    #   students3 = [student1.username, student4.username, student5.username]
    #   team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
    #   comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
    #   students4 = [student2.username, student3.username, student6.username]
    #   team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
    #   comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
    #   update_ratings(mod.username, comp2.name)
    #   update_rankings()
    #   self.assertDictEqual(display_notifications("steven"), {"notifications": [{"ID": 2, "Notification": "RANK : 1. Congratulations on your first rank!"}, {"ID": 10, "Notification": "RANK : 4. Oh no! Your rank has went down."}]})

    # def test4_display_notification(self):
    #   db.drop_all()
    #   db.create_all()
    #   mod = create_moderator("debra", "debrapass")
    #   comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
    #   comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
    #   student1 = create_student("james", "jamespass")
    #   student2 = create_student("steven", "stevenpass")
    #   student3 = create_student("emily", "emilypass")
    #   student4 = create_student("mark", "markpass")
    #   student5 = create_student("eric", "ericpass")
    #   student6 = create_student("ryan", "ryanpass")
    #   students1 = [student1.username, student2.username, student3.username]
    #   team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
    #   comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
    #   students2 = [student4.username, student5.username, student6.username]
    #   team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
    #   comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
    #   update_ratings(mod.username, comp1.name)
    #   update_rankings()
    #   students3 = [student1.username, student4.username, student5.username]
    #   team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
    #   comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
    #   students4 = [student2.username, student3.username, student6.username]
    #   team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
    #   comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
    #   update_ratings(mod.username, comp2.name)
    #   update_rankings()
    #   self.assertDictEqual(display_notifications("mark"), {"notifications": [{"ID": 4, "Notification": "RANK : 4. Congratulations on your first rank!"}, {"ID": 8, "Notification": "RANK : 2. Congratulations! Your rank has went up."}]})

    #Additional Integration Tests
    
    #Added from new table
    def test_update_student_username(self):
    #  Set up initial database state
      db.drop_all()  # Drop all tables
      db.create_all()  # Create fresh tables
      student = create_student("original_username", "password")  # Create a student with original username

     
      updated_student = update_student(student.id, "new_username")  # Update the student's username
      
     
      # Fetch the student from the database again to check the username
      student_from_db = get_student(student.id)

      # Check that the student's username was updated
      self.assertIsNotNone(updated_student)  # Ensure the returned student is not None
      self.assertEqual(student_from_db.username, "new_username")  # Ensure the username was updated
      self.assertNotEqual(student_from_db.username, "original_username")  # Ensure the old username was replaced
      




    def test_get_all_students(self):
    # Set up initial database state
      db.drop_all()  # Drop all tables to start fresh
      db.create_all()  # Create fresh tables

      # Add students to the database
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")

     
      all_students = get_all_students()  # Retrieve all students from the database

     
      # Ensure the function returns a list of students
      self.assertEqual(len(all_students), 3)  # Ensure the correct number of students are returned

      # Ensure that the students' data is correct
      student_usernames = [student.username for student in all_students]
      self.assertIn("james", student_usernames)  # Check if 'james' is in the list
      self.assertIn("steven", student_usernames)  # Check if 'steven' is in the list
      self.assertIn("emily", student_usernames)  # Check if 'emily' is in the list

      # verify that the student objects have all expected attributes
      self.assertTrue(all(hasattr(student, 'id') and hasattr(student, 'username') for student in all_students))

    def test_update_student_rating(self):
  
      db.drop_all()  # Drop all tables to start fresh
      db.create_all()  # Create fresh tables

      # Add a student with an initial rating
      student = create_student("james", "jamespass")
      student.rating_score = 15  # Set an initial rating for the student
      db.session.commit()  # Commit the changes to the database


      # Update the student's rating
      new_rating = 25
      result = update_student_rating(student.id, new_rating)

    
      # Ensure the rating update was successful
      self.assertIsNotNone(result)  # Ensure the result is not None
      self.assertEqual(result['old_rating'], 15)  # Verify the old rating was 15
      self.assertEqual(result['updated_rating'], 25)  # Verify the updated rating is 25

      #  Verify if the student's rating has been updated in the database
      updated_student = get_student(student.id)  # Retrieve the student again from the database
      self.assertEqual(updated_student.rating_score, 25)  # Ensure the student's rating is updated


    def test_recalculate_rank(self):
      # Step 1: Set up initial database state
      db.drop_all()
      db.create_all()

      student1 = create_student("james", "jamespass")
      student1.rating_score = 30  # Highest rating
      student1.comp_count = 3

      student2 = create_student("steven", "stevenpass")
      student2.rating_score = 25  # Second highest rating
      student2.comp_count = 2

      student3 = create_student("emily", "emilypass")
      student3.rating_score = 20  # Third highest rating
      student3.comp_count = 4

      student4 = create_student("mark", "markpass")
      student4.rating_score = 15  # Lowest rating
      student4.comp_count = 1

      # Commit initial students to the database
      db.session.add_all([student1, student2, student3, student4])
      db.session.commit()

      # Call recalculate_rank to update ranks
      Student.recalculate_rank(self)

      
      # Retrieve the students again from the database
      updated_students = Student.query.order_by(Student.curr_rank).all()

      # Ensure the students are ranked correctly based on rating_score
      self.assertEqual(updated_students[0].username, "james")  # Rank 1
      self.assertEqual(updated_students[0].curr_rank, 1)

      self.assertEqual(updated_students[1].username, "steven")  # Rank 2
      self.assertEqual(updated_students[1].curr_rank, 2)

      self.assertEqual(updated_students[2].username, "emily")  # Rank 3
      self.assertEqual(updated_students[2].curr_rank, 3)

      self.assertEqual(updated_students[3].username, "mark")  # Rank 4
      self.assertEqual(updated_students[3].curr_rank, 4)

    def test_add_notification(self):
      
      db.drop_all()
      db.create_all()

      
      student = create_student("james", "jamespass")
      db.session.commit()

     
      # Create a notification and associate it with the student by passing student_id
      notification = Notification(message="You achieved a new rank!", student_id=student.id)
      db.session.add(notification)
      db.session.commit()

    
      # Retrieve the notification from the database
      retrieved_notification = Notification.query.first()
      
      # Ensure the notification is correctly created and associated with the student
      self.assertEqual(retrieved_notification.message, "You achieved a new rank!")
      
      # Compare both as strings or integers based on how the student ID is stored
      self.assertEqual(str(retrieved_notification.student_id), str(student.id))  # Ensures both are strings

    def test1_add_mod(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      assert add_mod(mod1.username, comp.name, mod2.username) != None
       


    
    def test2_add_mod(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      mod3 = create_moderator("raymond", "raymondpass")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      assert add_mod(mod2.username, comp.name, mod3.username) == None
    
    def test_student_list(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings()
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings()
      self.assertEqual(get_all_students_json(), [{'id': 1, 'username': 'james', 'rating_score': 22, 'comp_count': 2, 'curr_rank': 1}, {'id': 2, 'username': 'steven', 'rating_score': 17, 'comp_count': 2, 'curr_rank': 4}, {'id': 3, 'username': 'emily', 'rating_score': 17, 'comp_count': 2, 'curr_rank': 4}, {'id': 4, 'username': 'mark', 'rating_score': 18, 'comp_count': 2, 'curr_rank': 2}, {'id': 5, 'username': 'eric', 'rating_score': 18, 'comp_count': 2, 'curr_rank': 2}, {'id': 6, 'username': 'ryan', 'rating_score': 13, 'comp_count': 2, 'curr_rank': 6}])

    def test_comp_list(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings()
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings()
      self.assertListEqual(get_all_competitions_json(), [{"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}, {"id": 2, "name": "Hacker Cup", "date": "23-02-2024", "location": "Macoya", "level": 1, "max_score": 20, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}])
      