import os
from dotenv import load_dotenv
import base64
from groq import Groq

# Load environment variables
load_dotenv()

# Step 1: Setup GROQ API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step 2: Convert image to required format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Define the image path
image_path = "acne.jpg"  # Replace with the actual path to your image file
encoded_image = encode_image(image_path)

# Step 3: Setup Multimodal LLM
query = "Please analyze the image of my face and let me know if there are any visible signs of acne or other skin conditions. Provide a detailed explanation."
model = "meta-llama/llama-4-scout-17b-16e-instruct"

def analye_the_image(query, model):
    client = Groq(api_key=GROQ_API_KEY)
    
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    # Extract and display the assistant's response
    assistant_response = chat_completion.choices[0].message.content
    return assistant_response

# Call the function and print the result
response = analye_the_image(query, model)
print("Assistant's Response:")
print(response)