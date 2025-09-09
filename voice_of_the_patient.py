import logging
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import os
from dotenv import load_dotenv
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Retrieve the GROQ_API_KEY
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
print(f"GROQ_API_KEY: {GROQ_API_KEY}")  # Debugging: Check if the API key is loaded

def record_audio_simple(file_path, duration=10, sample_rate=44100):
    """
    Simple audio recording function using sounddevice library.
    
    Args:
        file_path (str): Path to save the recorded audio file.
        duration (int): Duration of the recording in seconds.
        sample_rate (int): Sampling rate for the recording.
    """
    try:
        logging.info("Recording...")
        # Record audio
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        logging.info("Recording finished.")
        
        # Save the audio to a WAV file
        write(file_path, sample_rate, audio_data)
        logging.info(f"Audio saved to {file_path}.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Transcribe audio using the Groq API.
    
    Args:
        stt_model (str): The speech-to-text model to use.
        audio_filepath (str): Path to the audio file to transcribe.
        GROQ_API_KEY (str): API key for Groq.
    
    Returns:
        str: Transcription text.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # Open the audio file
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        
        # Return the transcription text
        return transcription.text
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        print(f"An error occurred during transcription: {e}")
        return None

# Main script
if __name__ == "__main__":
    # Step 1: Record audio
    audio_file_path = "voice_of_the_patient.wav"
    record_audio_simple(file_path=audio_file_path, duration=10)

    # Step 2: Convert WAV to MP3
    mp3_file_path = "voice_of_the_patient.mp3"
    audio = AudioSegment.from_wav(audio_file_path)
    audio.export(mp3_file_path, format="mp3", bitrate="128k")
    print(f"Audio converted and saved to {mp3_file_path}")

    # Step 3: Transcribe the audio
    stt_model = "whisper-large-v3"
    transcription_text = transcribe_with_groq(stt_model, mp3_file_path, GROQ_API_KEY)

    # Step 4: Print the transcription
    if transcription_text:
        print("Transcription:")
        print(transcription_text)