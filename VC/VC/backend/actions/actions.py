import requests
import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from geopy.geocoders import Nominatim
from datetime import datetime

class ActionGetLocation(Action):
    """Detect the user's location using their IP address or other methods"""
    def name(self) -> Text:
        return "action_get_location"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # replace with an actual API
        geolocator = Nominatim(user_agent="travel_assistant")
        location = geolocator.geocode("New York, USA")          
        if location:
            dispatcher.utter_message(text=f"Your location has been detected as: {location.address}")
            return [SlotSet("location", location.address)]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't detect your location. Please try again.")
            return []

class ActionGetWeather(Action):
    """Fetch the current weather based on the detected location"""
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        
        if location:
            # weather  API here
            weather_data = self.get_weather(location)
            if weather_data:
                weather_info = f"The current weather in {location} is {weather_data['weather']} with a temperature of {weather_data['temp']}°C."
                dispatcher.utter_message(text=weather_info)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the weather information.")
        else:
            dispatcher.utter_message(text="Please allow me to detect your location first.")
        
        return []

    def get_weather(self, location: str) -> dict:
        # demo weather data
        return {
            "weather": "sunny",
            "temp": random.randint(20, 30)
        }

class ActionGetNearbyPlaces(Action):
    """Fetch nearby hotels and tourist places based on the detected location"""
    def name(self) -> Text:
        return "action_get_nearby_places"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot("location")
        
        if location:
            # Fetch places API
            places_data = self.get_nearby_places(location)
            if places_data:
                hotels = places_data.get("hotels", [])
                tourist_spots = places_data.get("tourist_spots", [])
                
                if hotels:
                    hotel_list = "\n".join(hotels)
                    dispatcher.utter_message(text=f"Here are some nearby hotels in {location}:\n{hotel_list}")
                else:
                    dispatcher.utter_message(text="Sorry, no hotels found nearby.")
                
                if tourist_spots:
                    spots_list = "\n".join(tourist_spots)
                    dispatcher.utter_message(text=f"Here are some nearby tourist spots in {location}:\n{spots_list}")
                else:
                    dispatcher.utter_message(text="Sorry, no tourist spots found nearby.")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the places information.")
        else:
            dispatcher.utter_message(text="Please allow me to detect your location first.")
        
        return []

    def get_nearby_places(self, location: str) -> dict:
        # Mock data for nearby places ,(replace with real API data)
        return {
            "hotels": ["Hotel A", "Hotel B", "Hotel C"],
            "tourist_spots": ["Museum X", "Park Y", "Beach Z"]
        }

class ActionPlanDaySchedule(Action):
    """Generate a personalized day schedule based on user preferences"""
    def name(self) -> Text:
        return "action_plan_day_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        
        if location:
            # Plan the schedule 
            schedule = self.generate_day_schedule(location)
            if schedule:
                dispatcher.utter_message(text="Here is your personalized day schedule:\n" + "\n".join(schedule))
            else:
                dispatcher.utter_message(text="Sorry, I couldn't plan your schedule.")
        else:
            dispatcher.utter_message(text="Please allow me to detect your location first.")
        
        return []

    def generate_day_schedule(self, location: str) -> List[str]:
        # Mock schedule generation
        schedule = [
            f"8:00 AM - Breakfast at your hotel in {location}",
            f"9:30 AM - Visit Museum X",
            f"12:00 PM - Lunch at a local restaurant",
            f"2:00 PM - Visit Park Y",
            f"5:00 PM - Relax at Beach Z",
            f"7:00 PM - Dinner at a restaurant in {location}",
            f"9:00 PM - Free time or local sightseeing"
        ]
        return schedule

class ActionProvideTouristInfo(Action):
    """Provide general information about a tourist destination"""
    def name(self) -> Text:
        return "action_provide_tourist_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot("location")
        
        if location:
            # Fetch tourist info (mock data for now)
            tourist_info = self.get_tourist_info(location)
            dispatcher.utter_message(text=tourist_info)
        else:
            dispatcher.utter_message(text="Please allow me to detect your location first.")
        
        return []

    def get_tourist_info(self, location: str) -> str:
        # Mock tourist information
        return f"{location} is known for its rich culture, historic landmarks, and vibrant lifestyle. It has several must-see spots including famous museums, parks, and beaches."

