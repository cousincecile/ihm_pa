from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2

POSTGRES = {
    'user': 'of_dck',
    'pw': 'gft78kP9!luY!',
    'db': 'onlyfeed',
    'host': 'onlyfeed.ddns.net',
    'port': '5432',
}

db = psycopg2.connect( host=POSTGRES['host'], user=POSTGRES['user'], password=POSTGRES['pw'], dbname=POSTGRES['db'])


class Get_Video_Game_Price(Action):

    def name(self) -> Text:
        return "Get_Video_Game_Price"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        video_game = tracker.get_slot("video_game")
        price = fetch_price(video_game)
        print(price)
        dispatcher.utter_template("utter_give_price", tracker, price=price, video_game=video_game)

        return []

class Get_Video_Game_Rate(Action):

    def name(self) -> Text:
        return "Get_Video_Game_Rate"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        video_game = tracker.get_slot("video_game")
        rate = fetch_rate(video_game)
        dispatcher.utter_template("utter_give_rate", tracker, price=price, video_game=video_game)

        return []


def fetch_price(video_game):

    cur = db.cursor()
    cur.execute("SELECT price FROM steam_video_games WHERE name LIKE '%" + video_game +"%'")
    result = cur.fetchall()
    return result[0][0]

def fetch_rate(video_game):

    cur = db.cursor()
    cur.execute("SELECT rate FROM of_game_analysis WHERE id_game = (SELECT id FROM steam_video_games WHERE name LIKE '%" + video_game +"%' LIMIT 1)")
    result = cur.fetchall()
    return result

print(fetch_rate("Skyrim"))