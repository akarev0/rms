document.getElementById('chat-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const userInput = document.getElementById('user-input').value;
    document.getElementById('user-input').value = '';

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="user-message"><strong>You:</strong> ${userInput}</div>`;

    const response = await fetch('/chat-v2', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    chatBox.innerHTML += `<div class="bot-message"><strong>robot:</strong> ${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
});
