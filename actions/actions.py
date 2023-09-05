import json
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from unidecode import unidecode
import mysql.connector

class ValidateJobsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_jobs_form"
    
    ALLOWD_CONTRACTS_TYPES = ["cdd", "cdi", "Stage", "contrat a duree determinee", "contrat a duree indeterminee", "stage"]
    
    ALLOWED_VIllES = [
        "tunis", "tunisie", "tunisien",
        "ariana", "aryanah", "aryana", "arianna",
        "ben arous", "benarous", "bin arus", "benaros",
        "manouba", "manoubah", "manoba", "manouva",
        "nabeul", "nabul", "naboul", "nabol",
        "zaghouan", "zagouane", "zagwan", "zagouen",
        "bizerte", "bizert", "bizertee", "bizart", "binzart",
        "beja", "bija", "bejaa", "bejia",
        "jendouba", "jandouba", "jendoubeh", "jandoubeh", "jandoube", "jendoube",
        "le kef", "kef", "lkef", "lkeff", "el kef", "el keff", "elkef", "elkeff",
        "siliana", "silyana", "silyanna", "silianah",
        "kairouan", "kayrouane", "kayrouan", "kyrwan",
        "kasserine", "kacrine", "kacerine", "kacirine",
        "sidi bouzid", "sidi bouzide", "sidi bou zid", "sidi buzid", "sidibouzid",
        "sousse", "souss", "souese", "souece", "soussa", "sousa", "souse",
        "monastir", "monastire", "monaster", "monastere",
        "mahdia", "mahdiya", "mahdya", "mahdiah", "mehdia",
        "sfax", "sfaxe", "sfaks", "sfaqs",
        "gafsa", "gafsah", "gafsaa", "gafca",
        "tozeur", "tozeure", "tozor", "tozoor", "tozer",
        "kebili", "kebilli", "kebily", "kebilye",
        "gabes", "gabs", "gabse", "gabse",
        "medenine", "medenine", "mdenine", "mdenin",
        "tataouine", "tataouin", "tataoueen", "tatwane"
    ]
    
    ALLOWED_DIPLOMAS = ["bacalaureat", "bac", "bachelor", "licence", "master", "ingenieur","ingenieurie", "doctorat", "doctorant",
                        "bts", "brevet de technicien superieur", "cap", "certificat d aptitude professionnelle", "certificat aptitude professionnelle"]
    
    
    METIER_SKILLS = {
        "developpeur web": ["Front-end (HTML, CSS, JavaScript)", "Frameworks (React, Angular)", "Back-end (Node.js, Python)", "Bases de données", "Conception Web"],
        "developpeur logiciel": ["Programmation (C++, Java, Python)", "Algorithmes", "Débogage", "Conception logicielle", "Collaboration d'équipe"],
        "ingenieur devops": ["Automatisation (CI/CD)", "Infrastructure as Code", "Conteneurisation (Docker, Kubernetes)", "Gestion de systèmes", "Sécurité"],
        "administrateur système": ["Gestion de serveurs", "Réseaux", "Sécurité informatique", "Dépannage", "Scripting (Bash, PowerShell)"],
        "analyste en cybersécurité": ["Sécurité des systèmes", "Cryptographie", "Détection d'intrusions", "Gestion des vulnérabilités", "Conformité"],
        "data scientist": ["Analyse de données", "Machine Learning", "Statistiques", "Programmation (Python, R)", "Visualisation de données"],
        "ingenieur réseau": ["Conception de réseaux", "Routage, Commutation", "Protocoles réseau", "Sécurité réseau"],
        "architecte cloud": ["Services Cloud (AWS, Azure, GCP)", "Architecture distribuée", "Sécurité Cloud", "Gestion des coûts"],
        "ux/ui designer": ["Conception d'interfaces utilisateur", "Expérience utilisateur", "Wireframing", "Prototypage", "Design visuel"],
        "analyste de données": ["Extraction et transformation de données (ETL)", "SQL", "Visualisation de données", "Analyse statistique"]
    }

    def validate_slot_type_contrat(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if unidecode(slot_value.lower()) in self.ALLOWD_CONTRACTS_TYPES:            
            if unidecode(slot_value.lower()) in ["cdd", "contrat a duree determinee"]:
                slot_value = "CDD"
            elif unidecode(slot_value.lower()) in ["cdi", "contrat a duree indeterminee"]:
                slot_value = "CDI"   
            elif unidecode(slot_value.lower()) == "stage":
                slot_value = "Stage"      
            return {"slot_type_contrat": slot_value}  
        else:
            dispatcher.utter_message(text=f"Désolé, le type de contrat '{slot_value}' n'est pas valide. Veuillez choisir parmi CDI, CDD ou stage.") 
            return {"slot_type_contrat": None}
        
    def validate_slot_ville(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if unidecode(slot_value.lower()) in self.ALLOWED_VIllES:
            if unidecode(slot_value.lower()) in ["tunis", "tunisie", "tunisien"]:
                slot_value = "Tunis"
            elif unidecode(slot_value.lower()) in ["ariana", "aryanah", "ariyana", "arianna"]:
                slot_value = "Ariana"
            elif unidecode(slot_value.lower()) in ["ben arous", "benarous", "bin arus", "benaros"]:
                slot_value = "Ben Arous"
            elif unidecode(slot_value.lower()) in ["manouba", "manoubah", "manoba", "manouva"]:
                slot_value = "Manouba"
            elif unidecode(slot_value.lower()) in ["nabeul", "nabul", "naboul", "nabol"]:
                slot_value = "Nabeul"
            elif unidecode(slot_value.lower()) in ["zaghouan", "zagouane", "zagwan", "zagouen"]:
                slot_value = "Zaghouan"
            elif unidecode(slot_value.lower()) in ["bizerte", "bizert", "bizertee", "bizart", "binzart"]: 
                slot_value = "Bizerte"
            elif unidecode(slot_value.lower()) in ["beja", "bija", "bejaa", "bejia"]:
                slot_value = "Béja"
            elif unidecode(slot_value.lower()) in ["jendouba", "jandouba", "jendoubeh", "jandoubeh", "jandoube", "jendoube"]:
                slot_value = "Jendouba"
            elif unidecode(slot_value.lower()) in ["le kef", "kef", "lkef", "lkeff", "el kef", "el keff", "elkef", "elkeff"]:
                slot_value = "Le Kef"
            elif unidecode(slot_value.lower()) in ["siliana", "silyana", "silyanna", "silianah"]:
                slot_value = "Siliana"
            elif unidecode(slot_value.lower()) in ["kairouan", "kayrouane", "kayrouan", "kyrwan"]:
                slot_value = "Kairouan"
            elif unidecode(slot_value.lower()) in ["kasserine", "kacrine", "kacérine", "kacirine"]:
                slot_value = "Kasserine"
            elif unidecode(slot_value.lower()) in ["sidi bouzid", "sidi bouzide", "sidi bou zid", "sidi buzid", "sidibouzid"]:
                slot_value = "Sidi Bouzid"
            elif unidecode(slot_value.lower()) in ["sousse", "souss", "souese", "souece", "soussa", "sousa", "souse"]:
                slot_value = "Sousse"
            elif unidecode(slot_value.lower()) in ["monastir", "monastire", "monaster", "monastere"]:
                slot_value = "Monastir"
            elif unidecode(slot_value.lower()) in ["mahdia", "mahdiya", "mahdya", "mahdiah", "mehdia"]:
                slot_value = "Mahdia"
            elif unidecode(slot_value.lower()) in ["sfax", "sfaxe", "sfaks", "sfaqs", "sfaxes", "sfakse", "sfakse", "sfakse"]:
                slot_value = "Sfax"
            elif unidecode(slot_value.lower()) in ["gafsa", "gafsah", "gafsaa", "gafca"]:
                slot_value = "Gafsa"
            elif unidecode(slot_value.lower()) in ["tozeur", "tozeure", "tozor", "tozoor", "tozer"]:
                slot_value = "Tozeur"
            elif unidecode(slot_value.lower()) in ["kebili", "kebilli", "kebily", "kebilye"]:
                slot_value = "Kebili"
            elif unidecode(slot_value.lower()) in ["gabes", "gabs", "gabse", "gabse"]:
                slot_value = "Gabès"
            elif unidecode(slot_value.lower()) in ["medenine", "medenine", "mdenine", "mdenin"]:
                slot_value = "Medenine"
            elif unidecode(slot_value.lower()) in ["tataouine", "tataouin", "tataoueen", "tatwane"]:
                slot_value = "Tataouine"
            return {"slot_ville": slot_value}
        else:
            dispatcher.utter_message(text=f"Désolé, la ville '{slot_value}' n'est pas valide. Veuillez choisir parmi les 24 gouvernorats de la Tunisie.")
            return {"slot_ville": None}

    def validate_slot_salaire_minimum(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            # Convertir la valeur du slot en un nombre décimal (float)
            salaire_minimum = float(slot_value)
            if salaire_minimum >= 0:
                return {"slot_salaire_minimum": salaire_minimum}
            else:
                dispatcher.utter_message(text="Le salaire minimum doit être supérieur ou égal à 0.")
                return {"slot_salaire_minimum": None}
        except ValueError:
            # Si la valeur n'est pas un nombre valide, envoyer un message d'erreur
            dispatcher.utter_message(text="Veuillez entrer un montant de salaire valide (chiffres uniquement).")
            return {"slot_salaire_minimum": None}
        
    def validate_slot_diplome(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if unidecode(slot_value.lower()) in self.ALLOWED_DIPLOMAS:
            if unidecode(slot_value.lower()) in ["bacalaureat", "bac", "bachelor"]:
                slot_value = "Bacalaureat"
            elif unidecode(slot_value.lower()) in ["licence"]:
                slot_value = "Licence"
            elif unidecode(slot_value.lower()) in ["master"]:
                slot_value = "Master"
            elif unidecode(slot_value.lower()) in ["ingenieur", "ingenieurie"]:
                slot_value = "Ingenieur"
            elif unidecode(slot_value.lower()) in ["doctorat", "doctorant"]:
                slot_value = "Doctorat"
            elif unidecode(slot_value.lower()) in ["bts", "brevet de technicien superieur"]:
                slot_value = "BTS"
            elif unidecode(slot_value.lower()) in ["cap", "certificat d aptitude professionnelle", "certificat aptitude professionnelle"]:
                slot_value = "CAP"
            return {"slot_diplome": slot_value}
        else:
            dispatcher.utter_message(text=f"Désolé, le diplôme '{slot_value}' n'est pas valide. Veuillez choisir parmi Bacalaureat, Licence, Master, Ingenieur ou Doctorat.")
            return {"slot_diplome": None}     

    def validate_slot_experience(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            experience_years = int(slot_value)
            if experience_years >= 0:
                return {"slot_experience": experience_years}
            else:
                dispatcher.utter_message(text="L'expérience ne peut pas être négative. Veuillez entrer un nombre positif ou zéro.")
                return {"slot_experience": None}
        except ValueError:
            dispatcher.utter_message(text="Veuillez entrer un nombre valide pour l'expérience (entier positif).")
            return {"slot_experience": None}
        
    
    def validate_slot_metier(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if unidecode(slot_value.lower()) in self.METIER_SKILLS:    
            skills = self.METIER_SKILLS[unidecode(slot_value.lower())]  
            skill_buttons = [{"title": skill, "payload": f'/inform{{"skills":"{skill}"}}'} for skill in skills]
            dispatcher.utter_message(text=f"Quelles compétences avez-vous pour {slot_value} ? Sélectionnez parmi les options ci-dessous :", buttons=skill_buttons)
            slot_skills = tracker.get_slot("slot_skills") or []  # Utilisation de tracker.get_slot pour obtenir la liste existante
            slot_skills.append(slot_value)  # Ajouter la compétence actuelle à la liste   
                 
        return {"slot_metier": slot_value}


class ActionGetJobOffers(Action):
    def name(self) -> Text:
        return "action_get_job_offers"

    def rank_offers(self, offers: List[Dict[Text, Any]], user_criteria: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ranked_offers = sorted(offers, key=lambda offer: self.calculate_relevance(offer, user_criteria), reverse=True)
        return ranked_offers

    def calculate_relevance(self, offer: Dict[Text, Any], user_criteria: Dict[Text, Any]) -> float:
        relevance = 0.0
        
        if offer['metier'] == user_criteria['metier']:
            relevance += 1.5
            
        if offer['ville'] == user_criteria['ville']:
            relevance += 1.0

        if offer['type_contrat'] == user_criteria['type_contrat']:
            relevance += 0.5
            
        if offer['diplome'] == user_criteria['diplome']:
            relevance += 0.5
            
        if offer['skills'] == user_criteria['skills']:
            relevance += 0.3

        if offer['experience'] >= user_criteria['experience']:
            relevance += 0.3 * (offer['experience'] - user_criteria['experience']) / 10.0
        
        return relevance
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Récupérer les valeurs des slots depuis le tracker
        user_criteria = {
            "ville": tracker.get_slot("slot_ville"),
            "type_contrat": tracker.get_slot("slot_type_contrat"),
            "metier": tracker.get_slot("slot_metier"),
            "diplome": tracker.get_slot("slot_diplome"),
            "experience": tracker.get_slot("slot_experience"),
            "skills": tracker.get_slot("slot_skills"), 
        }

        # Établir une connexion à la base de données
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="jobs_offres"
        )

        # Construire et exécuter la requête SQL pour récupérer les annonces pertinentes
        query = (
            "SELECT * FROM Annonce WHERE "
            "ville = %s AND "
            "type_contrat = %s AND "
            "metier = %s AND "
            "diplome = %s AND "
            "experience >= %s AND "
            "skills = %s "
        )
        values = (
            user_criteria['ville'],
            user_criteria['type_contrat'],
            user_criteria['metier'],
            user_criteria['diplome'],
            user_criteria['experience'],
            ", ".join(user_criteria['skills'])
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, values)
        job_offers = cursor.fetchall()

        # Fermer la connexion à la base de données
        cursor.close()
        connection.close()

        # Convertir les dates en chaînes de caractères
        for offer in job_offers:
            offer['date_offre'] = offer['date_offre'].strftime('%Y-%m-%d')

        # Classer les offres par pertinence
        ranked_offers = self.rank_offers(job_offers, user_criteria)

        # Enregistrer les offres d'emploi dans un fichier JSON
        with open('Chatbot-UI/job_offers.json', 'w') as file:
            json.dump(ranked_offers, file, indent=4)
        
        # Traiter les résultats et envoyer une réponse au chatbot
        if ranked_offers:
            dispatcher.utter_message(text="Voici quelques offres d'emploi correspondant à vos critères :", attachment="http://localhost:8000/Chatbot-UI/web_offers.html")
        else:
            dispatcher.utter_message(text="Aucune offre d'emploi ne correspond à vos critères.")
        
        return []

class ActionRestart(Action):
    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="D'accord, veuillez ressaisir les informations nécessaires.")
        return [SlotSet("requested_slot", None), SlotSet("slot_diplome", None), SlotSet("slot_metier", None), SlotSet("slot_skills", None), SlotSet("slot_experience", None), SlotSet("slot_type_contrat", None), SlotSet("slot_pays", None), SlotSet("slot_ville", None), SlotSet("slot_salaire_minimum", None)]
  
class ActionStart(Action):
    def name(self):
        return "action_session_start"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_salutation")
        return [SlotSet("requested_slot", None), SlotSet("slot_diplome", None), SlotSet("slot_metier", None), SlotSet("slot_skills", None), SlotSet("slot_experience", None), SlotSet("slot_type_contrat", None), SlotSet("slot_pays", None), SlotSet("slot_ville", None), SlotSet("slot_salaire_minimum", None)]
  