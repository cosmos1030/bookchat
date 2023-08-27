# myapi/models.py
from django.db import models
from account.models import CustomUser


# Create your models here.
class Books(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False) 
    file = models.FileField(upload_to='pdf')
    pickle = models.FileField(upload_to='pickle', blank=True)

    def __str__(self):
        return f"{self.title}"
