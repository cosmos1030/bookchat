# bookchat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer
from .generate_model import ChainManager
from .models import Chat, Book, UserProfile
from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(WebsocketConsumer):
    def make_initial_msg(self): # 첫 화면 메시지
        initial_msg = f"안녕 {self.user.username}! 나는 {self.book.title}의 작가 {self.book.author}이야. 나랑 어떤 주제에 대해 토론하고 싶어?"
        initial_chat = Chat(user=self.user, book=self.book, msg=initial_msg, is_user_message=False)
        initial_chat.save()
        self.send(text_data=json.dumps({"message": initial_msg, "sender": "bot"}))
    def get_history(self):
        user = self.scope['user']
        book = self.book
        chat_records = Chat.objects.filter(user=user, book=book)
        if len(chat_records)!=0:
            for record in chat_records:
                if record.is_user_message==True:
                    self.send(text_data=json.dumps({"message": record.msg, "sender": "user"}))
                else:
                    self.send(text_data=json.dumps({"message": record.msg, "sender": "bot"}))
        else:
            self.make_initial_msg()

    def connect(self): # 클라이언트가 서버에 연결됐을 때 실행
        self.id = self.scope['url_route']['kwargs']['room_name']
        print("웹소켓 연결 성공")
        self.book = Book.objects.get(id = self.id) # 책 정보 불러오기
        self.user = self.scope['user']
        self.accept() # 연결을 수락
        self.chain_manager = ChainManager(self.id, self.user) # chain 생성

        self.get_history()
        # self.send(text_data=json.dumps({"user": self.user.username, "book":{"title": self.book.title, "author": self.book.author}}))

    def disconnect(self, close_code):
        print("웹소켓 연결 종료")

    def receive(self, text_data): # 전송된 메시지 처리, text_data에는 클라이언트가 전송한 메시지가 문자열 형태로 담겨있음
        text_data_json = json.loads(text_data) # 문자열을 딕셔너리 형태로 변환
        user_message = text_data_json["message"]
        user = self.scope['user']
        user_chat = Chat(user=user, book=self.book, msg=user_message, is_user_message=True)
        user_chat.save()

        bot_reply = self.chain_manager.make_answer(user_message)
        bot_chat = Chat(user=user, book=self.book, msg=bot_reply, is_user_message=False)
        bot_chat.save()

        self.send(text_data=json.dumps({"message": bot_reply})) # 딕셔너리를 json 형태로 변환해 전송

        book = self.book
        user_profile = None
        try:
            user_profile = UserProfile.objects.get(user=self.user)
        except ObjectDoesNotExist:
            user_profile = UserProfile(user=self.user)
            user_profile.save()
            user_profile = UserProfile.objects.get(user=self.user)
        user_profile.debated_books.add(book) # 유저가 읽은 책 목록에 추가
        # self.send(text_data=json.dumps({"message": self.scope['user'].username})) # 딕셔너리를 json 형태로 변환해 전송
