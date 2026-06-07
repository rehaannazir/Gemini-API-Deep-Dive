#    ******************* Pydantic Basics ************************

from pydantic import BaseModel, Field
from typing import Optional, List

# Concept 1: Base Model

class User(BaseModel):

    name : str
    age : int
    cnic : int = "xxxxxxxx" # Way of giving Default value

user = User(
    name = "Rehaan",
    age = 20

)

print(user)

# Concept 2: Type Validation

user_ = User(
    name = "Rehan Nazir",
    age = "Twenty"       # Give error due to invalid type
)

# Concept 3: Optional

class User(BaseModel):

    name : str
    age : int
    id : Optional [int] = None # Giving default for Optional is a best practice

user = User(
    name = "Rehan Nazir",
    age = 21
)

# Concept 4: List

class User(BaseModel):

    model : str
    company : str
    features : List[str]

user = User(
    model = "Fortuner",
    company = "Toyota",
    features = ["legender", "turbo", "4*4"]   
)

# Concept 5: Nested Model  (Important one)

class ingredient(BaseModel):

    name : str
    quantity : int 

class recipe(BaseModel):

    name : str
    ingredients : List[ingredient] 

dish = recipe(
    name = "Biryani",
    ingredients = [
        ingredient(
            name = "Garam Masala",
            quantity = 12
        ),
        ingredient(
            name = "Rice",
            quantity = 1
        ),
        ingredient(
            name = "Chicken",
            quantity = 1
        )
    ]
)


# Concept 6: Field (Gives Metadata) Important for schemas in Gemini

class Prodcut(BaseModel):

    name : str = Field(
        description = "Product Name"
    )

    price : float = Field(
        description = "Product Price"
    )

metal = Prodcut(
    name = "Sword",
    price = 490.5
)

# Concept 7: JSON Parsing

class User(BaseModel):

    name : str
    age : int

user = User(
    name = "Mia",
    age = 20
)

print(user.model_dump())  # Gives JSON Object

print(user.model_dump_json()) # Gives JSON String


# Concept 8: JSON Validation

class User(BaseModel):
    name : str
    age : int

AI_response = """
{   "name" : "Mia",
    "age" : 20
}
"""

user = User.model_validate_json( AI_response )

print(user.name)
print(user.age)