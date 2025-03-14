export { getVideoData } from './video.js';

// import ytdl from 'ytdl-core';
// import fs from 'fs';

// // use case
// // searching for toxicity in video transcription for age-appropriate content

// export async function getAudio(url) {
//     // Get Audio File
//     const audio = ytdl(url, { filter: 'audioonly' });
//     const path = './src/audio_output/audio.mp3';
//     const writeStream = fs.createWriteStream(path);
     
//     audio.pipe(writeStream);

//     return new Promise((resolve, reject) => {
//         writeStream.on('finish', () => {
//             resolve(path);
//         });

//         writeStream.on('error', (error) => {
//             reject(error);
//         });
//     });
// }

// export async function transcribeAudio(audio_file) {
//     // Perform Transcription
//     const session = await ai.languageModel.create();

//     // dummy link but it should be the audio file
//     const audio = audio_file;
//     // const audio = await fetch ('https://cdn.glitch.global/e5522a51-ab87-443b-80b5-2ce583856d56/en_jeremyt_2.wav?v=174043723126')

//     const audioCtx = new AudioContext();
//     const arrayBuffer = await audio.arrayBuffer();
//     const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
//     const response = await session.prompt([{type: 'audio', content: audioBuffer}, "Transcribe this audio: "]);

//     return response
// }

export async function summarizeText(transcription) {
    // Perform Summarization
    const options = { sharedContext: 'This is a scientific article', type: 'key-points', format: 'markdown', length: 'medium'};

    let summarizer;

    summarizer = await ai.summarizer.create(options)

    const summary = await summarizer.summarize(transcription, {context: 'Please summarize this video transcription.'});

    return summary;
}

export async function translateText(text) {
    // Perform Translation
    const translator = await ai.translator.create({ sourceLanguage: 'en', targetLanguage: 'es'});

    const translation = await translator.translate(text);

    return translation;
}