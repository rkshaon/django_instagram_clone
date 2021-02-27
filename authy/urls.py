from django.urls import path

from django.contrib.auth import views as authViews
from authy.views import sign_up

urlpatterns = [
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', sign_up, name='signup'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
]
