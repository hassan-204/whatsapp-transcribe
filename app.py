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
    try:
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
    except ValueError as ve:
        print(f"Value error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except requests.RequestException as re:
        print(f"Request error: {re}")
        raise HTTPException(status_code=502, detail="Error downloading media.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


def convert_ogg_to_mp3(ogg_file_path):
    try:
        audio = AudioSegment.from_file(ogg_file_path, format="ogg")
        mp3_file_path = ogg_file_path.replace(".ogg", ".mp3")
        audio.export(mp3_file_path, format="mp3")
        return mp3_file_path
    except Exception as e:
        print(f"Error converting .ogg to .mp3: {e}")
        raise


def transcribe(ogg_file_path):
    mp3_file_path = None
    try:
        mp3_file_path = convert_ogg_to_mp3(ogg_file_path)
        
        with open(mp3_file_path, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1",
                language='en',
                file=audio_file
            )
        
        return transcription.text
    except Exception as e:
        print(f"Error transcribing audio file: {e}")
        raise
    finally:
        # Clean up both .ogg and .mp3 files
        for file_path in [ogg_file_path, mp3_file_path]:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as cleanup_error:
                    print(f"Error deleting file {file_path}: {cleanup_error}")