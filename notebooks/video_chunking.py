import json
import pytube
import moviepy.editor as mp
from dataclasses import dataclass
from pathlib import Path
import cv2
from task_configs import DEFAULT_VIDEOS_BUCKET
from google.cloud import storage


class VideoPreprocessor:
    METADATA_FILE = 'metadata.json'

    def __init__(self, output_directory):
        self.output_directory = Path(output_directory)
        self.video_dir = None
        self.video_path = None
        self.audio_path = None


    def download_youtube_video(self, youtube_url):
        """Downloads a YouTube video and saves it locally.

        Args:
            youtube_url: The URL of the YouTube video.

        Returns:
            Path: The path to the downloaded video file.
        """

        # download video
        yt = pytube.YouTube(youtube_url)
        video_stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first() 

        # ensure video title is a valid filename & create video directory
        video_name = yt.title.replace('/', '_').replace('\\', '_').replace(':', '_')[:100]

        # create video directory
        video_dir = self.output_directory / video_name
        video_dir.mkdir(parents=True, exist_ok=True)
        # set class variable for video_dir
        self.video_dir = video_dir
        

        # download video
        video_path = video_dir / video_stream.default_filename
        self.video_path = video_path # Set class variable for video_path
        print(f'Downloading {video_name} to {video_dir} at {video_path}')
        video_stream.download(output_path=video_dir)

        return video_path

    def extract_audio(self, video_path=None):
        """Extracts the audio from a video file.

        Args:
            video_path: The path to the video file.

        Returns:
            Path: The path to the extracted audio file.
        """

        if self.video_path is None and video_path is None:
            raise ValueError('Please provide a video path.')
        elif video_path is None:
            video_path = self.video_path

        audio_filename = Path(video_path.stem + '.mp3')  # Change for cleaner naming
        audio_path = self.video_dir / audio_filename
        self.audio_path = audio_path

        clip = mp.VideoFileClip(str(video_path))  # Convert Path to str for moviepy
        print(f'Extracting audio to {audio_path} in {self.video_dir}')
        clip.audio.write_audiofile(str(audio_path))

        return audio_path

    def basic_segmentation(self, video_path=None, segment_length=120):
        """Segments a video into smaller clips and extracts audio for each.

        Args:
            video_path: The path to the video file.
            segment_length: The desired length of each segment in seconds.

        Returns:
            VideoSegment: An object containing lists of paths to the segments.
        """

        if self.video_path is None and video_path is None:
            raise ValueError('Please provide a video path.')
        elif video_path is None:
            video_path = self.video_path
        
        @dataclass
        class VideoSegments:
            video_paths: list[Path]  # Use Path type hints
            audio_paths: list[Path]

        clip = mp.VideoFileClip(str(video_path))
        duration = clip.duration
        num_segments = int(duration // segment_length) + 1

        segment_paths = []
        audio_paths = [] 

        for i in range(num_segments):
            start = i * segment_length
            end = min((i + 1) * segment_length, duration)

            # Video segment 
            segment_filename = f'video_segment_{i}.mp4'
            segment_path = self.video_dir / segment_filename
            subclip = clip.subclip(start, end)
            subclip.write_videofile(str(segment_path))
            segment_paths.append(segment_path)

            # Audio extraction for the segment
            audio_filename = f'audio_segment_{i}.mp3'
            audio_path = self.video_dir / audio_filename
            subclip.audio.write_audiofile(str(audio_path))  
            audio_paths.append(audio_path)

        self.segment_paths = segment_paths
        self.audio_paths = audio_paths
        
        return VideoSegments(segment_paths, audio_paths) 
    
    def extract_frames(self, video_path, frame_interval=1):
        """Extracts frames from a video at a specified interval.

        Args:
            video_path: The path to the video file.
            frame_interval: Interval between extracted frames (in seconds).

        Yields:
            numpy.ndarray: The next frame as a NumPy array.
        """

        cap = cv2.VideoCapture(str(video_path))  # Convert Path to str 

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # End of video

            if frame_count % (frame_interval * cap.get(cv2.CAP_PROP_FPS)) == 0: 
                yield frame

            frame_count += 1

        cap.release()

    def save_metadata(self):
        metadata = {
            "output_directory": str(self.output_directory),  
            "video_dir": str(self.video_dir) if self.video_dir else None,
            "video_path": str(self.video_path) if self.video_path else None,
            "audio_path": str(self.audio_path) if self.audio_path else None,
            "segment_paths": [str(p) for p in self.segment_paths] if self.segment_paths else None,
            "audio_paths": [str(p) for p in self.audio_paths] if self.audio_paths else None,
        }

        metadata_file = self.video_dir / self.METADATA_FILE
        with metadata_file.open('w') as f:
            json.dump(metadata, f)

    def load_metadata(self, video_dir_name=None):
        if video_dir_name is None:
            raise ValueError('Please provide a video directory.')
        else:
            self.video_dir = self.output_directory / video_dir_name

        metadata_file = self.video_dir / self.METADATA_FILE
        if metadata_file.exists():
            with metadata_file.open('r') as f:
                metadata = json.load(f)

            self.output_directory = Path(metadata.get('output_directory', self.output_directory))
            self.video_dir = Path(metadata.get('video_dir')) if metadata.get('video_dir') else None
            self.video_path = Path(metadata.get('video_path')) if metadata.get('video_path') else None
            self.audio_path = Path(metadata.get('audio_path')) if metadata.get('audio_path') else None
            self.segment_paths = [Path(p) for p in metadata.get('segment_paths', [])]
            self.audio_paths = [Path(p) for p in metadata.get('audio_paths', [])]
    def upload_to_cloud_storage(self,bucket):
        """ Uploads the entire directory, its subdirectories containing all video segments, 
            images, audios to cloud storage and returns the cloud storage uri of all the files
            Reference: https://cloud.google.com/storage/docs/samples/storage-transfer-manager-upload-directory
            Returns: a python dictionary containing all the respective extracted and 
                     chunked entities and their respective uris using the same keys as in the metadata.
        """
        cloud_storage_metadata_dict = {}
        #TODO: Andrew to implement this feature using the reference provided
        return cloud_storage_metadata_dict
        
