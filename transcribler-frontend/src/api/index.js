export { getVideoData, getTest } from "./video.js";

// import ytdl from 'ytdl-core';
// import fs from 'fs';

// // use case
// // searching for toxicity in video transcription for age-appropriate content

export async function transcribeAudio(audio_file) {
  // Perform Transcription
  const session = await ai.languageModel.create();

  // dummy link but it should be the audio file
  const audio = audio_file;
  const content = await audio.blob();
  const response = await session.prompt([
    { type: "audio", content: content },
    "Transcribe this audio: ",
  ]);

  return response;
}

export async function summarizeText(transcription) {
  // Perform Summarization

  const session = await ai.languageModel.create({
    systemPrompt: "You are a helpful and friendly assistant",
  });

  const response = await session.prompt([
    { type: "text", content: transcription },
    "Summarize this excerpt from a video transcription.",
  ]);

  return response;
}

export async function ageRating(summary) {
  const prompt =
    "What is the age rating of this video? Return your result as a JSON object with the key 'reasoning' with the value as an explanation string, and the key 'rating' and the value as the age rating. Only provide one of these values for the key 'rating': G, PR, PG-13, R, and NC-17";
  const session = await ai.languageModel.create({
    systemPrompt: "You are a helpful and friendly assistant",
  });
  const response = await session.prompt([
    { type: "text", content: summary },
    prompt,
  ]);
  return response;
}

export async function toxicity(summary) {
  const prompt = "";
  console.log(1);
  const session = await ai.languageModel.create({
    systemPrompt: "You are a helpful and friendly assistant",
  });
  const response = await session.prompt([
    { type: "text", content: summary },
    prompt,
  ]);
  return response;
}

export async function sentimentAnalysis(summary) {
  const prompt = "";
  const session = await ai.languageModel.create({
    systemPrompt: "You are a helpful and friendly assistant",
  });
  const response = await session.prompt([
    { type: "text", content: summary },
    prompt,
  ]);
  return response;
}

export async function translateText(text) {
  // Perform Translation
  const translator = await ai.translator.create({
    sourceLanguage: "en",
    targetLanguage: "es",
  });

  const translation = await translator.translate(text);

  return translation;
}
