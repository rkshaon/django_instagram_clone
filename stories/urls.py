from django.urls import path
from stories.views import new_story, show_media

urlpatterns = [
    path('new/', new_story, name='new_story'),
    path('showmedia/<stream_id>', show_media, name='show_media'),
]
