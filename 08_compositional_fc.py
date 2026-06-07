import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

#                     Compositional Function Handling (Chaining Multiple Functions)

"""
Suppose I want to set the thermostat temperature based on the location temperature
I will use two functions
One to get Location and its temperature
The other to set thermostat temperature
Both are chained because one func depend on other
The Gemini uses both in sequence
"""

def get_loc_temperature(location : str) -> dict:

    """
    It will take the location and give the temperature of that location
    """

    print(f"TOOL CALL: get_loc_temperature({location})")

    print("TOOL RESPONSE: {'temperature' : 25, 'Unit' : 'Celcius'}")

    return ({"temperature" : 25, "Unit" : "Celcius"})

def set_thermostat_temperature(temperature : int) -> dict:

    """
    It will set the tempearture of themostat. 
    """

    print(f"TOOL CALL: set_temperature_thermostat(temperature = {temperature})") 

    print("TOOL RESPONSE: {'status' : 'success}")


res = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents="We are in london. If temperature of it is above 25C set thermostat temperature 10C otherwise 30C",
    config= types.GenerateContentConfig(
        tools=[get_loc_temperature,set_thermostat_temperature]
    )
)

