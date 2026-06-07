import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

#                   Parallel 

power_disco_ball = {
    "name": "power_disco_ball",
    "description": "Powers the spinning disco ball.",
    "parameters": {
        "type": "object",
        "properties": {
            "power": {
                "type": "boolean",
                "description": "Whether to turn the disco ball on or off.",
            }
        },
        "required": ["power"],
    },
}

start_music = {
    "name": "start_music",
    "description": "Play some music matching the specified parameters.",
    "parameters": {
        "type": "object",
        "properties": {
            "energetic": {
                "type": "boolean",
                "description": "Whether the music is energetic or not.",
            },
            "loud": {
                "type": "boolean",
                "description": "Whether the music is loud or not.",
            },
        },
        "required": ["energetic", "loud"],
    },
}

dim_lights = {
    "name": "dim_lights",
    "description": "Dim the lights.",
    "parameters": {
        "type": "object",
        "properties": {
            "brightness": {
                "type": "number",
                "description": "The brightness of the lights, 0.0 is off, 1.0 is full.",
            }
        },
        "required": ["brightness"],
    },
}

# The first step is to set ctool config

tool = types.Tool(function_declarations=[power_disco_ball,start_music,dim_lights])

config = types.GenerateContentConfig(
    tools = [tool],

    automatic_function_calling = types.AutomaticFunctionCallingConfig( disable = True),

    # To force the model to select any function insated of all

    tool_config =types.ToolConfig(
        function_calling_config = types.FunctionCallingConfig( mode = 'ANY')
    )
)

chat = client.chats.create(model = "gemini-3.5-flash", config = config)

res = chat.send_message("Start the party by strating the music, starting the disco lights and altering the lights")

# Print out each of the function calls requested from this single call
print("Example 1: Forced function calling")
for fn in res.function_calls:
    args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
    print(f"{fn.name}({args}) - ID: {fn.id}")
