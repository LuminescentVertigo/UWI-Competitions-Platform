Competitions Platform CLI system:

Instructions for Using CLI Commands
To interact with the project through the command line interface (CLI), the following instructions outline the available commands and their usage for managing students, moderators, competitions, and notifications.

Install Required Dependencies:
pip install -r requirements.txt


CLI Commands Overview

Initialization and Database Setup

Initialize the Database:
This command will drop the existing database, recreate it, and load data from the CSV files (students.csv, moderators.csv, competitions.csv, results.csv).
Command: flask init
Result: The database will be reset, and rankings will be recalculated.


Student Commands
Create a Student:

This command will create a new student.
flask student create <username> <password>
Example: flask student create stud1 stud1pass

Update a Student’s Username:

This command allows you to update a student’s username.
flask student update <student_id> <new_username>
Example: flask student update 1 stud_new


List All Students:

This command will list all students in the database.
flask student list <string|json>
Example: flask student list string


Display Student Profile:

This command displays the profile of a student based on their ID.
flask student display <studentID>
Example: flask student display 1

Display Student Notifications:

This command retrieves all notifications for a student by their ID.
flask student notifications <studentID>
Example: flask student notifications 1


Moderator Commands

Create a Moderator:

This command creates a new moderator.
flask mod create <username><password>
Example: flask mod create mod1 mod1pass

Add Moderator to Competition:

This command adds a moderator to a competition.
flask mod addMod <moderator1> <competition_name> <moderator2>
Example: flask mod addMod  mod1 comp1 mod2


Add Results to a Competition:

This command adds results for a team in a competition.
flask mod addResults <moderator_name> <competition_name> <team_name> <student1> <student2> <student3> <score>
Example: flask mod addResults mod1 comp1 team1 stud1 stud2 stud3 10


Confirm Results and Update Rankings:

This command confirms the results and updates the rankings.
flask mod confirm <moderator_name> <competition_name>
Example: flask mod confirm mod1 comp1


Display Overall Rankings:

This command displays the overall rankings of all students.
flask mod rankings
Example: flask mod rankings


List All Moderators:

This command lists all moderators in the database.
flask mod list <string|json>
Example: flask mod list string


Competition Commands

Create a Competition:

This command creates a new competition.
flask comp create <moderator_name> <competition_name> <date> <location> <level> <max_score>
Example: flask comp create mod1 comp1 09-02-2024 CSL 1 25


Display Competition Details:

This command displays details of a competition.
flask comp details <competition_name>
Example: flask comp details comp1


List All Competitions:

This command lists all competitions in the database.
flask comp list
Example: flask comp list


Display Competition Results:

This command displays the results of a competition.
flask comp results <competition_name>
Example: flask comp results comp1


Notification Commands

Add a Notification:

This command adds a notification for a student.
flask notification add <student_id> <message>
Example: flask notification add 1 "RANK: 1. Congratulations on your first rank!"


View All Notifications for a Student:

This command retrieves all notifications for a student by their ID.
flask notification view <student_id>
Example: flask notification view 1

Rank Update Notification:

This command sends a notification regarding a student's rank update.
flask notification rank-update <student_id> <old_rank> <new_rank>
Example: flask notification rank-update 1 2 1


Test Commands

Run Tests:
flask test app <unit|int|all>
Example: flask test app all

