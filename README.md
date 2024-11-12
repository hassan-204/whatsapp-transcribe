# WhatsApp Voice Transcription API with FastAPI and Twilio

This project is a FastAPI-based API for handling and transcribing WhatsApp voice messages received through Twilio. The application processes `.ogg` audio files, converts them to `.mp3`, and transcribes them using OpenAI's Whisper model.

## Features

- **WhatsApp Messaging**: Responds to incoming WhatsApp voice messages via Twilio.
- **Voice Message Processing**: Downloads, converts, and transcribes voice messages.
- **Audio Conversion**: Converts `.ogg` audio files to `.mp3` format using `pydub` and `ffmpeg`.
- **Transcription**: Uses OpenAI Whisper API for audio transcription.
- **Dockerized**: Packaged with Docker and Docker Compose for easy setup and deployment.

## Setup

### Prerequisites

- Twilio account with a registered WhatsApp number
- OpenAI API key
- Docker (required for running the project in a containerized environment)


## Getting Started

Follow these steps to clone the repository and run the application using Docker.

### 1. Clone the Repository

- Open a terminal and clone the repository:

    ```bash
    git clone https://github.com/hassan-204/whatsapp-transcribe/
    cd whatsapp-transcribe
    ```

### 2. Run the Application with Docker

- Ensure you have Docker and Docker Compose installed on your machine.

- In the project root, create a `.env` file with your environment variables:

    ```plaintext
    OPENAI_KEY=<your_openai_api_key>
    TWILIO_SID=<your_twilio_account_sid>
    TWILIO_KEY=<your_twilio_auth_token>
    ```

- Start the application using Docker Compose:

    ```bash
    docker-compose up --build -d
    ```

- Once the application is running, it will be accessible at `http://<your-server-ip>:9999`.

*Note:* Ensure that your VM allows inbound connections with the port `9999`.


### 3. Configure Twilio

- To complete the setup, configure your Twilio WhatsApp number to direct incoming messages to your server’s IP & Port:
    <img src="https://i.gyazo.com/8adc02ef0e442431dacc08f0d3313d25.png" alt="App Screenshot" width="80%"/>


## Possible Improvements

This project could be expanded and improved in several ways:

1. **Using a Local Transcription Model**: 
   - Currently, this project relies on OpenAI's Whisper API for audio transcription. For increased privacy, lower latency, or reduced API costs, consider using a local transcription model. Libraries like [Whisper by OpenAI](https://github.com/openai/whisper) or [Vosk](https://alphacephei.com/vosk/) offer options for on-device transcription, which could eliminate the dependency on external APIs and provide more control over data processing.

2. **Integrate the WhatsApp Business API**:
   - This application currently uses Twilio's API to handle WhatsApp messages. For higher throughput, advanced message templates, or more extensive integrations, the [WhatsApp Business API](https://www.whatsapp.com/business/api) could be a strong alternative. The Business API allows for additional features, like templated messages and customer management, and may be ideal for scaling up this application in a production environment.




