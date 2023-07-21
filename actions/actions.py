from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, Form

class ValidateEmploiForm(Action):
    def name(self) -> Text:
        return "emploi_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        required_slots = ["slot_location", "slot_type_contrat", "slot_domaine_emploi"]
        missing_slots = []

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                missing_slots.append(slot_name)

        if len(missing_slots) > 0:
            if "slot_salaire_minimum" in missing_slots or "slot_salaire_maximum" in missing_slots:
                # Au moins l'un des slots de salaire est manquant
                if "slot_salaire_minimum" not in missing_slots:
                    missing_slots.remove("slot_salaire_maximum")
                elif "slot_salaire_maximum" not in missing_slots:
                    missing_slots.remove("slot_salaire_minimum")

            # Répéter la question manquante
            dispatcher.utter_message(template=f"utter_demande_{missing_slots[0]}")
            return [SlotSet("requested_slot", missing_slots[0])]

        return [Form("emploi_form"), SlotSet("requested_slot", None)]