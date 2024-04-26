// WebSocket connection
let ws;

window.onload = function() {
    // Establish WebSocket connection when the page loads
    ws = new WebSocket('ws://localhost:8081/ws');
    
    // Event listener for WebSocket connection open
    ws.onopen = function(event) {
        console.log('WebSocket connection opened.');
        sendData({ event: 'connect' });
    };
    
    // Event listener for WebSocket errors
    ws.onerror = function(event) {
        console.error('WebSocket connection error:', event);
    };
    
    // Event listener for WebSocket close
    ws.onclose = function(event) {
        console.log('WebSocket connection closed:', event);
    };
};

// Function to send JSON data over WebSocket
function sendData(data) {
    // Check if WebSocket connection is open before sending data
    console.log('Sending data:', data);
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
    } else {
        console.error('WebSocket connection is not open.');
    }
}

function startLnd() {
    console.log("Starting LND");
    sendData({ event: 'startLnd' });
}

function stopLnd() {
    sendData({ event: 'stopLnd' });
}

function getLndInfo() {
    sendData({ event: 'getLndInfo' });
}

// server expects a JSON object, with an event key and data key, example:
// { event: 'connect', data: 'some data' }
// communication should follow standard json format
