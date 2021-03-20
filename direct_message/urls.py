from django.urls import path
from direct_message.views import inbox

urlpatterns = [
    path('', inbox, name='inbox'),
]
