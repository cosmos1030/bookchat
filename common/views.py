from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save() # 데이터베이스에 저장
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = raw_password) # 유저 인증
            login(request, user) # 회원가입 후 바로 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form}) # 같은 url로 post 요청 보내기