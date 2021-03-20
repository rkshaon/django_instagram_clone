from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

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
