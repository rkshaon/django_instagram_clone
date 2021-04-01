from django.urls import path
from direct_message.views import inbox, direct_message, send_dm, user_search, new_conversation

urlpatterns = [
    path('', inbox, name='inbox'),
    path('message/<username>', direct_message, name='direct_message'),
    path('send/', send_dm, name='send_dm'),
    path('new/', user_search, name='user_search'),
    path('new/<username>', new_conversation, name='newconversation'),
]
