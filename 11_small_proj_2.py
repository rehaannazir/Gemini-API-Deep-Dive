import os
from google import genai
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv


load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


class Issue(BaseModel):
    issue: str = Field(description="Problem of user")
    urgency: Literal["low", "medium", "high"] = Field(
        description="How urgent the user's issue is"
    )
    action: str = Field(description="Possible action for problem")


email = "I ordered a product 10 days ago but it has not arrived. Update me or refund my money"

prompt = f"""
Task: Extract the user Gmail issue in precise way.

Gmail:
{email}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": Issue,
        "max_output_tokens": 500,
        "temperature": 0.2
    }
)

print(response.text)

issue = Issue.model_validate_json(response.text)
print(issue)