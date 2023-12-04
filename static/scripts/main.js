var socketio = io()
const auth1 = "SChatauth4";
const auth2 = "SChatauth8";

const messages = document.getElementById('msgs');
const createMessage = (name, msg, time) => { // add msg to html document
    const content = `
    <div class="text">
        <span>
            <strong>${name}</strong>: ${msg}
        </span>
        <span class="muted">
            ${time}
        </span>
    </div>
    `;
    messages.innerHTML += content
    autoScroll();
}

socketio.on("message", (data) => {
    createMessage(data.name, data.message, data.time);
});

const sendMessage = () => {
    const message = document.getElementById('message');
    const time = new Date().toLocaleString();
    if (message.value == "") return;
    const data = {data: message.value, time: time};
    socketio.emit("data", data);
    message.value = "";
};

document.getElementById('message').addEventListener('keypress', function(event) {
    if (event.key == 'Enter') {
        document.getElementById('send-btn').click();
    }
});

function autoScroll() {
    messages.scrollTop = messages.scrollHeight;
}

function displayMessages() {
    const house = document.querySelector('.header h2').dataset.house;
    const room = document.querySelector('.header h2').dataset.room;
    fetch(`/api/msgs?house=${house}&room=${room}&auth=${auth1}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
            }
            console.log('Response Status:', response.status)
            return response.json();
        })
        .then(msgs => {
            msgs.forEach(msg => {
                createMessage(msg.name, msg.message, msg.time)
            });
        })
        .catch(error => console.error('Error fetching messages:', error));
}

window.onload = displayMessages();