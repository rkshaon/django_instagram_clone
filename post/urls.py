from django.urls import path

from post.views import index

urlpatterns = [
    path('', index, name='index'),
]
