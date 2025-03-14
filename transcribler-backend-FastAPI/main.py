from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

@app.post("/download-audio/")
async def download_audio(request: Request):
    data = await request.json()
    url = data["url"]

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    output_path = "audio_output"
    os.makedirs(output_path, exist_ok=True)
    audio_file_path = os.path.join(output_path, "audio.mp3")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio_output/audio.%(ext)s",
        "ffmpeg_location": "/opt/homebrew/bin/ffmpeg",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(audio_file_path)
    return FileResponse(audio_file_path, media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)