from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=200)
    data=models.TextField()
    likes=models.IntegerField(default=0)
    date=models.DateField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    date=models.DateField()
    content=models.TextField()
    likes=models.IntegerField(default=0)
    post=models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


