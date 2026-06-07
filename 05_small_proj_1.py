#                   Men’s UEFA European Championship final

import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

class Match(BaseModel):

    tournament : str = Field(description = "Name of the tournament of which you get  from the web")
    year : int 
    winner : str = Field(description="Name of winning team in the tournament")
    runner_up : str = Field(description="Name of runner-up team which loses in final in the tournament")
    goals : int = Field(description="The total no of goals in the final of tournament")
    scorers : List[str] = Field(description="The name of players who scores in the final")
    summary : Optional[str] = Field(description="Give the final match summary that you get from the web search")


prompt = """
Get the information from the web search of the Final Match of Latest UEFA Champions League (Am talking about football)

Now gives me information in JSON with only:
tournament
year
winner
runner up
goals
scorers
summary

Note: Keep in mind search from the web and get information of Final match of the Latest UEFA Champions League
"""

response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents = prompt,
    config = {
        "response_mime_type" : "application/json",
        "response_schema" : Match.model_json_schema(),
        "tools" :[{
            "google_search" : {}
        }]
    }
)

match_stats = Match.model_validate_json(response)
print(response)

