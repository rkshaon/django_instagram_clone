from django.db import models
from django.contrib.auth.models import User
from post.models import Post

class Notification(models.Model):
    """docstring for Notification."""
    NOTIFICATION_TYPE = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))

    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
