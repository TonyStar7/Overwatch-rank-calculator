import requests
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_URL = "https://overfast-api.tekrop.fr"
IMG_DIR = os.path.join(project_root, "assets")
TANK_IMG_URL = "https://static.playoverwatch.com/img/pages/career/icons/role/tank-f64702b684.svg#icon"
TANK_FILE = os.path.join(IMG_DIR, "tank.jpeg")


def get_ow_player_data(player_id):
        url =f"{BASE_URL}/players/{player_id}/summary"  #Access Player Summary
        response = requests.get(url)

        if response.status_code == 200:
            print(f"fetch successful for {player_id}")
            player_data = response.json()               #Convert to JSON data
            return player_data
        else:
            print(f"Problem accessing API, status code: {response.status_code}")



def rank_info(player_data, role):
        try:
            rank_data = player_data["competitive"]["pc"][role]
            if rank_data and rank_data.get("division"):
                return f"{rank_data["division"].upper()} {rank_data["tier"]}"
            else:
                return "UNRANKED"
        except KeyError:
            return "PRIVATE"
        
