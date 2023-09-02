// 웹소켓
const chatHistory = []

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

chatSocket.onopen = function(e) {
  console.log("연결성공!")
}

let info = null

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);

  if (data.message){
    removeLoadingMessage()
    displayMessage(data.sender, data.message)
    chatHistory.push({sender: data.sender, message: data.message})
    console.log(chatHistory)
  }
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

  if (message !== '' && bookId) {
    displayMessage('user', message);
    chatHistory.push({sender: 'user', message: message})
    userMessageInput.value = '';

    showLoadingMessage();
    chatSocket.send(
      JSON.stringify({
        message: message,
      })
    );
  }
}

document.querySelector('#reset').onclick = function (e){
  axios.delete(`/api/chat/${bookId}/delete`).then(() => {
      console.log("채팅 기록이 성공적으로 삭제되었습니다!!!");
      window.location.reload();
  }).catch(() => {
      console.log("채팅 기록 삭제에 실패했습니다.");
  });
}

// document.querySelector('#end').onclick = function (e){
//   axios.post(`/api/chat/${bookId}/end/`, {chatHistory})
//   .then(() => {
//       console.log("POST 요청이 성공했습니다.");
//       window.location.href = `/result-page/${bookId}/`;
//   }).catch(() => {
//       console.log("POST 요청이 실패했습니다.");
//   });
// }

export { chatHistory }