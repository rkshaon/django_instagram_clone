from django.urls import path

from notifications.views import show_notification

urlpatterns = [
    path('', show_notification, name='show_notification'),
]
