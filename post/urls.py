from django.urls import path

from post.views import index, new_post

urlpatterns = [
    path('', index, name='index'),
    path('new/', new_post, name='new_post'),
]
