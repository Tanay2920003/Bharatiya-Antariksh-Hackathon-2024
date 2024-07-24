# Import the necessary libraries
from geopy.geocoders import Nominatim
import spacy


# Function to extract cities from a given text
def extract_cities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    geolocator = Nominatim(user_agent="geoapiExercises")

    cities = []
    for ent in doc.ents:
        if ent.label_ == "GPE":
            location = geolocator.geocode(ent.text)
            if location:
                cities.append(ent.text)
    return cities


# Example usage
text = "I have visited New York, Los Angeles, and Chicago."
cities = extract_cities(text)
print("Cities found:", cities)

# Confirm installation and functionality
print("Successfully installed and imported geopy and spacy!")
