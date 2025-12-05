from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import fitz
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "backend/static/uploads"
AUDIO_DIR = "backend/static/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text.strip()

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize this text clearly and concisely. The lecture topic and main idea should go first. Afterwards the main ideas of each specific subtopic should be in its own bullet point. Try to include some examples if possible.:\n{text}"}]
    )
    return response.choices[0].message.content.strip()

def text_to_speech(text, output_audio_path):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    audio_bytes = response.read()  
    with open(output_audio_path, "wb") as f:
        f.write(audio_bytes)
    return output_audio_path


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_location)
    if not text:
        return {"error": "No text found in PDF"}

    summary_text = summarize_text(text)

    audio_filename = f"{os.path.splitext(file.filename)[0]}_summary.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    text_to_speech(summary_text, audio_path)

    audio_url = f"http://localhost:8000/static/audio/{audio_filename}"
    return {
        "summary_text": summary_text,
        "audio_url": audio_url
    }


