import express from 'express';
const router = express.Router();
import { getAudio, transcribeAudio, summarizeText, translateText } from '../utils/helper.js';

router.post('/process-url', async (req, res) => {
    const {url} = req.body;

    try {
        // Download URL
        const audio = await getAudio(url);
        
        // Perform Transcription
        const transcription = await transcribeAudio(audio);
        
        // Perform Summarization
        const summary = await summarizeText(transcription);
        
        // Perform Translation
        const translation = await translateText(summary);
        
        res.json({ transcription, summary, translation});
    } catch (error) {
        res.status(500).json({error: error.message});
    }
});

export default router;