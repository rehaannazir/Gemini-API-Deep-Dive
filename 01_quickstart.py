import os
from google import genai
from PIL import Image
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=API_KEY)

#                           Streaming Response

"""
It printx response in flow as the part(chunk) is completed it prints them without waiting for whole response to complete and then print
"""


response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Write an essay on Illumnati in 500 words"
)



for chunk in response:
    print(chunk.text, end=" ", flush=True)


#                           System Instruction      

"""
It means assigning the model a specific role or give it ruleset
We can say "hey model act like you are teacher"
"""  

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are an AI mentor. Your name is Jhons"
    ),
    contents="Give your small intro"
)

print(response.text)


#                         Multi-turn conversation (Chat)

"""
It means handling multiple prompt at a time
It conserves history of all prompts and their responses
We may use streing here
"""

chat = client.chats.create(model="gemini-2.5-flash")

res_1 = chat.send_message("Who is pakistan national animal in one word?")
print(res_1.text)

res_2 = chat.send_message("Who is pakistan's national bird in one word?")
print(res_2.text)

for message in chat.get_history():

    print(f"role - {message.role}", end=": ")
    print(message.parts[0].text)

t = [*chat.get_history()]
tokens = client.models.count_tokens(
    model = "gemini-2.5-flash",
    contents = t
)

#                Multimodel Responses (Using image)

"""
Gemini API can take image and give us output in text by recignising it
Its helpful to extract data from receipts, invoices, screenshots
"""

image = Image.open("../weather.png")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[image, "Can you understand this it?"]
)

print(response.text)

#                             Thinking

"""
To increase response accuracy and cost we use it
"""

response = client.models.generate_content(
    model = "gemini-3.5-flash",
    config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(thinking_level="low") 
    ),
    contents= "1+7-6*5="
)

print(response.text)