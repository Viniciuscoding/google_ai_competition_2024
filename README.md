# Transcribler - Google AI Competition 2024

Deloitte Team Submission for GCP/Gemini Hackathon. A Chrome Extension for YouTube Multimodal Analysis.

## Overview

Transcribler is a Chrome Extension that provides AI-powered support for YouTube videos with a single click. It offers features such as summarization, translation, Q&A chatbot, sentiment analysis, topic modeling, fake news checking, and age appropriateness evaluation.

![Project Stages](/transcribler-frontend/public/imgs/stages.png)

## Key Features

- Dynamic text summarization with adjustable length
- Language-agnostic transcript summarization
- Support for videos without subtitles
- Asynchronous communication with Flask Backend
- Multiple analysis options: sentiment, topic modeling, fake news detection, etc.

## Demo

![Screenshot](/transcribler-frontend/public/imgs/screenshot-youtube-summary.png)

[Watch Demo Video](https://www.youtube.com/watch?v=bu5BQ0PadBo)

## Installation

1. Clone the repository: `git clone https://github.com/Viniciuscoding/google_ai_competition_2024.git`

2. Set up and run the backend environment: \ 
	`cd transcriber-backend` \
	`pip install -r requirements.txt` \
	`flask --app app run` \

	This will start a local server at `http://127.0.0.1:5000/`. You may see a couple of warnings, but you can ignore them.

3. Set up and run the frontend environment \
	`cd transcriber-frontend` \
	`npm i` \
	`npm run build` \
	`npx vite preview` \

	This will start a local server at `http://localhost:4173`. You may see a couple of warnings, but you can ignore them.

4. Create a `.env` file at the root of the `transcribler-frontend` directory with your Gemini API key: `VITE_GEMINI_API_KEY="your_api_key"`

5. Create a `.env` file at the root of the `transcribler-backend` directory with your Google and Gemini API keys: \
	`GOOGLE_API_KEY="your_api_key"` \
	`GEMINI_API_KEY="your_api_key"` \

6. Load the Chrome extension:
	- Go to `chrome://extensions/`
	- Enable "Developer mode"
	- Click "Load unpacked" and select the `build` folder inside the `transcribler-frontend` directory

## Usage

Navigate to any YouTube video, click the extension icon, and select "Summarize" to see the video transcript summary and access other analysis features.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch for your feature/fix
3. Make changes and commit
4. Push changes to your fork
5. Create a Pull Request
6. Update `Requirements.txt` if new dependencies are added

## Technologies Used

- Flask Backend REST API
- Google Cloud Platform (GCP)
- Gemini AI
- Chrome Extension API
- Venv for environment management
- Various Python libraries (see `environment.yml` for details)
- React
- Vite
- Material UI
- Axios

## Note

This project is part of the Google AI Competition 2024 and showcases the integration of GCP/Gemini technologies with a practical Chrome extension for YouTube video analysis.

