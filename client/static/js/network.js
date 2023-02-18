class Connection {
    constructor(onOpen, onMessage, onClose, onError) {
        this.connection = new WebSocket(path);
        this.connection.onmessage = onMessage;
        this.connection.onclose = onClose;
        this.connection.onerror = onError;
    }

    push = (type, data) => {
        this.connection.send(JSON.stringify({type: type, payload: data}));
    }
}


