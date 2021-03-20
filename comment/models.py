from django.db import models
from post.models import Post
from django.contrib.auth.models import User

class Comment(models.Model):
    """docstring for Comment."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
