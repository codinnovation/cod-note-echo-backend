from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY_2")

app = FastAPI()

# Define request body structure
class TranscriptRequest(BaseModel):
    transcript: str
    transcriptHeader: str
    courseName: str

# Sanitize input to prevent injection
def sanitize_input(text: str) -> str:
    return text.replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("<", "").replace(">", "")

@app.post("/api/summary")
async def summarize_transcript(request: TranscriptRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="Missing OpenAI API key")

    clean_transcript = sanitize_input(request.transcript)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Summarize the following lecture transcript from the course '{request.courseName}', covering '{request.transcriptHeader}'.

                    - Remove off-topic discussions, background noise, and interruptions.
                    - Keep key points structured with subheaders.
                    - Maintain clarity, add examples where necessary.
                    - Use simple, academic language.

                    Transcript:
                    '{clean_transcript}'
                    """,
                }
            ],
        )

        summary = response["choices"][0]["message"]["content"].strip()

        return {"message": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

