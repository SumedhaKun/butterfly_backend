from django.test import TestCase
from .models import Post,User, Comment
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
        self.image = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        self.image.save(img_io, format='JPEG')
        self.image_file = ContentFile(img_io.read(), 'test_image.jpg')

    def test_model_creation(self):
        post=Post.objects.create(title="Test Title",data="Test Data", image=self.image_file, date="2024-07-03" )
        self.assertEqual(post.image.name, 'test_image.jpg')
        self.assertEqual(post.title,"Test Title")
        self.assertEqual(post.data,"Test Data")
        self.assertEqual(post.likes, 0)
        self.assertEqual(post.date,"2024-07-03")
        self.assertEqual(post.caption,"Loading...")

class CommentTestCase(TestCase):
    def setUp(self):
        self.image = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        self.image.save(img_io, format='JPEG')
        self.image_file = ContentFile(img_io.read(), 'test_image.jpg')

    def test_model_creation(self):
        post=Post.objects.create(title="Test Title",data="Test Data", image=self.image_file, date="2024-07-03" )
        comment=Comment.objects.create(date="2024-07-03",content="Test Content", post=post)
        self.assertEqual(comment.post.title,"Test Title")
        self.assertEqual(comment.date,"2024-07-03")
        self.assertEqual(comment.content,"Test Content")
        self.assertEqual(comment.likes,0)

class UserTestCase(TestCase):
    def test_model_creation(self):
        user=User.objects.create(username="test_name",email="test@gmail.com",password="password")
        self.assertEqual(user.username,"test_name")
        self.assertEqual(user.email,"test@gmail.com")


