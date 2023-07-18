# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction

class AfficherLocalisationsAction(Action):
    def name(self) -> Text:
        return "afficher_localisations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        locations = [
            "Ariana", "Beja", "Ben Arous", "Bizerte", "Gabes", "Gafsa", "Jendouba", "Kairouan", "Kasserine",
            "Kebili", "Le Kef", "Mahdia", "Manouba", "Medenine", "Monastir", "Nabeul", "Sfax", "Sidi Bouzid",
            "Siliana", "Sousse", "Tataouine", "Tozeur", "Tunis", "Zaghouan"
        ]

        buttons = []
        for location in locations:
            payload = f"/choisir_localisation{{'location': '{location}'}}"
            button = {"title": location, "payload": payload}
            buttons.append(button)
        
        dispatcher.utter_message(
            text="Dans quelle localisation souhaitez-vous chercher des offres d'emploi ?",
            buttons=buttons
        )

        return []

class ChoisirLocalisationAction(Action):
    def name(self) -> Text:
        return "choisir_localisation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.latest_message.get('payload').get('location')
        dispatcher.utter_message(text=f"Vous avez choisi la localisation {location}.")

        return [SlotSet("location", location)]
