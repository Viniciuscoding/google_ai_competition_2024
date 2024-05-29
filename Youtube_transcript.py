from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_clean_transcript(video_id):
    """Takes a youtube video id (in the video link, can look like: YrVVXFMgXrw). Pulls transcript and returns clean version."""
    # checks to see if full link then returns just id
    if "v=" in video_id:
        video_id = parse_video_id(video_id)
    # Pull transcript
    script = YouTubeTranscriptApi.get_transcript(video_id)
    # Combine 'text' fields into one string
    input_string = ' '.join([line['text'] for line in script])
    # remove special charaters
    pattern = re.compile(r'[^a-zA-Z0-9\s.,;:!"\'()\-—–?‘’“”\[\]]')
    transcript =  pattern.sub('', input_string)

    return transcript

def parse_video_id(video_url):
    try:
        # Split the URL by "v="
        split_url = video_url.split("v=")
        # Extract the substring after "v="
        video_id = split_url[1]
        return video_id
    except IndexError:
        print("Invalid URL format")
        return None
