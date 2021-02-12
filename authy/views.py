from django.shortcuts import render
from authy.forms import SignupForm

def Signup(request):
    form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
