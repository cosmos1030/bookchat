// 웹소켓

function getBookIdFromUrl() {
  // Extract the bookId from the current URL using Regular Expression
  const url = window.location.pathname;
  const regex = /\/book-page\/(\d+)\//;
  const match = url.match(regex);
  if (match) {
    return match[1];
  }
  return null;
}

function showLoadingMessage() {
  const chatMessages = document.getElementById('chatMessages');
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'message bot loading';
  loadingDiv.textContent = '로딩중...';
  chatMessages.appendChild(loadingDiv);
  scrollToBottom();
}

function removeLoadingMessage() {
  const loadingDiv = document.querySelector('.message.bot.loading');
  if (loadingDiv) {
    loadingDiv.remove();
  }
}

function scrollToBottom() {
  const chatMessages = document.getElementById("chatMessages");
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function displayMessage(sender, message) {
  const chatMessages = document.getElementById("chatMessages");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message " + sender;
  messageDiv.textContent = message;
  chatMessages.appendChild(messageDiv);

  scrollToBottom();
}


const bookId = getBookIdFromUrl()

const chatSocket = new WebSocket(
  'wss://'
  + window.location.host
  + '/ws/chat/'
  + bookId
  +'/'
)

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  removeLoadingMessage()
  displayMessage('bot', data.message)
}



chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

document.querySelector('#submit').onclick = function (e) {
  sendMessage();
};

document.getElementById('userMessage').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

function sendMessage() {
  const userMessageInput = document.getElementById('userMessage');
  const message = userMessageInput.value.trim();
  const bookId = getBookIdFromUrl();
  console.log("씨발!")

  if (message !== '' && bookId) {
    displayMessage('user', message);
    userMessageInput.value = '';

    showLoadingMessage();
    chatSocket.send(
      JSON.stringify({
        message: message,
      })
    );
  }
}
