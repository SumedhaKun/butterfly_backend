from django.http import JsonResponse
from rest_framework.views import APIView  
from .models import Post
from .models import Comment
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserSerializer, CommentSerializer
from rest_framework import generics
import rest_framework.permissions
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.tokens import AccessToken
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


# User views:

@csrf_exempt 
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        headers={"Access-Control-Allow-Origin":"https://butterfly-frontend.onrender.com"}
        username=request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED,headers=headers)

@permission_classes([AllowAny])
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@ensure_csrf_cookie
@permission_classes([rest_framework.permissions.IsAuthenticated])
@api_view(['GET'])
def get_authenticated_user(request):
    user = request.user
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
            return Response("username or password is incorrect", status=status.HTTP_400_BAD_REQUEST)
        
@permission_classes([rest_framework.permissions.IsAuthenticated])
@api_view(['GET'])
def get_user_by_key(request,pk):
    try:
        user = User.objects.get(pk=pk)
        followers=user.profile.followers
        followers = UserSerializer(followers, many=True)

        following=user.profile.following
        following = UserSerializer(following, many=True)
        data = {
            'username': user.username,
            'email': user.email,
            'followers': followers.data,
            'following':following.data
        }
        return Response(data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])
def follow_user(request,pk):
    user_to_follow=User.objects.get(pk=pk)
    request.user.profile.following.add(user_to_follow)
    user_to_follow.profile.followers.add(request.user)
    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH'])
def unfollow_user(request,pk):
    user_to_unfollow=User.objects.get(pk=pk)
    request.user.profile.following.remove(user_to_unfollow)
    user_to_unfollow.profile.followers.remove(request.user)
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_followers(request):
    followers=request.user.profile.followers
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_following(request):
    following=request.user.profile.following
    serializer = UserSerializer(following, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request,pk):
    user=User.objects.get(pk=pk)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Post Views:

def save_image(image):
    aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    aws_storage_bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    img = Image.open(image)
    img.thumbnail((300, 300))
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    image_file = InMemoryUploadedFile(
        buffer, None, 'example.jpg', 'image/jpeg', buffer.getbuffer().nbytes, None
    )
    s3_client = boto3.client('s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    try:
        s3_client.upload_fileobj(image_file, aws_storage_bucket_name, 'images/example.jpg')
    except ClientError as e:
        print(e)
        return None

    return image_file.url

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        print(request.FILES) 
        return super().create(request, *args, **kwargs)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]

@api_view(['GET'])
def get_posts_by_user(request,pk):
    user=User.objects.get(pk=pk)
    posts=Post.objects.filter(user=user)
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False,status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_post_likes(request,pk):
    post=Post.objects.get(pk=pk)
    post.likes+=1
    post.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_caption(request,pk):
    post=Post.objects.get(pk=pk)
    post.caption=request.data["caption"]
    post.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_post(request,pk):
    post=Post.objects.get(pk=pk)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#Comment views:

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@api_view(['GET'])
def get_comments_by_post(request,pk):
    post=Post.objects.get(pk=pk)
    comments=Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
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
    comment.likes+=1
    comment.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_comment(request,pk):
    comment=Comment.objects.get(pk=pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

    








    