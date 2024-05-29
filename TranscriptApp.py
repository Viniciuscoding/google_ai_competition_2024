# Import all the necessary dependencies
import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
import google.generativeai as genai
from dotenv import load_dotenv
from Gemini_Video_Summary import Gemini_Summarization
from configured_chat import ConfiguredChat
from notebooks.topic_detection_function import detect_topics_sentiment

load_dotenv()  # Load environment variables from .env file
application = Flask(__name__)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

chat_instance = ConfiguredChat(
    project_id="vertexai-gemini-hackathon-2024",
    model_name="gemini-1.5-pro-preview-0409",
)

chat_instance = chat_instance.model.start_chat()


@application.get("/summary")
def summary_api():
    """
    Summarizes the transcript of a YouTube video.

    This function takes a YouTube video URL and an optional max_length parameter as inputs.
    It first retrieves the transcript of the YouTube video.
    If the transcript is longer than 3000 words, it uses extractive summarization (e.g. LSA).
    Otherwise, it uses abstractive summarization.

    Parameters:
    - url (str): The URL of the YouTube video.
    - max_length (int, optional): The maximum length of the summary. Defaults to 150.

    Returns:
    - str: The summarized transcript.
    - int: HTTP status code (200 for success, 404 for failure).
    """
    url = request.args.get("url", "")
    max_length = int(request.args.get("max_length", 150))
    video_id = url.split("=")[1]
    summarizer = Gemini_Summarization()

    try:
        transcript = get_transcript(video_id)
        # print(f"transcript: {transcript}\n")
    except:
        return "No subtitles available for this video", 404

    try:
        # final_summary, combined_summaries = summarizer.complete_summarization(
        #     transcript, is_YU_url=False
        # )
        sentiment_topic = detect_topics_sentiment(transcript)
        print(f"sentiment: {sentiment_topic}\n")
        # print(f"summary: {final_summary}\n")
    except Exception as e:
        print(f"Error occurred during summarization: {str(e)}")
        return "An error occurred during summarization. Please try again later.", 500

    return sentiment_topic, 200
    # return final_summary, sentiment_topic, 200

def is_transcript_english(transcript):
    """
    Detect if the transcript is primarily in English.

    :param transcript: The transcript text to be analyzed.
    :return: True if the transcript is primarily in English, False otherwise.
    """
    try:
        language = detect(transcript)
        return language == "en"

    except Exception as e:
        return False


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

@application.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    response = chat_instance.send_message(user_message)
    response_text = response.text
    print(response_text)
    return response_text


if __name__ == "__main__":
    application.run(debug=True)
