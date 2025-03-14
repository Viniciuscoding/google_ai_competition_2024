import os
import json
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
import google.generativeai as genai
from dotenv import load_dotenv
from Gemini_Video_Summary import Gemini_Summarization
from topic_detection_function_vin import detect_topics_sentiment
from Vin_Gemini_Video_Summary import Transcription
from configs import VIN_SUMMARY_PROMPT, VIN_TOPIC, VIN_SENTIMENT_ANALYSIS


import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from pytubefix import YouTube

# Load the .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)
# Accessing the environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

from IPython.display import Markdown

# url = "https://www.youtube.com/watch?v=6COmYeLsz4c"

import requests
from bs4 import BeautifulSoup

def get_transcript(video_id):
    """
    Fetches and concatenates the transcript of a YouTube video.

    Parameters:
    video_id (str): The ID of the YouTube video.

    Returns:
    str: A string containing the concatenated transcript of the video.

    Raises:
    Exception: If there is an error in fetching the transcript.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise e

    transcript = " ".join([d["text"] for d in transcript_list])
    return transcript

def parse_sentiment(sentiment):
    data = {}
    lines = sentiment.strip().split("\n")

    for line in lines:
        if "**" in line:
            key = line.split("**")[1].strip(":") 
            value = line.split(":**")[1].strip() 
            data[key] = value
    return data

def download_audio(youtube_url):
  """Downloads the audio of a YouTube video to Google Cloud Storage.

  Args:
    youtube_url: The URL of the YouTube video.
  """

  try:
    yt = YouTube(youtube_url)
    print(f"Downloading: {yt.title}")
    audio_stream = yt.streams.filter(only_audio=True).first()

    if audio_stream:
        # Download the audio to a temporary file
        temp_file = audio_stream.download(output_path="./audio")
        print(f"Downloaded to {temp_file}")
        return temp_file
    else:
        print("No suitable audio stream found.")

  except Exception as e:
    print(f"An error occurred: {e}")



def main(url):
    data = download_audio(url)
    json_data = json.dumps(data, indent=4)
    return json_data

if __name__ == "__main__":
    # Code here will only run when the script is executed directly, not when imported
    main()