from django.urls import path, include
from .views import index, book_page, my_page, delete_chat_records, result_page, make_report
from . import routing

app_name = 'bookchat'

urlpatterns = [
    path("", index, name='index'),
    path("book-page/<int:id>/", book_page, name="book-page"),
    path("result-page/<int:id>/", result_page, name="result-page"),
    path("my-page/", my_page, name="my-page"),
    path("api/chat/<int:book_id>/delete/", delete_chat_records),
    path("api/chat/<int:book_id>/end/", make_report),
    # path("book-page/<id>/send_message/", send_message, name="send_message"),
]