from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import json
from django.urls import reverse

from .models import Book, UserProfile, Chat
from .generate_pkl import save_pickle
from .generate_model import ChainManager

# Create your views here.
def index(request):
    books = Book.objects.all() # DB의 모든 책 정보 불러오기
    path = settings.MEDIA_ROOT
    return render(request, 'bookchat/index.html', {
        "books": books,
        "path": path
    })

@login_required
def book_page(request, id):
    book = Book.objects.get(id = id) # 특정 id의 책 불러오기
    if not book.pickle:
        save_pickle(id) # pickle 파일이 없다면 만들어 주기
        # 로딩 화면 구축
    return render(request, 'bookchat/book_page.html', {
        "book": book
    })

def result_page(request, id):
    book = Book.objects.get(id = id) # 특정 id의 책 불러오기
    user = request.user
    return render(request, 'bookchat/result_page.html', {
        "book": book,
        "user": user
    })

def my_page(request):
    # user = None
    # if request.user.is_authenticated:
    #     user = request.user
    # user_profile = UserProfile.objects.get(user=user)
    # books = Book.objects.filter(user= user_profile)
    return render(request, 'bookchat/my_page.html', {})

@csrf_exempt
def send_message(request, id):
    if request.method == 'POST':
        # 챗봇 로직 처리 (답변 생성)
        user_message = request.POST.get('message', '')
        user = request.user

        chain_manager = ChainManager(id, user)

        # Use the chain to get the answer
        bot_reply = chain_manager.make_answer(user_message)

        return JsonResponse({'reply': bot_reply})
    else:
        return JsonResponse({'error': 'POST 요청만 지원합니다.'})

@csrf_exempt
def delete_chat_records(request, book_id):
    book = Book.objects.get(id=book_id)
    chat_records = Chat.objects.filter(user=request.user, book=book)
    chat_records.delete()
    return JsonResponse({"success": True})

@csrf_exempt
def make_report(request, book_id):
    id = book_id
    redirect_url = None
    if request.method == 'POST':
        chat_history = json.loads(request.body)['chatHistory']
        print(chat_history)
        # 리디렉션할 URL을 지정합니다. 예를 들어, 'report' 뷰로 리디렉션할 수 있습니다.
        redirect_url = reverse('bookchat:result-page', args=[id])
        print(redirect_url)
    return HttpResponseRedirect(redirect_url)
        