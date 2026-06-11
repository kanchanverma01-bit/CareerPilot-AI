import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ HERE
        messages=[
            {"role": "system", "content": "You are an AI interviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content