import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_response(prompt, language="en"):
    # Modify temperature/top_p/stop_tokens for control
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant who responds in {language}."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content.strip()
