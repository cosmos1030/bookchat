from django.contrib import admin
from django.urls import path, include
from bookchat.views import index
from django.conf import settings
from django.conf.urls.static import static
from account.views import register, login, user_profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bookchat.urls")),
    path("common/", include("common.urls")),
    path("api/", include("api.urls")),
    path("", index, name="index"),  # 로그인 후 홈페이지로 redirect를 위함
    path("api/login/", login),
    path("api/register/", register),
    path('api/user-profile/', user_profile),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
