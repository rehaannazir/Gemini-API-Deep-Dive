import os
import pathlib
import io
import httpx
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client()

# PDF Parsing from local folder

filepath = pathlib.Path("cv.pdf") # Retrive and encode pdf bytes

prompt = "Summarize this cv in 100 words"

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        types.Part.from_bytes(
            data = filepath.read_bytes(),
            mime_type="application/pdf"
        ),
        prompt
    ]
)

print(response.text)

# PDF Parsing from URL pdf

doc_url = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"

data = httpx.get(doc_url).content # Retrieve and encode pdf bytes

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents = [
        types.Part.from_bytes(
            data = data,
            mime_type = "application/pdf"
        ),
        prompt
    ]
)

print(response.text)

# For large files which are locally stored

filepath = pathlib.Path("cv.pdf")

file = client.files.upload(  # File API
    file=filepath
)

response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents = [file, prompt]
)
print(response.text)

# For large files using the url 

file = io.BytesIO(httpx.get(doc_url).content)

new_file = client.files.upload(
    file=file,
    config=dict(mime_type='application/pdf')
)

response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents = [
        new_file,
        prompt
    ]
)

print(response.text)