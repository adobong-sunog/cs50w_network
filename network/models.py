from cgitb import text
from email.policy import default
from tkinter import CASCADE, N
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from requests import delete

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

class Follows(models.Model):
    id = models.BigAutoField(primary_key=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="fwing")
    followers = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="fwers")

    class Meta:
        unique_together = ["following", "followers"]

    def __str__(self):
        return f"{self.followers} follows {self.following}"

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    image = models.URLField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    
class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["postID", "liker"]

    def __str__(self):
        return f"Post with {self.postID} liked by {self.liker}"