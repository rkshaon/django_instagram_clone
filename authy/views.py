from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import resolve
from django.contrib.auth.models import User

from authy.forms import SignupForm
from authy.models import Profile
from post.models import Post, Follow


def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favorites.all()

    # profile info stats
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follower_count = Follow.objects.filter(following=user).count()

    # paginator
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts_paginator,
        'profile': profile,
        'url_name': url_name,
        'post_count': post_count,
        'following_count': following_count,
        'follower_count': follower_count,
    }
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context, request))


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
