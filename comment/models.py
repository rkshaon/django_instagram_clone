from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User

from post.models import Post
from notifications.models import Notification

class Comment(models.Model):
    """docstring for Comment."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user

        notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_type=2)
        notify.save()

    def user_delete_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user

        notify = Notification.objects.filter(post=post, sender=sender, user=post.user, notification_type=2)
        notify.delete()

    def __str__(self):
        return str(self.user) + " - " + str(self.body) + " - " + str(self.date)

# Comment
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_delete_comment_post, sender=Comment)
