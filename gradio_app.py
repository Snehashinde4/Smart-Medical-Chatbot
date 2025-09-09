#VoiceBot UI using gradio
import os
import gradio as gr
from brain_of_the_doctor import encode_image,analye_the_image
from voice_of_the_patient import record_audio_simple, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_eleven_labs