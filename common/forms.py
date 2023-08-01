from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm): # 기본 장고 폼을 이용해 회원가입 폼 생성
    email = forms.EmailField(label="이메일") # 이메일은 별도 추가
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']