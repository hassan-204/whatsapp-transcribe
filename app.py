from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from openai import OpenAI
from pydub import AudioSegment
from requests.auth import HTTPBasicAuth
from starlette.responses import Response

openai_key = os.getenv('OPENAI_KEY')
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_KEY')

openai_client = OpenAI(api_key=openai_key)
app = FastAPI()

# Directory to save media files if sent
MEDIA_FOLDER = "downloads/"
os.makedirs(MEDIA_FOLDER, exist_ok=True)

@app.post("/whatsapp")
async def whatsapp(request: Request):
    form_data = await request.form()
    from_number = form_data.get("From")
    message_body = form_data.get("Body")
    num_media = int(form_data.get("NumMedia", 0))

    print(f"Message from {from_number}: {message_body}")

    # Prepare a response
    response = MessagingResponse()

    # Process incoming media if present
    if num_media > 0:
        media_url = form_data.get("MediaUrl0")
        content_type = form_data.get("MediaContentType0")
        
        # Download and save the media file
        file_extension = content_type.split('/')[1]  # Extracts the file extension from content type
        file_name = f"{from_number}_media.{file_extension}"
        file_path = os.path.join(MEDIA_FOLDER, file_name)
        
        # Download the file
        media_content = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token)).content
        with open(file_path, "wb") as file:
            file.write(media_content)
        
        print(f"Media saved to {file_path}")
        transcription = transcribe(file_path)
        response.message(transcription)
    else:
        # If no media, just respond to the text message
        response.message("Hello! Thanks for your message.")
    
    return Response(content=str(response), media_type="application/xml")

def convert_ogg_to_mp3(ogg_file_path):
    audio = AudioSegment.from_file(ogg_file_path, format="ogg")
    mp3_file_path = ogg_file_path.replace(".ogg", ".mp3")
    audio.export(mp3_file_path, format="mp3")
    return mp3_file_path

def transcribe(ogg_file_path):
    mp3_file_path = convert_ogg_to_mp3(ogg_file_path)
    audio_file = open(mp3_file_path, "rb")
    transcription = openai_client.audio.transcriptions.create(
        model="whisper-1", 
        language='en',
        file=audio_file 
    )
    audio_file.close()

    return transcription.text