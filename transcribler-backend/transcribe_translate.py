import re
from youtube_transcript_api import YouTubeTranscriptApi

class TranscribeTranslate():
    """A solution to transcribe and translate youtube videos by just providing their links."""

    def parse_video_id(self,video_url):
        try:
            # Split the URL by "v="
            split_url = video_url.split("v=")
            # Extract the substring after "v="
            video_id = split_url[1]
            return video_id
        except IndexError:
            return "Invalid URL format"

    def clean_transcript(self,transcript):
        """Takes a youtube video id (in the video link, can look like: YrVVXFMgXrw).
        Pulls transcript and returns clean version."""
        input_string = ' '.join([line['text'] for line in transcript])
        return input_string

    def video_transcript_list(self,video_id):
        print(video_id)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        return transcript_list

    def video_transcript(self,transcript_list, language_code = ["en"]):
        return transcript_list.find_transcript(language_code)

    def fetch_transcript(self,transcript):
        return transcript.fetch()

    def video_language(self,transcript):
        return transcript.language

    def video_translation_languages(self,transcript):
        return transcript.translation_languages

    def video_language_supported(self,translation_languages, language):
        count = 0
        nlang = len(translation_languages)
        for lang in translation_languages:
            count += 1
            if lang['language_code'] == language:
                return True
            else:
                if count == nlang:
                    break
                else:
                    continue
        return False

    def video_translation(self,transcript, language):
        if transcript.is_translatable:
            try:
                translation = transcript.translate(language)
                return self.fetch_transcript(translation)
            except Exception as exception:
                print("Error: TranslationLanguageNotAvailable. Could not translate the video because the translation language is not avaialable.")
                # raise exception
                return [{'text': f"Language '{language}' is not available for translation.", 'start': 0.0, 'duration': 0.0}]
        else:
            return [{'text': f"Language '{language}' is not available for translation.", 'start': 0.0, 'duration': 0.0}]