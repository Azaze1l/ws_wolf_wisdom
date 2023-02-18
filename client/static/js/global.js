// globals
let connection;
let path;
let run = true;
let SubscribeButton = document.getElementById('subscribe')

// user
let subscribed;
let id = 'initial';

// server
const INITIAL = 'initial'
const WISDOM_DISTRIBUTION = 'wisdom_distribution';
const SUBSCRIBE_CONFIRMATION = 'subscribe_confirmation'

// client
const PING_EVENT = 'ping';
const CONNECT_EVENT = 'connect';
const DISCONNECT_EVENT = 'disconnect';
const SUBSCRIBE_EVENT = 'subscribe'
const UNSUBSCRIBE_EVENT = 'unsubscribe'


