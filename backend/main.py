from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# Import your service functions
from services.whisper import transcribe_audio
from services.summarizer import generate_summary
from services.text_to_speech import generate_tts

app = FastAPI()

# Allow requests from your Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = "backend/static/uploads"
AUDIO_DIR = "backend/static/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "SummA.I.ry backend is running!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 1. Save uploaded file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Transcribe if audio/video, else read text
    if file.content_type.startswith("audio") or file.content_type.startswith("video"):
        text = transcribe_audio(file_location)
    else:
        with open(file_location, "r", errors="ignore") as f:
            text = f.read()

    # 3. Generate summary
    summary_text = generate_summary(text)

    # 4. Generate TTS audio
    audio_filename = f"{os.path.splitext(file.filename)[0]}_summary.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    generate_tts(summary_text, audio_path)

    # 5. Return JSON to frontend
    return {
        "summary_text": summary_text,
        "audio_url": f"/static/audio/{audio_filename}"
    }
