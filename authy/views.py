from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from authy.forms import SignupForm
from django.contrib.auth.models import User

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    template = loader.get_template('signup.html')
    return HttpResponse(template.render(context, request))
