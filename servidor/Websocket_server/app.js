import WebSocket from 'ws';

const SERVER_WS = 'ws://localhost:8010/ws';
let ws;

function connectWebSocket() {
    ws = new WebSocket(SERVER_WS);

    ws.on('open', () => {
        console.log("[WebSocket] Conectado.");
        ws.send('Cliente conectado com sucesso!');
    });

    ws.on('message', (data) => {
        console.log("[WebSocket] Mensagem recebida:", data.toString());
        ws.send('Confirmado! Mensagem recebida.');
    });

    ws.on('close', () => {
        console.warn("[WebSocket] Ligação perdida. A tentar reconectar...");
        setTimeout(connectWebSocket, 3000);
    });
}

connectWebSocket();



