import base64
import os
import re
from mistralai import Mistral

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# --- Main Execution ---

image_path = "first_part.jpg"
base64_image = encode_image(image_path)
api_key = os.environ["MISTRAL_API_KEY"]
model = "pixtral-12b-2409"
client = Mistral(api_key=api_key)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image? Please respond with fields like 'Character Name:', 'Classes:', 'Race:', 'Level:', etc... Basically, all the bigger fonts are some characteristic of the character."},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
        ]
    }
]

chat_response = client.chat.complete(model=model, messages=messages)
response_text = chat_response.choices[0].message.content
print("Raw response:\n", response_text)
# Extract the relevant fields from the response