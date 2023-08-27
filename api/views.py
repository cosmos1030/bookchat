from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import Books
from account.models import CustomUser
from .generate_pkl import save_pickle
from .generate_model import ChainManager
from .serializers import BookSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser

@api_view(["GET"])
def book_list(request):
    books = Books.objects.all()
    return Response(
        {
            "books": BookSerializer(books, many=True).data,
        }
    )

class pdfUploadView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request):
        print(request.data)
        user_id = request.data['user_id']
        user = CustomUser.objects.get(id=user_id)
        file = request.data['file']
        title = request.data['title']
        book = Books.objects.create(
            user = user,
            file = file,
            title = title
        )
        book.save()
        return Response({'msg': 'success!!'})


@api_view(["GET"])
def book_page(request, id):
    book = Books.objects.get(id=id)
    if not book.pickle:
        save_pickle(id)
        # Create loading screen here
    return Response({"book": BookSerializer(book).data})


@api_view(["POST"])
def send_message(request, id):
    if request.method == "POST":
        user_message = request.data.get("message", "")

        chain_manager = ChainManager(id)

        bot_reply = chain_manager.make_answer(user_message)

        return Response({"reply": bot_reply})
    else:
        return Response({"error": "Only POST requests are supported."})

