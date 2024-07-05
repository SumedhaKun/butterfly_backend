from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView  
# Create your views here.
from .models import Post
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserSerializer
from rest_framework import generics
import rest_framework.permissions
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view


@csrf_exempt 
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        print(request.data)
        username=request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        # check validity
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'User registered successfully'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

def get_authenticated_user(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
    })

@api_view(['GET'])
def get_authentication_status(request):
    user=request.user
    print(user)
    print(user.is_authenticated)
    if user.is_authenticated:
        return Response({'authenticated': True, 'username': user.username},status=status.HTTP_200_OK)
    else:
        return Response({'authenticated': False},status=status.HTTP_200_OK)

@csrf_exempt 
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.get_username())
            print(user.is_authenticated)
            return Response({'username': username},status=status.HTTP_200_OK)
            
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticatedOrReadOnly]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticatedOrReadOnly]
