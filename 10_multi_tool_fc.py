import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

#                                                                     Multi-tool Function Calling

def analyze_project(impact : int, difficulty : int) -> dict:

    """
        description : On the basis of analysis of given AI bussiness project it determines the true worth of project and wether the user should try this project or not

        args : impact (a number from 1-10) tells how much that project is crucial
            difficulty (a number from 1-10) tells how much that project is difficult

        return : It returns score, impact, difficulty and recommendation which help user to take decision about the project
    
    """



    score = impact - difficulty
    recommendation = ""

    if (score >= 5):
        recommendation = "High Priority Project"
    elif (5 > score > 2):
        recommendation = "Medium Priority Project"
    else :
        recommendation = "Low Priority Project"

    return {
        'impact' : impact,
        'difficulty' : difficulty,
        'score' : score,
        'recommendation' : recommendation
    }

promt_2 = """
Search the goggle web and find the AI projects for small bussinesses.
Now select the best AI project according to you and give it the impact and difficulty number from 1-10 according to you

Your answer must be in this format

Project Name  = -----
Impact = ------ (Any number from 1-10)
Difficulty = ----- (Any number from 1-10)

The numbers must be according to AI project according to you not randomnly
"""

input_tokens = client.models.count_tokens(
    model = "gemini-2.5-flash",
    contents = [promt_2]
)


web_response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = promt_2,
    config = types.GenerateContentConfig(
        tools = [
            types.Tool(google_search = types.GoogleSearch())
        ]
    )
)

web_ans = web_response.text

prompt_1 = f"""
You have  a given project name with impact no and difficulty no
{web_ans}
Now use it and apply analyze-project function on it
Use the analyze_project function to analysze it and give the result
Also give me the reason why you select it
"""

func_res = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = promt_2,
    config = types.GenerateContentConfig(
        tools = [
           analyze_project
        ]
    )
)

final_res = func_res.text