from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=50, null=False) 
    book_cover = models.ImageField(upload_to='img')
    file = models.FileField(upload_to='pdf')
    intro = models.CharField(max_length=200, null=False)
    author = models.CharField(max_length=20, null=False)
    author_intro = models.CharField(max_length=200, null=False)
    pickle = models.FileField(upload_to='pickle', blank=True)
    # users = models.ManyToManyField(User, through='Chat', related_name='users')

    def __str__(self):
        return f"{self.title} ({self.author})"

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # 메시지 보낸 시간
    is_user_message = models.BooleanField(default=False)  # 사용자가 보낸 메시지 여부
    def __str__(self):
        return f'{self.timestamp}: {"User" if self.is_user_message else "Bot"} - {self.msg}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    debated_books = models.ManyToManyField(Book, blank=True, related_name='user')