from youtube_transcript_api import YouTubeTranscriptApi

class Transcription:
    def video_id_finder(yt_url):
        """
        argument:
            yt_url <str> = Youtube url in a string format
        output:
            yt_id <str>= A string id from a Youtube url is returned. In case of a wrong URL is provided, an IndexError exception is returned.
        """
        try:
            yt_id = yt_url.split("v=")[1]
            return yt_id
        except IndexError:
            return "Not a valid URL format. Please make sure to include YouTube videos URL."

    def yt_transcription_list(video_id):
        """
        argument:
            video_id <str> = Youtube url in a string format
        output:
            transcription_list <TranscriptList> = A list of results d.
        """
        try:
            transcription_list = YouTubeTranscriptApi.list_transcripts(video_id)
            return transcription_list
        except Exception as exception:
            raise exception

    def yt_transcript(transcript_list, lang_code = ["en"]):
        """
        argument:
            lang_code <list[str]> = String language codes inside a list of strings.
            transcript_list <TranscriptList> = Return a TranscriptList object which is iterable and provides methods to filter the list of transcripts for specific languages and types.
        output:
            transcript <str> = Return a string from the transcript based on the language code provided.
        """   
        return transcript_list.find_transcript(lang_code)

    def video_language(transcript_list):
        return transcript_list.language

    def fetch_transcript(transcript):
        return transcript.fetch()

    def format_transcript(transcript):
        input_string = ' '.join([row['text'] for row in transcript])
        return input_string
    

# class Translation: 
#     def video_translation_languages(transcript):
#         return transcript.translation_languages

#     def language_to_ISO(language, yt_lang_lib = ISO_693):
#         for lang_n_ISO in yt_lang_lib.keys():
#             if language.lower() in lang_n_ISO.lower():
#                 return yt_lang_lib[language.title()]
#             else:
#                 continue
#         print(f"The language '{language}' is not supported by Youtube's library of languages. None is returned for a language not found")
#         return None

#     def translate_transcript(transcription, language):
#         try:
#             ISO = language_to_ISO(language)
#             if transcription.is_translatable:
#                 try:
#                     translation = transcription.translate(ISO)
#                     return fetch_transcript(translation)
#                 except Exception as exception:
#                     print(f"Error: TranslationLanguageNotAvailable. The language ISO '{ISO}' for '{language}' is not supported by Youtube.")
#                     return [{'text': f"'{language}' is not translatable.", 'start': 0.0, 'duration': 0.0}]
#             else:
#                 return [{'text': f"'{language}' is not translatable.", 'start': 0.0, 'duration': 0.0}]
#         except Exception as exception:
#             return f"{language} not found in the Youtube's library of languages supported for the ISO format."