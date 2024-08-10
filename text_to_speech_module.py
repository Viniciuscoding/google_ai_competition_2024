import os
import json
import pandas as pd
import IPython.display as ipd
from google.cloud import texttospeech

# Code to run the text-to-speech audio
def synthesize_text(text, file_name):
    """Synthesizes speech from the input string of text."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        # name="en-US-Standard-C",
        name="en-US-Journey-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    
    # Uncomment this only to save the response audio into a mp3 file
    # The response's audio_content is binary.
    # with open(f"{os.getcwd()}/audios/{file_name}.mp3", "wb") as out:
    #     out.write(response.audio_content)
    #     print(f'Audio content written to file "{file_name}"')
    return response.audio_content

# Code to get and hear the audio results

# transcript_data = "This is an example only to text the audio coming from this text"
# Transforming the transcript text into audio
# transcript_audio = synthesize_text(transcript_data, "transcript_audio")
# Listening the transcription audio
# ipd.Audio(transcript_audio, autoplay=True) 
