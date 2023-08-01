// function getBookIdFromUrl() {
//   // Extract the bookId from the current URL using Regular Expression
//   const url = window.location.pathname;
//   const regex = /\/book-page\/(\d+)\//;
//   const match = url.match(regex);
//   if (match) {
//     return match[1];
//   }
//   return null;
// }

// function showLoadingMessage() {
//   const chatMessages = document.getElementById('chatMessages');
//   const loadingDiv = document.createElement('div');
//   loadingDiv.className = 'message bot loading';
//   loadingDiv.textContent = '로딩중...';
//   chatMessages.appendChild(loadingDiv);
//   scrollToBottom();
// }



// // Add event listener for the input field to detect "Enter" key press
// document.getElementById('userMessage').addEventListener('keyup', function(event) {
//   if (event.key === 'Enter') {
//     sendMessage(); // Call sendMessage() function when Enter key is pressed
//   }
// });

// function sendMessage() {
//   const userMessageInput = document.getElementById("userMessage");
//   const message = userMessageInput.value.trim();
//   const bookId = getBookIdFromUrl();

//   if (message !== "" && bookId) {
//     displayMessage("user", message);
//     userMessageInput.value = "";

//     showLoadingMessage();

//     // AJAX 요청을 보낼 URL을 동적으로 생성합니다.
//     const chatUrl = `/book-page/${bookId}/send_message/`; // book id 값을 URL에 넣어서 생성합니다.

//     // AJAX 요청을 보냅니다.
//     $.ajax({
//       type: "POST",
//       url: chatUrl,
//       data: { message: message },
//       dataType: "json",
//       success: function (response) {
//         removeLoadingMessage();

//         // 서버로부터의 응답을 처리합니다.
//         const botReply = response.reply;
//         displayMessage("bot", botReply);
//       },
//       error: function(xhr, status, error) {
//         // Remove the loading message and show an error message
//         removeLoadingMessage();
//         displayMessage('bot', '오류가 발생했습니다. 다시 시도해주세요.');
//         console.error('오류 발생:', error);
//       },
//     });
//   }
// }



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
  'ws://'
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

document.querySelector('#submit').onclick = function(e) {
  const userMessageInput = document.getElementById("userMessage");
  const message = userMessageInput.value.trim();
  const bookId = getBookIdFromUrl();

  if (message !== "" && bookId) {
    displayMessage("user", message);
    userMessageInput.value = "";

    showLoadingMessage();
    chatSocket.send(JSON.stringify({
      'message': message
    }));
  }
}