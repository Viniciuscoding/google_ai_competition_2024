const express = require('express');
const app = express();

const http = require('http');
const {Server} = require("socket.io");
const cors = require('cors');

app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
})

io.on("connection", (socket) => {
  // console.log(`User Connected: ${socket.id}`)

  socket.on("send_message", (data) => {
    socket.broadcast.emit("receive_message", data)
  })
})

const configRoutes = require('./routes');

app.use(express.json());
configRoutes(app);

server.listen(5000, () => {
  console.log('Backend will be running on http://localhost:5000');
  console.log();
});