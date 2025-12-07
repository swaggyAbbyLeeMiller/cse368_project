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

def extract_text_from_mp4(mp4_path):
    with open(mp4_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )
    return response.text.strip()

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    "Summarize this text clearly and concisely. Start with the main topic. "
                    "Then list major subtopics in bullet points with examples where possible.\n\n" + text
                )
            }
        ]
    )
    return response.choices[0].message.content.strip()

def evaluate_summary(original_text, summary_text):
    prompt = (
        "Evaluate the summary using this rubric:\n"
        "1. Every section/slide is covered.\n"
        "2. The summary is clear and understandable.\n"
        "3. Each major subtopic has its own bullet point.\n\n"
        "Give each category a score from 1 to 3.\n"
        "Then explain the reasoning in 2–3 sentences.\n\n"
        "Return your response in this format only:\n"
        "Scores: X, Y, Z\nExplanation: <text>\n\n"
        "Original Text:\n" + original_text +
        "\n\nSummary:\n" + summary_text
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def parse_scores(evaluation_text):
    try:
        header = evaluation_text.split("\n")[0]
        parts = header.replace("Scores:", "").split(",")
        scores = [int(x.strip()) for x in parts]
        return scores
    except:
        return [3, 3, 3]

def improve_summary(original_text, previous_summary):
    prompt = (
        "The previous summary did not score well. Improve it using the rubric:\n"
        "1. Make sure every major section is addressed.\n"
        "2. Improve clarity.\n"
        "3. Ensure each subtopic has its own bullet point.\n\n"
        "Rewrite a better summary:\n\n"
        "Original text:\n" + original_text
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
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

    name = file.filename.lower()
    if name.endswith(".pdf"):
        text = extract_text_from_pdf(file_location)
    elif name.endswith(".mp4"):
        text = extract_text_from_mp4(file_location)
    else:
        return {"error": "Unsupported file type. Use PDF or MP4."}

    if not text:
        return {"error": "No text extracted from file."}

    summary = summarize_text(text)
    evaluation = evaluate_summary(text, summary)
    scores = parse_scores(evaluation)

    if any(score <= 2 for score in scores):
        summary = improve_summary(text, summary)
        evaluation = evaluate_summary(text, summary)

    audio_filename = f"{os.path.splitext(file.filename)[0]}_summary.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    text_to_speech(summary, audio_path)

    audio_url = f"http://localhost:8000/static/audio/{audio_filename}"

    return {
        "summary_text": summary,
        "evaluation": evaluation,
        "audio_url": audio_url
    }



