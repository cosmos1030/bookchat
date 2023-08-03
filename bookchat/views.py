from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

from .models import Books
from .generate_pkl import save_pickle
from .generate_model import ChainManager

# Create your views here.
def index(request):
    books = Books.objects.all() # DB의 모든 책 정보 불러오기
    path = settings.MEDIA_ROOT
    return render(request, 'bookchat/index.html', {
        "books": books,
        "path": path
    })

def book_page(request, id):
    book = Books.objects.get(id = id) # 특정 id의 책 불러오기
    if not book.pickle:
        save_pickle(id) # pickle 파일이 없다면 만들어 주기
        # 로딩 화면 구축
    return render(request, 'bookchat/book_page.html', {
        "book": book
    })

@csrf_exempt
def send_message(request, id):
    if request.method == 'POST':
        # 챗봇 로직 처리 (답변 생성)
        user_message = request.POST.get('message', '')

        chain_manager = ChainManager(id)

        # Use the chain to get the answer
        bot_reply = chain_manager.make_answer(user_message)

        return JsonResponse({'reply': bot_reply})
    else:
        return JsonResponse({'error': 'POST 요청만 지원합니다.'})

# def chat(request, id):
#     return render(request, 'bookchat/chat.html', {
#         "id": id
#     })