# bookchat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer
# from .generate_model import ChainManager


class ChatConsumer(WebsocketConsumer):
    def connect(self): # 클라이언트가 서버에 연결됐을 때 실행
        self.id = self.scope['url_route']['kwargs']['room_name']
        print("웹소켓 연결 성공")
        self.accept() # 연결을 수락
        # self.chain_manager = ChainManager(self.id) # chain 생성

    def disconnect(self, close_code):
        print("웹소켓 연결 종료")

    def receive(self, text_data): # 전송된 메시지 처리, text_data에는 클라이언트가 전송한 메시지가 문자열 형태로 담겨있음
        text_data_json = json.loads(text_data) # 문자열을 딕셔너리 형태로 변환

        user_data = text_data_json

        # bot_reply = self.chain_manager.make_answer(user_message)
        bot_reply = {'message': "꺼져", 'sender': "bot"}

        print("메시지 수신 완료")

        self.send(text_data=json.dumps(bot_reply)) # 딕셔너리를 json 형태로 변환해 전송
