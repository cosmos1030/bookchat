from django.urls import path
from .views import book_list, book_page, pdfUploadView
from . import routing

app_name = 'api'

urlpatterns = [
    path("book-list/", book_list),
    path('upload/', pdfUploadView.as_view()),
    path("book-page/<int:id>/", book_page, name="book-page"),
]