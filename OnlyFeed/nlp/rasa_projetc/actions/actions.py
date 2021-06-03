from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class Get_Video_Game_Price(Action):

    def name(self) -> Text:
        return "Get_Video_Game_Price"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_give_price", tracker, price="10")

        return []
