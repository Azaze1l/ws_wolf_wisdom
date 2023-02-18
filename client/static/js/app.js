init = () => {
    connection = new Connection(onOpen, onMessage, onClose, onError);
}

ping = () => {
    if (!run) return;
    console.log(`ping`);
    connection.push(PING_EVENT, {
        id: id,
    });
}

onMessage = (msg) => {
    let event = JSON.parse(msg.data);
    const type = event['type'];
    const payload = event['payload'];
    console.log(`new event with type ${type} and payload ${JSON.stringify(payload)}`);
    if (type === INITIAL) {
        onFullyConnected(payload);
    } else if (type === WISDOM_DISTRIBUTION) {
        let el = document.getElementById('quotes');
            el.textContent = payload["message"];
    } else if (type === SUBSCRIBE_CONFIRMATION){
        let el = document.getElementById("quotes");
        el.textContent = "Любят тихо. Громко только подписываются.";
    }else {
        console.log(`unsupported event type ${type}, data ${payload}`)
    }
}

onFullyConnected = (payload) => {
    id = payload['id'];
    subscribed = false;
    connection.push(CONNECT_EVENT, {
        id: id,
    });
    setInterval(ping, 5000)
}


onOpen = () => {
    console.log('ws connection opened');
}


onClose = () => {
    console.log('ws connection closed');
    connection.push(
        DISCONNECT_EVENT,
        {
            id: id,
        }
    );
    run = false;
}


onError = (e) => {
    console.log(`connection closed with error ${e}`);
    run = false;
}

onSubscribe = () => {
    subscribed = true;
    SubscribeButton.classList.add("active")
}

onUnsubscribe = () => {
   subscribed = false;
   SubscribeButton.classList.remove("active");
   let el = document.getElementById("quotes");
   el.textContent = "Волк это волк до первой отписки...";
}

onClick = () => {
    if (subscribed === false) {
        connection.push(SUBSCRIBE_EVENT, {
        id: id,
    });
        onSubscribe()
    } else {
         connection.push(UNSUBSCRIBE_EVENT, {
        id: id,
    });
        onUnsubscribe()
    }

}
SubscribeButton.addEventListener('click', onClick);
