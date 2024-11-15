import os
import logging

from flask import Flask, request, jsonify
from pydub import AudioSegment
from google.cloud import speech

app = Flask(__name__)

# Reemplaza con tu clave de servicio de Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Your Google API Key.json"  # Asegúrate de que la ruta sea correcta

# Configurar el registro
logging.basicConfig(level=logging.INFO)

# Variable para almacenar la transcripción
transcripcion_actual = None

def transcribir_audio(audio):
    """Transcribe un archivo de audio utilizando la API de Speech-to-Text."""
    client = speech.SpeechClient()

    # Convertir el archivo a 16 kHz y 16 bits si es necesario
    audio_segment = AudioSegment.from_file(audio)  # Cargar el archivo
    audio_segment = audio_segment.set_frame_rate(16000)  # Cambiar la tasa de muestreo a 16 kHz
    audio_segment = audio_segment.set_sample_width(2)  # Establecer la profundidad de bits a 16 bits (2 bytes)
    converted_audio_path = 'audio_converted.wav'
    audio_segment.export(converted_audio_path, format='wav')  # Exportar el archivo convertido

    try:
        with open(converted_audio_path, "rb") as audio_file:
            content = audio_file.read()
    except Exception as e:
        logging.error("Error al abrir el archivo de audio: %s", str(e))
        raise

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="es-ES",  # Cambia a tu idioma deseado
    )

    try:
        response = client.recognize(config=config, audio=audio)
    except Exception as e:
        logging.error("Error en la solicitud a la API de Google Speech: %s", str(e))
        raise

    # Obtener la transcripción de los resultados
    transcripciones = [result.alternatives[0].transcript for result in response.results]
    return " ".join(transcripciones)  # Devuelve todas las transcripciones como un único texto

@app.route('/transcribir', methods=['POST'])
def transcribir():
    """Endpoint para recibir el archivo de audio y devolver la transcripción."""
    global transcripcion_actual  # Usar la variable global para almacenar la transcripción
    if 'audio.wav' not in request.files:  ## Must be same name ex 'audio.wav', from HTTP POST in flow
        logging.error("No se encontró ningún archivo de audio")
        return jsonify({'error': 'No se encontró ningún archivo de audio'}), 400

    # Guardar el archivo de audio
    audio_file = request.files['audio.wav']

    if audio_file.filename == '':
        logging.error("No se seleccionó ningún archivo")
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

    # Guardar el archivo temporalmente
    audio_path = 'audio.wav'
    audio_file.save(audio_path)
    logging.info("Archivo guardado: %s", audio_path)  # Log de archivo guardado

    try:
        transcripcion_actual = transcribir_audio(audio_path)
        logging.info("Transcripción: %s", transcripcion_actual)  # Log de la transcripción
        return jsonify({'texto': transcripcion_actual})
    except Exception as e:
        logging.error("Error en la transcripción: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/transcripcion', methods=['GET'])
def obtener_transcripcion():
    """Endpoint para obtener la última transcripción."""
    if transcripcion_actual is None:
        return jsonify({'error': 'No hay transcripción disponible'}), 404

    return jsonify({'texto': transcripcion_actual})

if __name__ == '__main__':
    app.run(debug=True)
