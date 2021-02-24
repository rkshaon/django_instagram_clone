from django.urls import path

from post.views import index, new_post, post_details, tags, like

urlpatterns = [
    path('', index, name='index'),
    path('new/', new_post, name='new_post'),
    path('<uuid:post_id>', post_details, name='post_details'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
    path('<uuid:post_id>/like', like, name='post_like'),
]
