import requests
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import ScoreboardV2
from datetime import datetime, timedelta

# Save origin request() of requests.Session
original_request = requests.Session.request


def custom_request(self, method, url, *args, **kwargs):
    headers = kwargs.pop("headers", {})
    headers["User-Agent"] = "Mozilla/5.0"
    kwargs["headers"] = headers
    return original_request(self, method, url, *args, **kwargs)

#
requests.Session.request = custom_request

def get_scoreboard_by_date(date_str):
    today = datetime.today()

    if date_str.lower() == "today":
        target_date = today
    elif date_str.lower() == "yesterday":
        target_date = today - timedelta(days=1)
    elif date_str.lower() == "tomorrow":
        target_date = today + timedelta(days=1)
    else:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")  
        except ValueError:
            print("Invalid date! Correct format is YYYY-MM-DD.")
            return

    formatted_date = target_date.strftime("%m/%d/%Y")  
    print(f"\nNBA Scores for {target_date.strftime('%Y-%m-%d')}:\n" + "-"*40)

    try:
        scoreboard_data = ScoreboardV2(game_date=formatted_date)
        # data = scoreboard_data.get_data_frames()  
        data = scoreboard_data.get_normalized_dict()
        games = data["GameHeader"]
        line_scores = data["LineScore"]
    except Exception as e:
        print("Failed to fetch data:", repr(e))
        return
    
    if not games:
        print("No games available.")
        return
    
    for game in games:
        if "HOME_TEAM_ABBREVIATION" not in game or "VISITOR_TEAM_ABBREVIATION" not in game:
            print("Incomplete data for one game!!!")
            continue

        game_id = game["GAME_ID"]
        home_team = game["HOME_TEAM_ABBREVIATION"]
        visitor_team = game["VISITOR_TEAM_ABBREVIATION"]
        game_status = game["GAME_STATUS_TEXT"]

        if not home_team or not visitor_team or not game_status:
            continue  

        home_score = next((line["PTS"] for line in line_scores if line["TEAM_ABBREVIATION"] == home_team and line["GAME_ID"] == game_id), "-")
        visitor_score = next((line["PTS"] for line in line_scores if line["TEAM_ABBREVIATION"] == visitor_team and line["GAME_ID"] == game_id), "-")

        print(f"{visitor_team} | {visitor_score} vs {home_team} | {home_score} --- [{game_status}]")

date_input = input("Enter the date (yesterday/today/tomorrow or YYYY-MM-DD): ")
get_scoreboard_by_date(date_input)
