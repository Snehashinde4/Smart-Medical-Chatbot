import os
import platform
import subprocess
from gtts import gTTS
from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv()

def text_to_speech_with_gtts(text, output_filepath):
    language = "en"
    
    # Generate MP3 file
    audioobj = gTTS(text=text, lang=language, slow=False)
    audioobj.save(output_filepath)
    
    # Convert MP3 to WAV
    wav_filepath = output_filepath.replace(".mp3", ".wav")
    audio = AudioSegment.from_mp3(output_filepath)
    audio.export(wav_filepath, format="wav")
    
    # Play the WAV file
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', wav_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Input text for TTS
input_text = "Hello, this is your personal health assistant."
text_to_speech_with_gtts(input_text, output_filepath="gtts_test.mp3")

# Step 2: Convert text to speech using ElevenLabs
import elevenlabs
from elevenlabs import ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech_with_eleven_labs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        model="eleven_turbo_v2", 
        output_format="mp3_22050_32",
    )
    
    elevenlabs.save(audio, "elevenlabs_test.mp3")
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
