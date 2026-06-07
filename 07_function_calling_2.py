#                       Function Calling (Part 2)

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import base64

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# Creating a Bar chart

chart_decalaration = {
    "name" : "chart_formation",
    "description" : "Create the bar chart by using the given terms title, labels, values",

    "parameters" : {

        "type" : "object",

        "properties" : {
            "title" : {
                "type" : "string",
                "description" : "It gives the title of the bar chart."
            },
            "labels" : {
                "type" : "array",
                "items" : {"type" : "string"},
                "description" : "It gives the list varaibles used as labels for axis. (e.g. Q1 Q2 Q3)"
            },
            "values" : {
               "type" : "array",
                "items" : {"type" : "string"},
                "description" : "It gives the list numerical values on the given axis (e.g. on x-axis 5 10 15 20 50)"
            }
        },
        "required" : ["title", "labels", "values"]
    }
}

tool = types.Tool(function_declarations=[chart_decalaration])
config = types.GenerateContentConfig(
    tools=[tool],
    thinking_config = types.ThinkingConfig(thinking_level="medium")
)

response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents = "Construct a Random of your choice bar chart of Sales Analysis as title.With the values on x axis as name of products and on y axis price range. It shows comparison of total sales of different random products of your choice",
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

# After using thinking , we can ensure that: 

part = response.candidates[0].content.parts[0]
if part.thought_signature:
  print(base64.b64encode(part.thought_signature).decode("utf-8"))