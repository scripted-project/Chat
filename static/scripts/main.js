var socketio = io()

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
