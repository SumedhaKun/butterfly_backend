from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView  
# Create your views here.
from .models import Post
from .models import Comment
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserSerializer, CommentSerializer
from rest_framework import generics
import rest_framework.permissions
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.tokens import AccessToken
@csrf_exempt 
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        print(request.data)
        username=request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'User registered successfully'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@permission_classes([AllowAny])
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
@permission_classes([rest_framework.permissions.IsAuthenticated])
@api_view(['GET'])
def get_user_by_key(request,pk):
    try:
        user = User.objects.get(pk=pk)
        print(user)
        data = {
            'username': user.username,
            'email': user.email,
        }
        return Response(data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@ensure_csrf_cookie
@permission_classes([rest_framework.permissions.IsAuthenticated])
@api_view(['GET'])
def get_authenticated_user(request):
    user = request.user
    if user:
        print(user.get_username())
    headers={"Access-Control-Allow-Origin":"http://127.0.0.1:3000", "Access-Control-Allow-Credentials": "true",}
    if user.is_authenticated:
        data = {
            'username': user.username,
            'email': user.email,
        }
        return Response(data, status=200,headers=headers)
    else:
        return Response({'error': 'User not authenticated'}, status=401,headers=headers)
@csrf_exempt 
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'POST':
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            # login(request, user)
            print(user.get_username())
            access_token = AccessToken.for_user(user)
            return Response({'token': str(access_token)},status=status.HTTP_200_OK)
            
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
               
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]

@api_view(['GET'])
def get_comments_by_post(request,pk):
    post=Post.objects.get(pk=pk)
    comments=Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    print(comments)
    return JsonResponse(serializer.data, safe=False,status=status.HTTP_200_OK)

@api_view(['POST'])
def create_comment(request):
    content=request.data["content"]
    date=request.data["date"]
    pk=request.data["pk"]
    post=Post.objects.get(pk=pk)
    comment=Comment.objects.create(content=content,date=date, post=post,user=request.user)
    comment.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_comment_likes(request,pk):
    comment=Comment.objects.get(pk=pk)
    print(comment.likes)
    comment.likes+=1
    print(comment.likes)
    comment.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_post_likes(request,pk):
    post=Post.objects.get(pk=pk)
    post.likes+=1
    post.save()
    return Response(status=status.HTTP_200_OK)


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer






    