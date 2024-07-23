const WebSocket = require("ws");

const url = "ws://127.0.0.1:8080/ws/example/room";
const connection = new WebSocket(url);

connection.onopen = () => {
    console.log("Connected");
};

connection.onerror = (error) => {
    console.log(`Websocket error: ${error.message}`);
};

connection.onmessage = (e) => {
    console.log(e.data);
};

process.on("SIGINT", function () {
    connection.close(1000);
    process.exit();
});
