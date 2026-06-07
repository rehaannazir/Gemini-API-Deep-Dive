#                             Recipe Extractor

import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
"""

class ingredient(BaseModel):

    name : str = Field(
        description = "Name of the ingredient"
    )
    quantity : str = Field(
        description = "Quanity of ingredient with units"
    )

class Recipe(BaseModel):

    name : str = Field(
        description = "Name of recipe for which we require ingredients"
    )
    time_to_cook : Optional [str] = Field(
        description = "Time required to cook the whole recipe"
    )
    ingredients : List[ingredient] = Field(
        description = "Ingrdedients required to cook the recipe"
    )
    instructions : List[str] = Field(
        description = "Step-by-Step instructions of things which ae helpful to cook recipe"
    )

response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents = prompt,
    config={
        "response_mime_type" : "application/json",
        "response_schema" : Recipe.model_json_schema()
    }
)

recipe = Recipe.model_validate_json(response.text)

print(recipe)

#                  Recursive Schemas (Avoid it just use it where necessary)

prompt = """
Generate an organization chart for a small team.
The manager is Alice, who manages Bob and Charlie. Bob manages David.
"""

class Employee(BaseModel):

    name : str = Field(
        description="Name of Employee"
    )
    employee_id : int = Field(
        description="Id of employee given by organisation"
    )
    manages : List["Employee"] = Field(
        default_factory = list,
        description = "A list of employees reporting to this employee"
    )

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = prompt,
    config = {
        "response_mime_type" : "application/json",
        "response_schema" : Employee
    }
)

employee = Employee.model_validate_json(response.text) # Gemini is giving faulty output
print(employee)

#                   Streaming

prompt = "The new UI is incredibly intuitive and visually appealing. Great job. Add a very long summary to test streaming!"

class Fetch(BaseModel):

    topic : str 
    summary : str = Field(
        description = "Write an extensive summary on the given topic"
    )

response = client.models.generate_content_stream(
    model = "gemini-2.5-flash",
    contents = prompt,
    config = {
        "response_mime_type" : "application/json",
        "response_schema" : Fetch.model_json_schema()
    }
)
    
for chunk in response:

    print(chunk.candidates[0].content.parts[0].text)
