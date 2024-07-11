from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User
from .models import Comment



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['pk','title','data','likes','date','user']
        read_only_fields=['user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['pk','date','content','likes','post','user']
        read_only_fields=['user']