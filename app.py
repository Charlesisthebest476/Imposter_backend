import json
import os
import google
from google import genai


client = genai.Client(api_key="")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Tell me a joke about robots"
)

print(response.txt)

def get_secret(category):
    prompt = f"msfgjbjhtghsdbtijsjtgwb"
    response = client.models.generate_content(
        model = "gemini-2.5-flash"'
        contents = prompt,
        config = {
            'response_mime_type': 'application/json',
            'response_schema': {
                'type': 'object',
                'properties': {
                    'secret': {'type': 'string'},
                    'hint': {'type': 'string'}
                }
            }
        }

    )
    return response.parsed
