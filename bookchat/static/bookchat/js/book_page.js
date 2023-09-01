import {chatHistory} from './script.js'

console.log(chatHistory)

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

const book_id = getBookIdFromUrl()

// document.querySelector('#reset').onclick = function (e){
//     axios.delete(`/api/chat/${book_id}/delete`).then(() => {
//         console.log("채팅 기록이 성공적으로 삭제되었습니다!!!");
//         window.location.reload();
//     }).catch(() => {
//         console.log("채팅 기록 삭제에 실패했습니다.");
//     });
// }

// document.querySelector('#end').onclick = function (e){
//   axios.post(`/api/chat/${book_id}/end/`, {chatHistory})
//   .then(() => {
//       console.log("POST 요청이 성공했습니다.");
//   }).catch(() => {
//       console.log("POST 요청이 실패했습니다.");
//   });
// }