from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Groq Translator API")

# Get API key and validate it exists
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.error("GROQ_API_KEY not found in environment variables")
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize Groq client
try:
    groq_client = Groq(api_key=api_key)
    logger.info("Groq client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {str(e)}")
    raise

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = "English"

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Groq Translator API"}

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        logger.info(f"Received translation request: {request.dict()}")
        
        # Construct the prompt for translation
        prompt = f"""Translate the following text from {request.source_language} to {request.target_language}:
        
Text: {request.text}

Translated text:"""

        logger.info("Sending request to Groq API")
        # Call Groq API
        completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful translation assistant. Provide only the translated text without any additional explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.3,
        )

        translated_text = completion.choices[0].message.content.strip()
        logger.info(f"Successfully received translation: {translated_text}")

        return TranslationResponse(
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language
        )

    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8001) 