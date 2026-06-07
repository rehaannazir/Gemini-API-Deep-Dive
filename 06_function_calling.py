#                                                            Function Calling
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# Basic way to call function

def weather(city : str):

    print(f"The weather in {city} is Sunny, 35°C")

weather_tool = { # Above function description: In this case we don't need them

    "name ": "weather",
    "descrition" : "Tells the weather of the given city",

    "parameters" : {

        "type" : "object",
        
        "properties" : {
            
            "city" : {

                "type" : "string",
                "description" : "The name of the the given city"
            }
        }

    },
    "required" : ["city"]
}

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = "Give me the weather of Lahore",
    config = {
        "tools" : [weather]
    }
)


# Advanced Weather Function Decalaration


weather_declaration = {
    "name" : "weather_tool",
    "description" : "Tells the weather of a given city",

    "parameters" : {
        "type" : "object",

        "properties" : {

            "city" : {
                "type" : "string",
                "description" : "The name of the given city"
            }
        },
        "required" : ["city"]
    }
}

tool = types.Tool(function_declarations=[weather_declaration])
config = types.GenerateContentConfig(
    tools=[tool],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="ANY",
            allowed_function_names=["weather_tool"]
        )
    )
)

resposne = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = "Tell me the weather of Lahore by using function declaration",
    config = config
)

# Checking if function call used or not

if response.candidates[0].content.parts[0].function_call:

    function_call = response.candidates[0].content.parts[0].function_call

    print("Function Call Name: ",function_call.name)
    print("Function Call Argument(s): ",function_call.args)
    print("Function Call ID: ",function_call.id)

else:
    print("Function Call is not used")
    print(response.text)


