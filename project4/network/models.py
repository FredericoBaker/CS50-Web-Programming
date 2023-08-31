from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    liked_by = models.ManyToManyField(User, symmetrical=False, blank=True, related_name="users_liked")
    timestamp = models.DateTimeField(auto_now_add=True)

    def count_likes(self):
        return self.liked_by.count()