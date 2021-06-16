from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
import datetime

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
        print(video_game)
        price = fetch_price(video_game)
        dispatcher.utter_template("utter_give_price", tracker, price=price, video_game=video_game)

        return []

class Get_Video_Game_Rate(Action):

    def name(self) -> Text:
        return "Get_Video_Game_Rate"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return []

class Get_Recommandation(Action):

    def name(self) -> Text:
        return "Get_Recommandation"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = tracker.current_state()["sender_id"]
        video_game = fetch_recommandation(user_id)

        dispatcher.utter_template("utter_give_recommandation", tracker, video_game=video_game)

        return []


class Get_Evaluation(Action):

    def name(self) -> Text:
        return "Get_Evaluation"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = tracker.current_state()["sender_id"]
        rate = tracker.latest_message['text']
        id_evaluated_game = fetch_id_game_recommandation(user_id)
        save_user_evaluation(id_evaluated_game, user_id, rate)

        dispatcher.utter_template("utter_happy", tracker)

        return []

def fetch_price(video_game):
    cur = db.cursor()
    cur.execute("SELECT price FROM steam_video_games WHERE name LIKE '%" + video_game +"%'")
    result = cur.fetchall()
    return float(result[0][0]) / 100

def fetch_recommandation(user_id):
    cur = db.cursor()
    cur.execute("SELECT name FROM steam_video_games WHERE id = (SELECT game_id FROM of_game_recommandation a WHERE of_user_id = "+ user_id + " AND a.game_id NOT IN (SELECT game_id FROM of_game_user_evaluation WHERE of_user_id = "+ user_id + ") ORDER BY date_create DESC LIMIT 1)")
    result = cur.fetchall()
    return result[0][0]

def fetch_id_game_recommandation(user_id):
    cur = db.cursor()
    cur.execute("SELECT game_id FROM of_game_recommandation a WHERE of_user_id = "+ user_id + " AND a.game_id NOT IN (SELECT game_id FROM of_game_user_evaluation WHERE of_user_id = "+ user_id + ") ORDER BY date_create DESC LIMIT 1")
    result = cur.fetchall()
    return result[0][0]

def save_user_evaluation(game_id, user_id, rate):
    date_create = datetime.datetime.now()
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO of_game_user_evaluation(of_user_id, game_id, rate, date_create) VALUES(" + str(user_id) + "," + str(game_id) + "," + str(rate) + ", '" + str(date_create) + "')")
        db.commit()
    except Exception as e:
        print(e)