# Webex Contact Center Audio Transcription Application

This Flask web application is designed to integrate with **Webex Contact Center** to process audio files recorded during a "Record Activity" event. The application receives the recorded audio as a POST request, transcribes the audio to text using the **Google Cloud Speech-to-Text API**, and returns the transcribed text in the response.

## Purpose

The main objective of this application is to:

- Accept an audio file recorded during a Webex Contact Center activity (e.g., "Record Activity").
- Process the audio file, convert it to the required format.
- Send the audio file to **Google Cloud Speech-to-Text API** for transcription.
- Return the transcribed text to the Webex Contact Center audio record.

## Features

- **Audio Conversion**: The application ensures the audio file is in the proper format (16 kHz, 16-bit) for transcription.
- **Transcription**: The audio file is sent to Google Cloud's Speech-to-Text API for transcription into Spanish (or any language of choice).
- **File Handling**: The application accepts audio files via a POST request and stores them temporarily before processing.
- **Retrieving Transcription**: You can retrieve the latest transcription via a GET request.

## Requirements

Before running the application, ensure you have the following:

- **Python 3.7+** installed.
- **Google Cloud account** with the Speech-to-Text API enabled.
- **Google Cloud Service Account credentials** (JSON format).
- **FFmpeg** installed for audio file processing.

### Dependencies

Install the required Python dependencies using `pip`:

```bash
pip install Flask pydub google-cloud-speech
```
## Setup Instructions

1. Clone the repository or copy the code into a project directory.

2. Install the required dependencies:

   ```bash
   pip install flask pydub google-cloud-speech
   ```

3. Install FFmpeg (required by `pydub`). 

   - On Ubuntu:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   - On Windows, download the FFmpeg binaries from [FFmpeg's official website](https://ffmpeg.org/download.html) and add it to your system's PATH.

4. Set up Google Cloud credentials:

   - Go to the [Google Cloud Console](https://console.cloud.google.com/), create a project, enable the Speech-to-Text API, and create a service account key.
   - Download the service account key JSON file and place it in the project directory. Rename it to `speechkey.json` or update the environment variable in the code to match the file name.

5. Run the application:

   ```bash
   python app.py
   ```

   The application will start on `http://127.0.0.1:5000/`.

   You have to tunnel with ngrok port 5000 and then put en HTTP NODE in the Wxcc FLOW

## Usage Workflow

1. Recording in Webex Contact Center:

- During a Webex Contact Center session, an audio file is recorded (e.g., from a "Record Activity" event).
- The audio file is sent via a POST request to the /transcribir endpoint.
  
2. Audio Processing:

- The application processes the audio to ensure it's in the correct format (16 kHz, 16-bit).
- The processed audio is sent to the Google Cloud Speech-to-Text API for transcription.
  
3. Transcription:

-The transcription result is returned as text, and the Webex Contact Center can utilize it as needed.

4. Retrieving Transcription:

- The GET /transcripcion endpoint allows for retrieving the latest transcription result.

**Example Response:**

```json
{
    "texto": "Transcribed text of the audio"
}
```

### 2. Retrieve Latest Transcription

- **URL:** `/transcripcion`
- **Method:** `GET`

Retrieves the latest transcription processed by the API.

**Example Response:**

```json
{
    "texto": "Transcribed text of the audio"
}
```

### Images

![image](https://github.com/user-attachments/assets/1689f3c5-f5f8-47fd-9cc9-202b0541b99c)


![image](https://github.com/user-attachments/assets/8233d0e7-052c-4707-bd4c-8a8eeac83075)


