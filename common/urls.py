from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='common/login.html'), name='login'), # 장고 기본제공 로그인 창 활용
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'), 
]