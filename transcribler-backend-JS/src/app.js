import express from 'express';
import cors from 'cors';
import processRoute from './routes/process.js';

const app = express()
const port = 3000;

app.use(cors());

app.use(express.json());
app.use('/api', processRoute);

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});