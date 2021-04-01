from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.core.paginator import Paginator

from django.db.models import Q
from django.contrib.auth.models import User
from direct_message.models import Message

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_dm = None
    directs = None

    if messages:
        message = messages[0]
        active_dm = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_dm:
                message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_dm': active_dm,
    }

    template = loader.get_template('dm/direct.html')

    return HttpResponse(template.render(context, request))

@login_required
def direct_message(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_dm = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_dm': active_dm,
    }

    template = loader.get_template('dm/direct.html')

    return HttpResponse(template.render(context, request))

@login_required
def new_conversation(request, username):
	from_user = request.user
	body = ''

	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('user_search')

	if from_user != to_user:
		Message.send_message(from_user, to_user, body)

	return redirect('inbox')

@login_required
def send_dm(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    print(request.POST)
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)

        return redirect('inbox')
    else:
        HttpResponseBadRequest()

@login_required
def user_search(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
        }

    template = loader.get_template('dm/search_user.html')

    return HttpResponse(template.render(context, request))
