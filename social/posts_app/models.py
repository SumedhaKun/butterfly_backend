from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    followers=models.ManyToManyField(User, related_name= "followers",blank=True)
    following=models.ManyToManyField(User, related_name="following",blank=True)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class Post(models.Model):
    title=models.CharField(max_length=200)
    data=models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    likes=models.IntegerField(default=0)
    date=models.DateField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    caption=models.TextField(default="Loading...")

    def __str__(self):
        return self.title

class Comment(models.Model):
    date=models.DateField()
    content=models.TextField()
    likes=models.IntegerField(default=0)
    post=models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


