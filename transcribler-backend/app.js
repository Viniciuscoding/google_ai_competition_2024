import express, { json } from 'express';
import http from 'http';

const app = express();

const server = http.createServer(app);

import configRoutes from './routes/index.js';

app.use(json());
configRoutes(app);

server.listen(5000, () => {
  console.log('Backend will be running on http://localhost:5000');
  console.log();
});

