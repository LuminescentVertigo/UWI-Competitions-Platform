from flask import *
from flask_login import current_user, login_required
from App.controllers import *
from App.models import Moderator

comp_views = Blueprint("comp_views", __name__, template_folder="../templates")

#Return the JSON list of competitions fetched from the database
@comp_views.route("/api/competitions", methods=["GET"])
def get_competitions_api():
    competitions = get_all_competitions_json()
    return jsonify(competitions), 200


#Add new competition to the database
@comp_views.route("/api/competitions", methods=["POST"])
@login_required
def create_competition_api():
    print(f"DEBUG: Current User: {current_user}, Session: {session.get('user_type')}")
    
    if session.get("user_type") != "moderator":
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    date = f"{data['date'][8:10]}-{data['date'][5:7]}-{data['date'][0:4]}"
    moderator = Moderator.query.filter_by(id=current_user.id).first()

    if not moderator:
        return jsonify({"error": f"Moderator {current_user.username} not found!"}), 404

    response = create_competition(
        moderator.username, data["name"], date, data["location"], data["level"], data["max_score"]
    )

    if response:
        return jsonify({"message": "Competition created successfully!"}), 201

    return jsonify({"error": "Error creating competition"}), 500

## Competition details (by ID)
@comp_views.route("/api/competitions/<int:id>", methods=["GET"])
def competition_details_api(id):
    competition = get_competition(id)
    if not competition:
        return jsonify({"error": "Competition not found"}), 404

    return jsonify(competition.toDict()), 200

## Confirm and finalize competition results
@comp_views.route("/confirm_results/<string:comp_name>", methods=["POST"])
@login_required
def confirm_results(comp_name):
    if session.get("user_type") != "moderator":
        return jsonify({"error": "Unauthorized access"}), 403

    competition = get_competition_by_name(comp_name)
    if not competition:
        return jsonify({"error": "Competition not found"}), 404

    moderator = Moderator.query.filter_by(id=current_user.id).first()
    if update_ratings(moderator.username, competition.name):
        update_rankings()  # Recalculate rankings and notify observers
        return jsonify({"message": "Results confirmed and rankings updated!"}), 200

    return jsonify({"error": "Failed to confirm results!"}), 500


## POSTMAN: Fetch competitions as JSON
@comp_views.route("/competitions_postman", methods=["GET"])
def get_competitions_postman():
    competitions = get_all_competitions_json()
    return jsonify(competitions), 200


## POSTMAN: Create a new competition
@comp_views.route("/createcompetition_postman", methods=["POST"])
def create_comp_postman():
    data = request.json
    response = create_competition(
        "robert",
        data["name"],
        data["date"],
        data["location"],
        data["level"],
        data["max_score"],
    )
    if response:
        return jsonify({"message": "Competition created!"}), 201
    return jsonify({"error": "Error creating competition"}), 500


## POSTMAN: Get competition details
@comp_views.route("/competitions_postman/<int:id>", methods=["GET"])
def competition_details_postman(id):
    competition = get_competition(id)
    if not competition:
        return jsonify({"error": "Competition not found"}), 404

    return jsonify(competition.toDict()), 200


#Add competition results
@comp_views.route("/add_results_postman/<string:comp_name>", methods=["POST"])
def add_competition_results_postman(comp_name):
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    if session.get("user_type") != "moderator":
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        # Debug current user information
        print(f"DEBUG: Current User: {current_user.username}, ID: {current_user.id}")

        # Ensure the logged-in user is the moderator
        moderator = Moderator.query.filter_by(id=current_user.id).first()
        if not moderator:
            return jsonify({"error": f"Moderator {current_user.username} not found!"}), 404

        # Debug competition information
        print(f"DEBUG: Competition Name: {comp_name}")

        # Verify the competition exists
        competition = get_competition_by_name(comp_name)
        if not competition:
            return jsonify({"error": f"Competition {comp_name} not found!"}), 404

        # Check if the current moderator is associated with the competition
        if moderator not in competition.moderators:
            return jsonify({"error": f"Moderator {moderator.username} is not authorized to add results for {comp_name}!"}), 403

        data = request.json
        required_fields = ["student1", "student2", "student3", "team_name", "score"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        students = [data["student1"], data["student2"], data["student3"]]
        print(f"DEBUG: Students: {students}")

        # Add the team
        team_response = add_team(moderator.username, comp_name, data["team_name"], students)
        if not team_response:
            return jsonify({"error": "Failed to add team"}), 500

        # Add the results
        result_response = add_results(moderator.username, comp_name, data["team_name"], int(data["score"]))
        if not result_response:
            return jsonify({"error": "Failed to add results"}), 500

        # Update rankings after results
        update_rankings()

        return jsonify({"message": "Results added and rankings updated!"}), 201
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": f"Error occurred: {str(e)}"}), 500




@comp_views.route("/api/competitions/<string:comp_name>/results", methods=["POST"])
@login_required
def add_results_api(comp_name):
    if session.get("user_type") != "moderator":
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    students = [data["student1"], data["student2"], data["student3"]]
    response = add_team(current_user.username, comp_name, data["team_name"], students)

    if response:
        response = add_results(current_user.username, comp_name, data["team_name"], int(data["score"]))
        if response:
            update_rankings()
            return jsonify({"message": "Results added and rankings updated!"}), 201

    return jsonify({"error": "Error adding results!"}), 500
