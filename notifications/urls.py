from django.urls import path

from notifications.views import show_notification, delete_notification

urlpatterns = [
    path('', show_notification, name='show_notification'),
    path('<noti_id>/delete', delete_notification, name='delete_notification'),
]
