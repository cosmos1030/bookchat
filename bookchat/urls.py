from django.urls import path, include
from .views import index, book_page
from . import routing

app_name = 'bookchat'

urlpatterns = [
    path("", index, name='index'),
    path("book-page/<int:id>/", book_page, name="book-page"),
    # path("book-page/<id>/send_message/", send_message, name="send_message"),
]